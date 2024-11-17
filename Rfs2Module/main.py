# Modified 
# Copyright (C) 2021 Intel Corporation 
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
# Microsoft's Origin File is moved to LICENSES/iot-edge-samples from the project root.

# Origin
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import sys
import asyncio
from six.moves import input

from azure.iot.device.aio import IoTHubModuleClient, IoTHubDeviceClient, ProvisioningDeviceClient

from package.utility import *
from package.basecomnios import *
from package.gsensor import *
from package.rfssensor import *
from package.thresholdcontroller import *
import json
from azure.iot.device import Message

#Test without Azure IoT Edge
isEdge = False


#Model is in public now and it can be searched.
#https://github.com/Azure/iot-plugandplay-models/tree/main/dtmi/terasic/fcc
model_id ="dtmi:Terasic:FCC:DE10_Nano;1" 
useComponent = True

#Global Instances at first to support simulations
control_bridge = None
data_bridge    = None
rfs = RfsSensor(name='rfsSensors',real=False)
thc = ThresholdController(real=False)
msg_origin = os.getenv("MSG_ORIGIN")

# PROPERTY TASKS
async def execute_property_listener(client):
    global isEdge, data_bridge, thc
    if isEdge == False:
        while True :
            patch = await client.receive_twin_desired_properties_patch()  # blocking call
            prop_dict = thc.update_component_property(data_bridge,patch)
            logger.debug(prop_dict)
            await client.patch_twin_reported_properties(prop_dict)
    else:
        async def edge_twin_patch_handler(patch):
            prop_dict = thc.update_component_property(data_bridge,patch)
            logger.debug(prop_dict)
            await client.patch_twin_reported_properties(prop_dict)
        client.on_twin_desired_properties_patch_received = edge_twin_patch_handler


async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )

    provisioning_device_client.provisioning_payload = {"modelId": model_id}
    return await provisioning_device_client.register()

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception(
                "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version)
        print("IoT Hub Client for Python")
        logger.debug('DEBUG ::: Check {}'.format(hostname))
        delay = 10
        lux_threshold = 10
        watchdog_task  = None
        global isEdge, control_bridge, data_bridge, rfs, thc, msg_origin
        
        if "IOTEDGE_IOTHUBHOSTNAME" in os.environ:
            isEdge = True
        else:
            isEdge = False

        if isEdge == True:
            print("Azure IoT Edge with PnP!")
            client = IoTHubModuleClient.create_from_edge_environment(product_info=model_id)
        else:
            switch = os.getenv("IOTHUB_DEVICE_SECURITY_TYPE")
            if switch == "DPS":
                provisioning_host = (
                    os.getenv("IOTHUB_DEVICE_DPS_ENDPOINT")
                    if os.getenv("IOTHUB_DEVICE_DPS_ENDPOINT")
                    else "global.azure-devices-provisioning.net"
                )
                id_scope = os.getenv("IOTHUB_DEVICE_DPS_ID_SCOPE")
                registration_id = os.getenv("IOTHUB_DEVICE_DPS_DEVICE_ID")
                symmetric_key = os.getenv("IOTHUB_DEVICE_DPS_DEVICE_KEY")

                registration_result = await provision_device(
                    provisioning_host, id_scope, registration_id, symmetric_key, model_id
                )

                if registration_result.status == "assigned":
                    print("Device was assigned")
                    print(registration_result.registration_state.assigned_hub)
                    print(registration_result.registration_state.device_id)
                    client = IoTHubDeviceClient.create_from_symmetric_key(
                        symmetric_key=symmetric_key,
                        hostname=registration_result.registration_state.assigned_hub,
                        device_id=registration_result.registration_state.device_id,
                        product_info=model_id,
                    )
                else:
                    raise RuntimeError(
                        "Could not provision device. Aborting Plug and Play device connection."
                    )

            elif switch == "connectionString":
                conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
                print("Connecting using Connection String " + conn_str)
                client = IoTHubDeviceClient.create_from_connection_string(
                    conn_str, product_info=model_id
                )
            else:
                raise RuntimeError(
                    "At least one choice needs to be made for complete functioning of this sample."
                )

        # Connect the client.
        await client.connect()

        if(hostname in 'de10nano'):
            bridges = get_nios_status(hostname)
            if ( bridges[0] is not None ) : 
                logger.debug('DEBUG ::: The FPGA is ready!')
                control_bridge = bridges[0]
                data_bridge = bridges[1]
                rfs = RfsSensor(name='rfsSensors',real=True,offset=0x40100)
                thc = ThresholdController(real=True,bridge=data_bridge,offset=0x40200)
                watchdog_task = asyncio.create_task(watchdog_nios(control_bridge, 1))

        #Send initial values to Azure 
        init_patch= {
            'thresholdProperty': {
                '__t': 'c',
                'lux': { 'min': 0, 'max': 1000}
            },
            "$version": 1
        }
        init_dict=thc.update_component_property(data_bridge,init_patch)
        await client.patch_twin_reported_properties(init_dict)

        # Schedule tasks for listeners
        listener_tasks = asyncio.gather(
            execute_property_listener(client)
        )

        async def send_telemetry():
            print(f'Sending lux telemetry from the provisioned device every {delay} seconds')
            while True:
                try :
                    rfs_data = rfs.get_telemetries(data_bridge)
                    lux_value = rfs_data.get('lux')
                    if(lux_value >= lux_threshold):
                        msg = rfs.create_component_telemetry(generate_lux_message(lux_value, msg_origin))
                        logger.debug(f'Sent message: {str(msg)}')
                        await client.send_message(msg)
                
                finally :
                    await asyncio.sleep(delay)
        send_telemetry_task = asyncio.create_task(send_telemetry())

        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    #selection = input("Press Q to quit\n")
                    selection = input()
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(delay)
        # Run the stdin listener in the event loop
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)
        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel send_telemetry
        send_telemetry_task.cancel()

        # Cancel listening
        listener_tasks.add_done_callback(lambda r: r.exception())
        listener_tasks.cancel()

        if(watchdog_task is not None) :
            watchdog_task.cancel()

        # Finally, disconnect
        await client.disconnect()

    except Exception as e:
        print("Unexpected error %s " % e)
        raise

def generate_lux_message(lux_value, msg_origin):
    payload = {
           "notify": "true",
           "lux": lux_value,
           "from": msg_origin 
        }
    
    print(payload)

    # Create Message object
    message = Message(str(payload))  # Payload must be serialized (e.g., as a JSON string)
    message.content_type="application/JSON"
    message.content_encoding="UTF-8"

    return message


if __name__ == "__main__":
    # If using Python 3.7 or above, you can use following code instead:
    asyncio.run(main(),debug=True)
