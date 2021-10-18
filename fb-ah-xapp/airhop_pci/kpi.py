#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import asyncio
import logging
from typing import Any, Dict, List, Tuple

import betterproto
import onos_ric_sdk_py as sdk
from onos_api.e2t.e2.v1beta1 import (
    Action,
    ActionType,
    SubsequentAction,
    SubsequentActionType,
    TimeToWait,
)
from onos_api.topo import (
    E2Node,
    KpmReportStyle,
)
from onos_e2_sm.e2sm_kpm_v2.v2 import (
    CellObjectId,
    E2SmKpmActionDefinition,
    E2SmKpmActionDefinitionFormat1,
    E2SmKpmEventTriggerDefinition,
    E2SmKpmEventTriggerDefinitionFormat1,
    E2SmKpmIndicationHeader,
    E2SmKpmIndicationMessage,
    GranularityPeriod,
    MeasurementInfoItem,
    MeasurementInfoList,
    MeasurementType,
    MeasurementTypeName,
    RicStyleType,
    SubscriptionId,
)


KPM_SERVICE_MODEL_OID_V2 = "1.3.6.1.4.1.53148.1.2.2.2"


async def subscribe(
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    e2_node_id: str,
    e2_node: E2Node,
    report_style: KpmReportStyle,
    kpi: Dict[Tuple[str, str], Dict[str, int]],
) -> None:
    # Save subscription ID -> cell global ID
    sub_map = {}

    # kpi can return either ID or name, used to map ID to name
    # track per cell in case it's different between cells (unlikely)
    # maps: Cell Global ID -> meas ID -> meas Name
    cell_idname_map: Dict[str, Dict[str, str]] = {}

    # Sort cell IDs to create identical, deterministic subscriptions for demo
    actions = []
    for idx, cell in enumerate(
        sorted(await sdl_client.get_cells(e2_node_id), key=lambda c: c.cell_object_id)
    ):
        idname_map = {}
        meas_info_list = MeasurementInfoList()
        for measurement in report_style.measurements:
            meas_id = measurement.id
            if type(meas_id) is str:
                meas_id = measurement.id.replace("value:", "")
            try:
                idname_map[int(meas_id)] = measurement.name
            except ValueError:
                logging.exception(
                    f'Unable to process measurement.id in "{measurement}"'
                )
            meas_info_list.value.append(
                MeasurementInfoItem(
                    meas_type=MeasurementType(
                        meas_name=MeasurementTypeName(value=measurement.name)
                    )
                )
            )
        cell_idname_map[cell.cell_global_id.value] = idname_map

        sub_map[idx + 1] = cell.cell_global_id.value
        actions.append(
            Action(
                id=idx,
                type=ActionType.ACTION_TYPE_REPORT,
                subsequent_action=SubsequentAction(
                    type=SubsequentActionType.SUBSEQUENT_ACTION_TYPE_CONTINUE,
                    time_to_wait=TimeToWait.TIME_TO_WAIT_ZERO,
                ),
                payload=bytes(
                    E2SmKpmActionDefinition(
                        ric_style_type=RicStyleType(value=report_style.type),
                        action_definition_format1=E2SmKpmActionDefinitionFormat1(
                            cell_obj_id=CellObjectId(value=cell.cell_object_id),
                            meas_info_list=meas_info_list,
                            granul_period=GranularityPeriod(value=1000),
                            subscript_id=SubscriptionId(value=idx + 1),
                        ),
                    )
                ),
            )
        )

    logging.info(f"Subscribing kpm node {e2_node_id}")

    async for (header, message) in e2_client.subscribe(
        e2_node_id=e2_node_id,
        service_model_name="oran-e2sm-kpm",
        service_model_version="v2",
        subscription_id="fb-kpimon_oran-e2sm-kpm_sub",
        trigger=bytes(
            E2SmKpmEventTriggerDefinition(
                event_definition_format1=E2SmKpmEventTriggerDefinitionFormat1(
                    reporting_period=1000
                )
            )
        ),
        actions=actions,
    ):
        logging.debug(f"raw header: {header}")
        logging.debug(f"raw message: {message}")

        if not header or not message:
            logging.warning(
                f"skipping empty indication header/message from '{e2_node_id}'..."
            )
            continue

        ind_header = E2SmKpmIndicationHeader()
        ind_header.parse(header)
        ts = int.from_bytes(
            ind_header.indication_header_format1.collet_start_time.value, "big"
        )

        ind_message = E2SmKpmIndicationMessage()
        ind_message.parse(message)
        subscript_id = ind_message.indication_message_format1.subscript_id.value
        cellid = sub_map[subscript_id]

        logging.debug(f"cellid:{cellid} hdr:{ind_header} msg:{ind_message}")

        # track metrics per cell
        metrics = {}
        msg_cnt_key = ("global", "kpi_ind_message_count")  # key for msg count
        meas_info_list = ind_message.indication_message_format1.meas_info_list.value
        for meas_data_item in ind_message.indication_message_format1.meas_data.value:
            for idx, meas_record_item in enumerate(meas_data_item.meas_record.value):
                _, metric_value = betterproto.which_one_of(
                    meas_record_item, "measurement_record_item"
                )
                if metric_value is None:
                    logging.warning("Got a measurement record item with unset value")
                    continue

                field_name, type_value = betterproto.which_one_of(
                    meas_info_list[idx].meas_type, "measurement_type"
                )

                # e2node may return ID or name of a measurement, lookup name if ID is returned
                if field_name == "meas_id":
                    if cellid not in cell_idname_map:
                        logging.error(
                            f"missing measurement name lookup for cellid {cellid}"
                        )
                        continue
                    if type_value.value not in cell_idname_map[cellid]:
                        logging.error(
                            f"cannot find measurement name for {type_value.value} "
                            f"in {cell_idname_map[cellid]}"
                        )
                        continue
                    metric_name = cell_idname_map[cellid][type_value.value]
                elif field_name == "meas_name":
                    metric_name = type_value.value
                else:
                    logging.warning(
                        f"Got a measurement with unset or unknown type '{field_name}'"
                    )
                    continue

                logging.debug(
                    f"KPI {metric_name}={metric_value}. nodeid={e2_node_id} cellid={cellid} at {ts}"
                )
                metrics[metric_name] = metric_value

        # track metrics per cell id
        kpi[(e2_node_id, cellid)] = metrics

        # increment message counter
        kpi[msg_cnt_key] = kpi.get(msg_cnt_key, 0) + 1


async def track_kpi(
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    e2_node_id: str,
    e2_node: E2Node,
    kpi: Dict[Tuple[str, str], Dict[str, int]],
) -> None:
    """
    kpi = {cid: {metric_name: metric_value, ...}, ...}
    """

    try:
        service_model = next(
            sm
            for oid, sm in e2_node.service_models.items()
            if oid == KPM_SERVICE_MODEL_OID_V2
        )
    except StopIteration:
        return

    subscriptions = []
    for report_style in service_model.ran_functions[0].report_styles:
        subscriptions.append(
            subscribe(e2_client, sdl_client, e2_node_id, e2_node, report_style, kpi)
        )

    await asyncio.gather(*subscriptions)
