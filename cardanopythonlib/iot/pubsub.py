# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io, mqtt, auth
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4
import json
from datetime import datetime
# from node_lib import IOT

# Load files and config parameters
working_dir = "/home/cardanodatos/git/cnft-python/"

with open('./cardanopythonlib/config/cardano_config.json') as file:
    params=json.load(file)

endpoint = params['AWS_IOT']['endpoint']
# port = params['AWS_IOT']['port']
port = 8883
cert = params['AWS_IOT']['cert']
key = params['AWS_IOT']['key']
root_ca = params['AWS_IOT']['root-ca']
verbosity = params['AWS_IOT']['verbosity']['NoLogs']
signing_region = params['AWS_IOT']['signing_region']
topic = params['AWS_IOT']['topic']
client_id = "test-" + str(uuid4())

io.init_logging(getattr(io.LogLevel, verbosity), 'stderr')

received_count = 0
received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))

# Callback when the subscribed topic receives a message
obj = []
def on_message_received(topic, payload): 
    messages = payload.decode('utf-8')
    messages = json.loads(messages)
    try:
        if not 'client_id' in messages:
            # Build array depending on the number of messages to be received (Number is set by the seq identifier in the json file)
            obj.append(messages)
            nowTimeStamp = datetime.now()
            print("Received message from topic '{}' : '{}' : {}".format(nowTimeStamp, topic, obj))
            # Waits until the object lenght is equal to the sequence number in the message 
            if len(obj) == obj[0]['seq']:
                # iot = IOT(working_dir)
                # result_json = iot.message_treatment(obj,client_id)
                result_json = "I am treating the message"
                # result_json = cw.result_treatment(obj,client_id)
                # q.put(result_json)
                # message = q.get()
                message = result_json
                print('###########################')
                print("Publishing message to topic '{}': {}".format(topic, message))
                print('###########################')
                message_json = json.dumps(message)
                mqtt_connection.publish(
                    topic=topic,
                    payload=message_json,
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                time.sleep(1)
    except: 
        if obj:
            print("Message without seq param, no command executed {}".format(obj.pop(0)))
        else: 
            print("No message received. Object empty")
    
if __name__ == '__main__':
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    proxy_options = None
    # if (args.proxy_host):
    #     proxy_options = http.HttpProxyOptions(host_name=args.proxy_host, port=args.proxy_port)

    credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)
    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        endpoint=endpoint,
        client_bootstrap=client_bootstrap,
        region=signing_region,
        credentials_provider=credentials_provider,
        http_proxy_options=proxy_options,
        ca_filepath=root_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=30)

    # print("Connecting to {} with client ID '{}'...".format(
    #     endpoint, client_id))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Subscribe
    # print("Subscribing to topic '{}'...".format(topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
     
    subscribe_result = subscribe_future.result()
    # print("Subscribed with {}".format(str(subscribe_result['qos'])))
    print("Subscribed!")

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    # if args.count != 0 and not received_all_event.is_set():
    #     print("Waiting for all messages to be received...")

    # Prevents the execution of the code below (Disconnet) while received_all_event flag is False
    received_all_event.wait()

    print("{} message(s) received.".format(received_count))

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")