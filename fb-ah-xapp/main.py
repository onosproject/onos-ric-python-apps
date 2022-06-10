#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright 2004-present Facebook. All Rights Reserved.
# SPDX-FileCopyrightText: 2019-present Open Networking Foundation <info@opennetworking.org>
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import asyncio
import json
import logging
from typing import Dict, Optional, Tuple

from aiohttp import web

import onos_ric_sdk_py as sdk
from airhop_pci.airhop import AirhopEsonClient, make_neighbor as ah_make_neighbor
from airhop_pci.airhop_api.com.airhopcomm.eson.nr.v1 import (
    Cell,
    CellSize,
    CellSpecificOffsets,
    EventA3ReportConfig,
    NeighborList,
    PciPool,
    PciRange,
)
from airhop_pci.cells_tracker import CellChanges, CellsTracker, CellsState, cgiFromNcgi
from airhop_pci.kpi import track_kpi
from onos_api.e2t.e2.v1beta1 import (
    Action,
    ActionType,
    SubsequentAction,
    SubsequentActionType,
    TimeToWait,
)
from onos_e2_sm.e2sm_rc_pre.v2 import (
    # subscription
    E2SmRcPreEventTriggerDefinition,
    E2SmRcPreEventTriggerDefinitionFormat1,
    E2SmRcPreIndicationHeader,
    E2SmRcPreIndicationMessage,
    RcPreTriggerType,
    # control
    CellGlobalId,
    E2SmRcPreControlHeader,
    E2SmRcPreControlHeaderFormat1,
    E2SmRcPreControlMessage,
    E2SmRcPreControlMessageFormat1,
    E2SmRcPreControlOutcome,
    RanparameterDefItem,
    RanparameterId,
    RanparameterName,
    RanparameterType,
    RanparameterValue,
    RcPreCommand,
    RicControlMessagePriority,
)


async def async_main(
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    ct: CellsTracker,
    pci_disable_control: bool,
    mlb_disable_control: bool,
) -> None:
    async with e2_client, sdl_client:
        with AirhopEsonClient(args.eson_endpoint) as eson_client:
            kpi: Dict[Tuple[str, str], Dict[str, int]] = {}
            # kpi = {(e2node_id, cid): {metric_name: metric_value, ...}, ...}

            asyncio.create_task(
                # query changes to pci via subscribe()
                subscribe_pci_changes(e2_client, eson_client, ct, pci_disable_control),
            )
            asyncio.create_task(
                # query changes to pci via retrieve_proposed_changes()
                monitor_proposed_changes(
                    e2_client, eson_client, ct, pci_disable_control
                ),
            )
            asyncio.create_task(
                # MLB: update capacity
                update_eson_capacity(e2_client, eson_client, kpi, ct),
            )
            asyncio.create_task(
                # MLB: subscription
                subscribe_mlb_changes(e2_client, eson_client, ct, mlb_disable_control),
            )

            async for e2_node_id, e2_node in sdl_client.watch_e2_connections():

                logging.info(f"Found e2node {e2_node}")

                asyncio.create_task(
                    subscribe_e2(
                        e2_node_id,
                        e2_client,
                        sdl_client,
                        eson_client,
                        ct,
                        mlb_disable_control,
                    ),
                )

                asyncio.create_task(
                    # MLB: subscribe to kpi e2 messages
                    track_kpi(e2_client, sdl_client, e2_node_id, e2_node, kpi),
                )


async def subscribe_e2(
    e2_node_id: str,
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    eson_client: AirhopEsonClient,
    cells_tracker: CellsTracker,
    mlb_disable_control: bool,
) -> None:
    if args.trigger_periodic_s:
        trigger = E2SmRcPreEventTriggerDefinition(
            event_definition_format1=E2SmRcPreEventTriggerDefinitionFormat1(
                trigger_type=RcPreTriggerType.RC_PRE_TRIGGER_TYPE_PERIODIC,
                reporting_period_ms=args.trigger_periodic_s * 1000,
            )
        )
    else:
        trigger = E2SmRcPreEventTriggerDefinition(
            event_definition_format1=E2SmRcPreEventTriggerDefinitionFormat1(
                trigger_type=RcPreTriggerType.RC_PRE_TRIGGER_TYPE_UPON_CHANGE,
            )
        )

    logging.info(f"Subscribing rc-pre node {e2_node_id}")

    # load previously saved cell information state from topo
    for cell in await sdl_client.get_cells(e2_node_id):
        try:
            data = await sdl_client.get_cell_data(
                e2_node_id,
                cell.cell_global_id.value,
                [
                    "E2SmRcPreIndicationHeader",
                    "E2SmRcPreIndicationMessage",
                    "onos.topo.Location",
                    "onos.topo.Coverage",
                ],
            )
            if data is None:
                logging.warning(
                    f"get_cell_data empty for {e2_node_id} id:0x{cell.cell_global_id.value}"
                )
                continue
        except sdk.exceptions.ClientRuntimeError:
            logging.exception(
                f"get_cell_data failed for {e2_node_id} id:0x{cell.cell_global_id.value}"
            )
            continue

        header_json, message_json, location, coverage = data

        if header_json is None or message_json is None:
            logging.info(
                f"Found no data for {e2_node_id} id:0x{cell.cell_global_id.value}"
            )
        else:
            ind_header = E2SmRcPreIndicationHeader().from_json(
                header_json.decode("utf-8")
            )
            ind_message = E2SmRcPreIndicationMessage().from_json(
                message_json.decode("utf-8")
            )

            changes = await process_indication(
                e2_node_id,
                e2_client,
                sdl_client,
                eson_client,
                cells_tracker,
                ind_header,
                ind_message,
                mlb_disable_control,
            )

            if not changes:
                logging.warning(
                    f"Data found for {e2_node_id} id:0x{cell.cell_global_id.value} but no changes detected"
                )
                continue

            logging.info(f"Loaded saved ncgi 0x{changes.ncgi:x}")

            if location is not None:
                loc = json.loads(location.decode("utf-8"))
                cells_tracker.ncgi_cells_map[changes.ncgi].lat = loc["lat"]
                cells_tracker.ncgi_cells_map[changes.ncgi].lng = loc["lng"]
                logging.info(f"Loaded location for 0x{changes.ncgi:x}")

            if coverage is not None:
                cov = json.loads(coverage.decode("utf-8"))
                cells_tracker.ncgi_cells_map[changes.ncgi].azimuth = cov["azimuth"]
                cells_tracker.ncgi_cells_map[changes.ncgi].arc_width = cov["arc_width"]
                cells_tracker.ncgi_cells_map[changes.ncgi].tilt = cov["tilt"]
                cells_tracker.ncgi_cells_map[changes.ncgi].height = cov["height"]
                logging.info(f"Loaded coverage for 0x{changes.ncgi:x}")

    async for (header, message) in e2_client.subscribe(
        e2_node_id=e2_node_id,
        service_model_name="oran-e2sm-rc-pre",
        service_model_version="v2",
        subscription_id="fb-ah_oran-e2sm-rc-pre_sub",
        trigger=bytes(trigger),
        actions=[
            Action(
                id=10,
                type=ActionType.ACTION_TYPE_REPORT,
                subsequent_action=SubsequentAction(
                    type=SubsequentActionType.SUBSEQUENT_ACTION_TYPE_CONTINUE,
                    time_to_wait=TimeToWait.TIME_TO_WAIT_ZERO,
                ),
            )
        ],
    ):
        if len(header) == 0 or len(message) == 0:
            logging.warning(
                f"skipping empty indication header/message from '{e2_node_id}'..."
            )
            continue

        ind_header = E2SmRcPreIndicationHeader().parse(header)
        ind_message = E2SmRcPreIndicationMessage().parse(message)

        changes = await process_indication(
            e2_node_id,
            e2_client,
            sdl_client,
            eson_client,
            cells_tracker,
            ind_header,
            ind_message,
            mlb_disable_control,
        )

        if not changes:
            continue

        cell_id = format(changes.nci, "x")

        # due to intricacies of the system, a few retries are standard practice
        for retry_count in range(5):
            try:
                # save cell information state into topo to be used if app restarts
                await sdl_client.set_cell_data(
                    e2_node_id,
                    cell_id,
                    {
                        "E2SmRcPreIndicationHeader": bytes(
                            ind_header.to_json(), "utf-8"
                        ),
                        "E2SmRcPreIndicationMessage": bytes(
                            ind_message.to_json(), "utf-8"
                        ),
                    },
                )
                break
            except sdk.exceptions.ClientRuntimeError:
                logging.exception(f"set_cell_data failed, try {retry_count + 1}")
            asyncio.sleep(0.05 * retry_count)


async def process_indication(
    e2_node_id: str,
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    eson_client: AirhopEsonClient,
    cells_tracker: CellsTracker,
    ind_header: E2SmRcPreIndicationHeader,
    ind_message: E2SmRcPreIndicationMessage,
    mlb_disable_control: bool,
) -> Optional[CellChanges]:

    changes = cells_tracker.update(
        e2_node_id=e2_node_id,
        indication_header=ind_header.indication_header_format1,
        indication_message=ind_message.indication_message_format1,
    )
    if not changes:
        return
    logging.debug(f"Changes indicated: {changes}")

    coros = []
    if changes.cell_to_register:
        action = "Updating pci" if changes.is_update else "Registering new cell"
        logging.info(
            f"{action} for '{e2_node_id}': "
            f"ncgi=0x{changes.ncgi:x} "
            f"pci={changes.cell_to_register.pci}"
        )

        # Agreed offline with Radisys what these parameters should be:

        # hysteresis = +1dB
        # We expect to receive 2, because of
        # The IE Hysteresis is a parameter used within the entry and leave condition of an event
        # triggered reporting condition. The actual value is field value * 0.5 dB.

        # a3offset = +2dB
        # We expect to receive 4, because of
        # Offset value(s) to be used in NR measurement report triggering condition for event
        # a3/a6. The actual value is field value * 0.5 dB.

        # all others are 0dB
        # We expect to receive 15 for 0dB.

        coros.append(
            eson_client.register(
                cells=[
                    Cell(
                        ncgi=changes.ncgi,
                        cell_size=CellSize.CELL_SIZE_OUTDOOR_SMALL,
                        dl_nrarfcn=changes.cell_to_register.fcn,
                        ul_nrarfcn=changes.cell_to_register.fcn,
                        pci=changes.cell_to_register.pci,
                        pci_pool=PciPool(
                            [
                                PciRange(lower_pci=1, upper_pci=10),
                                PciRange(lower_pci=20, upper_pci=300),
                            ]
                        ),
                        neighbors=NeighborList(
                            [
                                ah_make_neighbor(n_ncgi, n_pci, n_fcn)
                                for n_ncgi, (n_pci, n_fcn) in sorted(
                                    changes.cell_to_register.neighbors.items()
                                )
                            ]
                        ),
                        vendor_info="vendor_info",
                        capacity_class_value=100,  # Airhop(BG) says set to 100.
                        event_a3_report_configs=EventA3ReportConfig(
                            nrarfcn=changes.cell_to_register.fcn,
                            offset=4,  # +2dB, value * 0.5 dB
                            hysteresis=2,  # +1dB, value * 0.5 dB
                        ),
                        cell_specific_offsets=CellSpecificOffsets(
                            cio=15,  # 0dB, value 15
                            offset_freq=15,  # 0dB, value 15
                            q_offset=15,  # 0dB, value 15
                        ),
                    ),
                ]
            )
        )

        # best effort set initial cell individual offset (cio) for all neighbors
        if mlb_disable_control:
            logging.warning(
                f"MLB --mlb-disable-control is set, skipping initial setting"
            )
        else:
            for neighbor_ncgi, _ in sorted(changes.cell_to_register.neighbors.items()):
                logging.info(
                    f"MLB initial OCN ncgi:0x{changes.ncgi:x} neighbor_ncgi:0x{neighbor_ncgi:x}"
                )
                coros.append(
                    update_mlb_cio(
                        e2_client=e2_client,
                        e2_node_id=e2_node_id,
                        cgi=changes.cell_to_register.cgi,
                        neighbor_cgi=cgiFromNcgi(neighbor_ncgi),
                        cell_individual_offset=15,  # 0dB, value 15
                        q_offset=15,  # 0dB, value 15
                    )
                )

    if changes.neighbors_to_add:
        logging.info(
            f"Adding neighbor: "
            f"ncgi=0x{changes.ncgi:x} "
            f"neighbors={sorted(changes.neighbors_to_add.items())}"
        )
        coros.append(eson_client.add_neighbor(changes.ncgi, changes.neighbors_to_add))

    if changes.neighbors_to_update:
        logging.info(
            f"Updating neighbor: "
            f"ncgi=0x{changes.ncgi:x} "
            f"neighbors={[(hex(n), p) for n, p in sorted(changes.neighbors_to_update.items())]}"
        )
        # airhop's "add" call also used to update neighbor information
        coros.append(
            eson_client.add_neighbor(changes.ncgi, changes.neighbors_to_update)
        )

    if changes.neighbors_to_remove:
        logging.info(
            f"Removing neighbor: "
            f"ncgi=0x{changes.ncgi:x} "
            f"neighbors={[hex(n) for n in sorted(changes.neighbors_to_remove)]}"
        )
        coros.append(
            eson_client.remove_neighbor(changes.ncgi, changes.neighbors_to_remove)
        )

    await asyncio.gather(*coros, return_exceptions=True)

    return changes


async def subscribe_pci_changes(
    e2_client: sdk.E2Client,
    eson_client: AirhopEsonClient,
    cells_tracker: CellsTracker,
    pci_disable_control: bool,
) -> None:
    """
    Subscribe to changes of pci due to conflicts.
    Changes are triggered when a Register or Add/Remove neighbor event occurs.
    To trigger a full conflict check, call pci_detect_and_resolve()
    """
    if args.pci_subscribe_delay is None:
        return
    if args.pci_subscribe_delay > 0:
        await asyncio.sleep(args.pci_subscribe_delay)
    logging.info(f"subscribe_pci_changes: waiting for changes")
    while True:
        try:
            async for change_request in eson_client.pci_subscribe():
                if args.processing_delay:
                    await asyncio.sleep(args.processing_delay)

                try:
                    e2_node_id = cells_tracker.get_e2_node_id(change_request.ncgi)
                except KeyError:
                    logging.warning(
                        f"subscribe_pci_changes: "
                        f"Received ncgi=0x{change_request.ncgi:x} pci={change_request.pci} "
                        f"but ncgi is not present, ignoring change."
                    )
                    continue

                logging.info(
                    f"subscribe_pci_changes: "
                    f"Received ncgi=0x{change_request.ncgi:x} pci={change_request.pci}"
                )

                if pci_disable_control:
                    logging.warning(
                        f"PCI --pci-disable-control is set, skipping update"
                    )
                    await eson_client.pci_confirm_change(
                        ncgi=change_request.ncgi, pci=change_request.pci
                    )
                    continue

                if await update_pci(
                    e2_client=e2_client,
                    e2_node_id=e2_node_id,
                    cgi=cells_tracker.get_cgi(change_request.ncgi),
                    new_pci=change_request.pci,
                ):
                    await eson_client.pci_confirm_change(
                        ncgi=change_request.ncgi, pci=change_request.pci
                    )
                else:
                    logging.warning(
                        f"Cannot update ncgi=0x{change_request.ncgi:x} -> pci={change_request.pci}. "
                        f"pci remains {cells_tracker.get_pci(change_request.ncgi)}."
                    )
                    await eson_client.pci_reject_change(
                        ncgi=change_request.ncgi,
                        pci=cells_tracker.get_pci(change_request.ncgi),
                    )
        except RuntimeError:
            logging.info(
                "subscribe_pci_changes() connection idled out, resubscribing..."
            )
        except Exception:
            logging.exception("subscribe_pci_changes() failed, resubscribing...")
        await asyncio.sleep(5)


async def monitor_proposed_changes(
    e2_client: sdk.E2Client,
    eson_client: AirhopEsonClient,
    cells_tracker: CellsTracker,
    pci_disable_control: bool,
) -> None:
    if args.pci_maintenance_delay is None:
        return
    if args.pci_maintenance_delay > 0:
        await asyncio.sleep(args.pci_maintenance_delay)
    while True:
        change_requests = await eson_client.pci_get_proposed_changes()
        for change_request in change_requests:
            try:
                e2_node_id = cells_tracker.get_e2_node_id(change_request.ncgi)
            except KeyError:
                logging.warning(
                    f"proposed_change: "
                    f"Received ncgi=0x{change_request.ncgi:x} pci={change_request.pci} "
                    f"but ncgi is not present, ignoring change."
                )
                continue
            logging.info(
                f"Received ncgi=0x{change_request.ncgi:x} pci={change_request.pci}"
            )

            if pci_disable_control:
                logging.warning(f"PCI --pci-disable-control is set, skipping update")
                await eson_client.pci_confirm_change(
                    ncgi=change_request.ncgi, pci=change_request.pci
                )
                continue

            if await update_pci(
                e2_client=e2_client,
                e2_node_id=e2_node_id,
                cgi=cells_tracker.get_cgi(change_request.ncgi),
                new_pci=change_request.pci,
            ):
                await eson_client.pci_confirm_change(
                    ncgi=change_request.ncgi, pci=change_request.pci
                )
            else:
                logging.warning(
                    f"Cannot update ncgi=0x{change_request.ncgi:x} -> {change_request.pci}. "
                    f"pci remains {cells_tracker.get_pci(change_request.ncgi)}."
                )
                await eson_client.pci_reject_change(
                    ncgi=change_request.ncgi,
                    pci=cells_tracker.get_pci(change_request.ncgi),
                )
        await asyncio.sleep(args.pci_maintenance_period)


async def update_pci(
    e2_client: sdk.E2Client, e2_node_id: str, cgi: CellGlobalId, new_pci: int
) -> bool:
    """
    return True if successful
    """
    hdr = E2SmRcPreControlHeader(
        control_header_format1=E2SmRcPreControlHeaderFormat1(
            rc_command=RcPreCommand.RC_PRE_COMMAND_SET_PARAMETERS,
            cgi=cgi,
        )
    )

    msg = E2SmRcPreControlMessage(
        control_message=E2SmRcPreControlMessageFormat1(
            # TODO: this should probably be a list, or outcomes should not be a list
            parameter_type=RanparameterDefItem(
                ran_parameter_id=RanparameterId(value=1),  # unique within this message
                ran_parameter_name=RanparameterName(value="pci"),
                ran_parameter_type=RanparameterType.RANPARAMETER_TYPE_INTEGER,
            ),
            parameter_val=RanparameterValue(value_int=new_pci),
        )
    )

    # TODO: don't catch exception in this function
    try:
        response = await e2_client.control(
            e2_node_id=e2_node_id,
            service_model_name="oran-e2sm-rc-pre",
            service_model_version="v2",
            header=bytes(hdr),
            message=bytes(msg),
        )
        if response is None:
            logging.warning(f"Control ACK is set to `NO_ACK`, skipping...")
            return False

        outcome = E2SmRcPreControlOutcome()
        outcome.parse(response)
        logging.info(f"Update PCI succeeded, outcome: {outcome}")
        return True
    except sdk.exceptions.ClientRuntimeError:
        logging.exception("Update PCI failed")
        return False


async def update_eson_capacity(
    e2_client: sdk.E2Client,
    eson_client: AirhopEsonClient,
    kpi: Dict[Tuple[str, str], Dict[str, int]],
    cells_tracker: CellsTracker,
) -> None:
    """
    update eson capacity for each cell

    kpi = {cid: {metric_name: metric_value, ...}, ...}
    """
    if args.mlb_update_capacity_period is None:
        return
    logging.info(f"MLB: monitoring kpi to report capacity")
    while True:
        coros = []
        for (e2_node_id, cid_str), metrics in kpi.items():
            if e2_node_id == "global":
                logging.info(f"MLB: stats: {cid_str} = {metrics}")
                continue

            cid = int(cid_str, 16)
            ncgi = cells_tracker.find_ncgi(e2_node_id, cid)

            if ncgi is None:
                logging.warning(f"MLB: unable to find ncgi for cid 0x{cid:x} '")

            conn_mean = metrics.get("RRC.Conn.Avg", None)
            if conn_mean is None:
                conn_mean = metrics.get("RRC.ConnMean", None)
            if conn_mean is None:
                logging.warning(
                    f"MLB: ncgi 0x{ncgi:x} missing 'RRC.Conn.Avg' of 'RRC.ConnMean'"
                )
                continue

            # normalize between 0 and 100, max 10 UEs
            capacity_value = int((1 - int(conn_mean) / 10) * 100)

            if capacity_value < 0:
                logging.warning(
                    f"MLB: ncgi 0x{ncgi:x} calculated capacity "
                    f"less than zero ({capacity_value}), overriden to 0."
                )
                capacity_value = 0

            coros.append(eson_client.mlb_report_capacity(ncgi, capacity_value))
            logging.info(
                f"MLB: reporting ncgi 0x{ncgi:x} capacity -> {capacity_value} "
                f"(conn mean={conn_mean})"
            )

        try:
            await asyncio.gather(*coros)
        except Exception:
            logging.exception("update_eson_capacity() failed, try again later...")
        await asyncio.sleep(args.mlb_update_capacity_period)


async def subscribe_mlb_changes(
    e2_client: sdk.E2Client,
    eson_client: AirhopEsonClient,
    cells_tracker: CellsTracker,
    mlb_disable_control: bool,
) -> None:
    """
    Subscribe to changes for MLB.
    """
    logging.info(f"subscribe_mlb_changes: waiting for changes")
    while True:
        try:
            async for change_request in eson_client.mlb_subscribe():
                if args.processing_delay:
                    await asyncio.sleep(args.processing_delay)

                try:
                    e2_node_id = cells_tracker.get_e2_node_id(change_request.ncgi)
                except KeyError:
                    logging.warning(
                        f"subscribe_mlb_changes: "
                        f"Received ncgi=0x{change_request.ncgi:x} "
                        f"but ncgi is not present, ignoring change."
                    )
                    continue

                try:
                    neighbor_cgi = cells_tracker.get_cgi(change_request.neighbor_ncgi)
                except KeyError:
                    logging.warning(
                        f"subscribe_mlb_changes: "
                        f"Received ncgi=0x{change_request.ncgi:x} "
                        f"but neighbor_ncgi=0x{change_request.neighbor_ncgi:x} is not present, "
                        f"ignoring change."
                    )
                    continue

                logging.info(
                    f"subscribe_mlb_changes: "
                    f"Received ncgi=0x{change_request.ncgi:x} "
                    f"neighbor_ncgi=0x{change_request.neighbor_ncgi:x} "
                    f"cio={change_request.cio} "
                    f"q_offset={change_request.q_offset}"
                )

                if mlb_disable_control:
                    logging.warning(
                        f"MLB --mlb-disable-control is set, skipping update"
                    )
                    await eson_client.mlb_confirm_change(
                        ncgi=change_request.ncgi,
                        neighbor_ncgi=change_request.neighbor_ncgi,
                        cio=change_request.cio,
                        q_offset=change_request.q_offset,
                    )
                    continue

                if await update_mlb_cio(
                    e2_client=e2_client,
                    e2_node_id=e2_node_id,
                    cgi=cells_tracker.get_cgi(change_request.ncgi),
                    neighbor_cgi=neighbor_cgi,
                    cell_individual_offset=change_request.cio,
                    q_offset=change_request.q_offset,
                ):
                    await eson_client.mlb_confirm_change(
                        ncgi=change_request.ncgi,
                        neighbor_ncgi=change_request.neighbor_ncgi,
                        cio=change_request.cio,
                        q_offset=change_request.q_offset,
                    )
                else:
                    logging.warning(
                        f"subscribe_mlb_changes: "
                        f"Cannot update mlb ncgi=0x{change_request.ncgi:x}."
                    )
        except RuntimeError:
            logging.exception(
                "subscribe_mlb_changes: connection idled out, resubscribing..."
            )
        except Exception:
            logging.exception("subscribe_mlb_changes: failed, resubscribing...")
        await asyncio.sleep(5)


async def update_mlb_cio(
    e2_client: sdk.E2Client,
    e2_node_id: str,
    cgi: CellGlobalId,
    neighbor_cgi: CellGlobalId,
    cell_individual_offset: int,
    q_offset: int,
) -> bool:
    """
    Update cell individual offset

    e2_node_id: e2node of the serving cell
    cgi: cgi of serving cell
    neighbor_cgi: cgi of neighboring cell
    cell_individual_offset: cio of neighboring cell

    cell individual offset units
    -- ASN1START
    -- TAG-Q-OFFSETRANGE-START
    Q-OffsetRange ::=                   ENUMERATED {
        dB-24, dB-22, dB-20, dB-18, dB-16, dB-14,
        dB-12, dB-10, dB-8, dB-6, dB-5, dB-4, dB-3,
        dB-2, dB-1, dB0, dB1, dB2, dB3, dB4, dB5,
        dB6, dB8, dB10, dB12, dB14, dB16, dB18,
        dB20, dB22, dB24}

    0 for -24dB
    1 for -22dB
    ...
    15 for 0dB
    16 for 1dB
    ...
    30  for 24dB

    return True if successful
    """

    # The service model does not have a way to specify both (neighbor_cgi, cio).
    # Because we only have one radio per E2 node, instead of using header.cgi to
    # specify serving cell cgi, we're using the e2_node_id to specify serving
    # cell and using the header cgi to specify the neighbor's cell cgi.
    # TODO: update this code when/if service model is updated
    hdr = E2SmRcPreControlHeader(
        control_header_format1=E2SmRcPreControlHeaderFormat1(
            rc_command=RcPreCommand.RC_PRE_COMMAND_SET_PARAMETERS,
            cgi=neighbor_cgi,
        )
    )

    msg = E2SmRcPreControlMessage(
        control_message=E2SmRcPreControlMessageFormat1(
            parameter_type=RanparameterDefItem(
                ran_parameter_id=RanparameterId(value=1),
                ran_parameter_name=RanparameterName(value="ocn_rc"),
                ran_parameter_type=RanparameterType.RANPARAMETER_TYPE_INTEGER,
            ),
            parameter_val=RanparameterValue(value_int=cell_individual_offset),
        )
    )

    try:
        logging.info(f"MLB control: e2:{e2_node_id} hdr:{hdr} msg:{msg}")
        response = await e2_client.control(
            e2_node_id=e2_node_id,
            service_model_name="oran-e2sm-rc-pre",
            service_model_version="v2",
            header=bytes(hdr),
            message=bytes(msg),
        )
        if response is None:
            logging.warning(f"Control ACK is set to `NO_ACK`, skipping...")
            return False

        outcome = E2SmRcPreControlOutcome()
        outcome.parse(response)
        logging.info(f"Update CIO succeeded, outcome: {outcome}")
        return True
    except sdk.exceptions.ClientRuntimeError:
        logging.exception("Update CIO failed")
        return False


async def get_pci_handler(request: web.Request) -> web.Response:
    cells_tracker = request.app["cells_tracker"]
    return web.json_response(cells_tracker.dump())


async def set_pci_multi_handler(request: web.Request) -> web.Response:
    e2_client = request.app["e2_client"]
    cells_tracker = request.app["cells_tracker"]

    items = request.rel_url.query.get("items")

    # expecting a single query param 'items'.
    # semicolon delimited list of set pci parameters
    # each set of pci parameters is ncgi, pci.
    # i.e.: "ncgi,pci;ncgi,pci;..."

    if items is None:
        raise web.HTTPBadRequest(reason="'items' is missing from query params")

    ops = items.split(";")
    args_list = []
    for op in ops:
        params = op.split(",")
        if len(params) != 2:
            raise web.HTTPBadRequest(reason=f"ncgi,pci expected, got '{op}'")

        ncgi, pci = params

        try:
            if ncgi.startswith("0x"):
                ncgi = int(ncgi, 16)
            else:
                ncgi = int(ncgi)
        except ValueError:
            raise web.HTTPBadRequest(
                reason=f"decimal or hex ncgi expected, got '{ncgi}'"
            )

        try:
            cgi = cells_tracker.get_cgi(ncgi)
            e2_node_id = cells_tracker.get_e2_node_id(ncgi)
        except KeyError:
            raise web.HTTPBadRequest(reason=f"ncgi 0x{ncgi:x} is not present")

        try:
            pci = int(pci)
        except ValueError:
            raise web.HTTPBadRequest(reason=f"decimal pci expected, got '{pci}'")

        args_list.append(
            (
                ncgi,
                {
                    "e2_node_id": e2_node_id,
                    "cgi": cgi,
                    "new_pci": pci,
                },
            )
        )

    results = await asyncio.gather(
        *[
            update_pci(
                e2_client=e2_client,
                **args,
            )
            for (_, args) in args_list
        ],
        return_exceptions=True,
    )

    resps = {"success": [], "error": []}
    for result, (ncgi, args) in zip(results, args_list):
        pci = args["new_pci"]
        if isinstance(result, Exception):
            resps["error"].append({"ncgi": hex(ncgi), "pci": pci, "msg": str(result)})
        else:
            # update_pci returns False if failed
            if result:
                resps["success"].append({"ncgi": hex(ncgi), "pci": pci})
            else:
                resps["error"].append(
                    {"ncgi": hex(ncgi), "pci": pci, "msg": "Failed to set new PCI"}
                )

    logging.info(f"set_pci_multi_handler: {str(resps)}")
    return web.json_response(resps)


async def set_cio_multi_handler(request: web.Request) -> web.Response:
    e2_client = request.app["e2_client"]
    cells_tracker = request.app["cells_tracker"]

    items = request.rel_url.query.get("items")

    # expecting a single query param 'items'.
    # semicolon delimited list of set parameters
    # each set of parameters is ncgi, neighbor_ncgi, cio.
    # i.e.: "ncgi,neighbor_ncgi,cio;ncgi,neighbor_ncgi,cio;..."

    if items is None:
        raise web.HTTPBadRequest(reason="'items' is missing from query params")

    ops = items.split(";")
    args_list = []
    for op in ops:
        params = op.split(",")
        if len(params) != 3:
            raise web.HTTPBadRequest(
                reason=f"ncgi,neighbor_ncgi,cio expected, got '{op}'"
            )

        ncgi, neighbor_ncgi, cio = params

        try:
            if ncgi.startswith("0x"):
                ncgi = int(ncgi, 16)
            else:
                ncgi = int(ncgi)
        except ValueError:
            raise web.HTTPBadRequest(
                reason=f"decimal or hex ncgi expected, got '{ncgi}'"
            )

        try:
            cgi = cells_tracker.get_cgi(ncgi)
            e2_node_id = cells_tracker.get_e2_node_id(ncgi)
        except KeyError:
            raise web.HTTPBadRequest(reason=f"ncgi 0x{ncgi:x} is not present")

        try:
            if neighbor_ncgi.startswith("0x"):
                neighbor_ncgi = int(neighbor_ncgi, 16)
            else:
                neighbor_ncgi = int(neighbor_ncgi)
        except ValueError:
            raise web.HTTPBadRequest(
                reason=f"decimal or hex neighbor_ncgi expected, got '{neighbor_ncgi}'"
            )

        try:
            neighbor_cgi = cgiFromNcgi(neighbor_ncgi)
        except KeyError:
            raise web.HTTPBadRequest(
                reason=f"neighbor_ncgi 0x{neighbor_ncgi:x} is not present"
            )

        try:
            cio = int(cio)
        except ValueError:
            raise web.HTTPBadRequest(reason=f"decimal cio expected, got '{cio}'")

        if cio < 0 or cio > 30:
            raise web.HTTPBadRequest(
                reason=f"cio within range 0 <= cio <= 30 expected, got {cio}"
            )

        args_list.append(
            (
                ncgi,
                neighbor_ncgi,
                {
                    "e2_node_id": e2_node_id,
                    "cgi": cgi,
                    "neighbor_cgi": neighbor_cgi,
                    "cell_individual_offset": cio,
                    "q_offset": 15,
                },
            )
        )

    results = await asyncio.gather(
        *[
            update_mlb_cio(
                e2_client=e2_client,
                **args,
            )
            for (_, _, args) in args_list
        ],
        return_exceptions=True,
    )

    resps = {"success": [], "error": []}
    for result, (ncgi, neighbor_ncgi, args) in zip(results, args_list):
        cio = args["cell_individual_offset"]
        if isinstance(result, Exception):
            resps["error"].append(
                {
                    "ncgi": hex(ncgi),
                    "neighbor_ncgi": hex(neighbor_ncgi),
                    "cio": cio,
                    "msg": str(result),
                }
            )
        else:
            # update_mlb_cio returns False if failed
            if result:
                resps["success"].append(
                    {"ncgi": hex(ncgi), "neighbor_ncgi": hex(neighbor_ncgi), "cio": cio}
                )
            else:
                resps["error"].append(
                    {
                        "ncgi": hex(ncgi),
                        "neighbor_ncgi": hex(neighbor_ncgi),
                        "cio": cio,
                        "msg": "Failed to set new cio",
                    }
                )

    logging.info(f"set_cio_multi_handler: {str(resps)}")
    return web.json_response(resps)


def main() -> None:
    e2_client = sdk.E2Client(
        app_id="fb-ah",
        e2t_endpoint=args.e2t_endpoint,
        ca_path=args.ca_path,
        cert_path=args.cert_path,
        key_path=args.key_path,
    )
    sdl_client = sdk.SDLClient(
        topo_endpoint=args.topo_endpoint,
        ca_path=args.ca_path,
        cert_path=args.cert_path,
        key_path=args.key_path,
    )

    cells_tracker = CellsTracker()

    app = web.Application()
    app["e2_client"] = e2_client
    app["cells_tracker"] = cells_tracker
    app.add_routes([web.get("/pci", get_pci_handler)])
    app.add_routes([web.post("/pci", set_pci_multi_handler)])
    app.add_routes([web.post("/cio", set_cio_multi_handler)])

    sdk.run(
        async_main(
            e2_client,
            sdl_client,
            cells_tracker,
            args.pci_disable_control,
            args.mlb_disable_control,
        ),
        args.path,
        app,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Airhop PCI xApp.")
    parser.add_argument("--ca-path", type=str, help="path to CA certificate")
    parser.add_argument("--key-path", type=str, help="path to client private key")
    parser.add_argument("--cert-path", type=str, help="path to client certificate")
    parser.add_argument(
        "--e2t-endpoint", type=str, default="onos-e2t:5150", help="E2T service endpoint"
    )
    parser.add_argument(
        "--eson-endpoint",
        type=str,
        default="localhost:50051",
        help="Airhop eson service endpoint",
    )
    parser.add_argument("--grpc-port", type=int, default=5150, help="grpc Port number")

    group = (
        parser.add_mutually_exclusive_group()
    )  # should use only one method of conflict resolution
    group.add_argument(
        "--pci-maintenance-delay",
        "-m",
        type=float,
        help="Initial delay (s) before monitoring proposed PCI conflict resolution changes, "
        "if not specified do not monitor.",
    )
    parser.add_argument(
        "--pci-maintenance-period",
        type=float,
        default=30,
        help="Period (s) for monitoring proposed PCI conflict resolution changes, "
        "only used if --pci-maintenance-delay is specified. Default=%(default)s",
    )
    group.add_argument(
        "--pci-subscribe-delay",
        "-s",
        type=float,
        help="Initial delay (s) before PCI conflict resolution changes subscription, "
        "if not specified does not subscribe.",
    )

    parser.add_argument(
        "--trigger-periodic-s",
        "-p",
        type=int,
        help="Set trigger for indication messages to be periodic, "
        "with the period specified in seconds. "
        "Default or 0 is sets trigger to be upon change.",
    )

    parser.add_argument(
        "--processing-delay",
        type=float,
        help="Insert artificial delay when processing indication messages (seconds).",
    )

    parser.add_argument(
        "--mlb-update-capacity-period",
        type=float,
        help="Specify the period (seconds) to update capacity value"
        "of cells in eSON. Recommended = 10",
    )

    parser.add_argument(
        "--path", type=str, help="path to the service's JSON configuration file"
    )
    parser.add_argument(
        "--topo-endpoint",
        type=str,
        default="onos-topo:5150",
        help="Topo service endpoint",
    )

    parser.add_argument(
        "--pci-disable-control",
        action="store_true",
        help="Avoid sending any automated PCI E2 control messages",
    )

    parser.add_argument(
        "--mlb-disable-control",
        action="store_true",
        help="Avoid sending any automated MLB (ocn) E2 control messages",
    )

    args = parser.parse_args()
    main()
