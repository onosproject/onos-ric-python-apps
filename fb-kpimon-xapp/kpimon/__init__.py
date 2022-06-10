#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright 2004-present Facebook. All Rights Reserved.
# SPDX-FileCopyrightText: 2019-present Open Networking Foundation <info@opennetworking.org>
#
# SPDX-License-Identifier: Apache-2.0

import asyncio
import logging
from typing import Any, Dict

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
    ServiceModelInfo,
)
from onos_e2_sm.e2smkpmv2.v2 import (
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

from .metrics import CUSTOM_COLLECTOR


KPM_SERVICE_MODEL_OID_V2 = "1.3.6.1.4.1.53148.1.2.2.2"


async def subscribe(
    app_config: Dict[str, Any],
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    e2_node_id: str,
    e2_node: E2Node,
    report_style: KpmReportStyle,
) -> None:
    # Save subscription ID -> cell global ID for Prometheus metric labeling
    sub_map = {}

    # Sort cell IDs to create identical, deterministic subscriptions for demo
    actions = []
    for idx, cell in enumerate(
        sorted(await sdl_client.get_cells(e2_node_id), key=lambda c: c.cell_object_id)
    ):
        meas_info_list = MeasurementInfoList()
        for measurement in report_style.measurements:
            meas_id = measurement.id
            if type(meas_id) is str:
                meas_id = int(measurement.id.replace("value:", ""))
            CUSTOM_COLLECTOR.register(meas_id, measurement.name)
            meas_info_list.value.append(
                MeasurementInfoItem(
                    meas_type=MeasurementType(
                        meas_name=MeasurementTypeName(value=measurement.name)
                    )
                )
            )

        sub_map[idx + 1] = cell.cell_global_id.value
        action_def = E2SmKpmActionDefinition(
            ric_style_type=RicStyleType(value=report_style.type),
        )
        action_def.action_definition_formats.action_definition_format1=E2SmKpmActionDefinitionFormat1(
            cell_obj_id=CellObjectId(value=cell.cell_object_id),
            meas_info_list=meas_info_list,
            granul_period=GranularityPeriod(
                value=app_config["report_period"]["granularity"]
            ),
            subscript_id=SubscriptionId(value=idx + 1),
        )
        action = Action(
            id=idx,
            type=ActionType.ACTION_TYPE_REPORT,
            subsequent_action=SubsequentAction(
                type=SubsequentActionType.SUBSEQUENT_ACTION_TYPE_CONTINUE,
                time_to_wait=TimeToWait.TIME_TO_WAIT_ZERO,
            ),
            payload=bytes(
                action_def
            ),
        )
        actions.append(
            action
        )

    if not actions:
        logging.warning(f"No cells found for E2 node with ID: '{e2_node_id}'")
        return

    trigger_def = E2SmKpmEventTriggerDefinition()
    trigger_def.event_definition_formats.event_definition_format1=E2SmKpmEventTriggerDefinitionFormat1(
        reporting_period=app_config["report_period"]["interval"]
    )

    async for (header, message) in e2_client.subscribe(
        e2_node_id=e2_node_id,
        service_model_name="oran-e2sm-kpm",
        service_model_version="v2",
        subscription_id=f"fb-kpimon_oran-e2sm-kpm_sub_{e2_node_id}",
        trigger=bytes(trigger_def),
        actions=actions,
    ):
        logging.debug(f"raw header: {header}")
        logging.debug(f"raw message: {message}")

        ind_header = E2SmKpmIndicationHeader()
        ind_header.parse(header)
        ts = int.from_bytes(
            ind_header.indication_header_formats.indication_header_format1.collet_start_time.value, "big"
        )

        ind_message = E2SmKpmIndicationMessage()
        ind_message.parse(message)
        subscript_id = ind_message.indication_message_formats.indication_message_format1.subscript_id.value

        meas_info_list = ind_message.indication_message_formats.indication_message_format1.meas_info_list.value
        for meas_data_item in ind_message.indication_message_formats.indication_message_format1.meas_data.value:
            for idx, meas_record_item in enumerate(meas_data_item.meas_record.value):
                _, metric_value = betterproto.which_one_of(
                    meas_record_item, "measurement_record_item"
                )
                if metric_value is None:
                    logging.warning("Got a measurement record item with unset value")
                    continue

                _, type_value = betterproto.which_one_of(
                    meas_info_list[idx].meas_type, "measurement_type"
                )
                if type_value is None:
                    logging.warning("Got a measurement with unset type")
                    continue

                metric_family = CUSTOM_COLLECTOR.metrics.get(type_value.value)
                if metric_family is None:
                    logging.warning(f"No metric family found for '{type_value.value}'")
                    continue

                cellid = sub_map[subscript_id]
                logging.info(
                    f"{metric_family.name}{{nodeid={e2_node_id}, cellid={cellid}}} {metric_value} {ts}"
                )
                metric_family.add_metric(
                    labels=[e2_node_id, cellid],
                    value=metric_value,
                    timestamp=ts,
                )


async def run(
    app_config: Dict[str, Any],
    e2_client: sdk.E2Client,
    sdl_client: sdk.SDLClient,
    e2_node_id: str,
    e2_node: E2Node,
    service_model: ServiceModelInfo,
) -> None:
    subscriptions = []
    for report_style in service_model.ran_functions[0].report_styles:
        subscriptions.append(
            subscribe(
                app_config, e2_client, sdl_client, e2_node_id, e2_node, report_style
            )
        )

    await asyncio.gather(*subscriptions)
