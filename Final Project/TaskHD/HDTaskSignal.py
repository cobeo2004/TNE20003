import paho.mqtt.client as mqtt
import time
import random
import json

broker = 'rule28.i4t.swin.edu.au'
user_information = {
    "client_identifier": "Publisher",
    "username": "103819212",
    "password": "103819212"
}
will_turn_on = False

topic = [("public/#", 0), ("public/103819212/fan/control", 0)]
publish_topic = "public/103819212/fan/status"


def connect_mqtt() -> mqtt.Client:
    global broker, user_information, topic

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!. Code: " + str(rc))

        else:
            print("Failed to connect, return code " + rc)
    client = mqtt.Client(user_information["client_identifier"])
    client.username_pw_set(
        user_information["username"], user_information["password"])
    client.on_connect = on_connect
    client.connect(broker)
    return client


def __showLog(client: mqtt.Client) -> None:
    def on_log(client, userdata, level, buf):
        print(f"Logs: {str(buf)}")
    client.on_log = on_log


def subscribe(client: mqtt.Client) -> None:
    def on_message(client, userdata, msg):
        global will_turn_on
        print("\n\n===================SUBSCRIBE======================")
        __showLog(client)
        print(f"Topic: {msg.topic}")
        print(f"Payload: {msg.payload.decode('utf-8')}")
        print(f"QoS: {msg.qos}")
        print(f"Retain: {msg.retain}")
        print("===================SUBSCRIBE======================\n\n")
        if msg.payload.decode("utf-8").lower() == "fan on":
            will_turn_on = True
        if msg.payload.decode("utf8").lower() == "fan off":
            will_turn_on = False

    client.on_message = on_message
    client.subscribe(topic)


def publish(client: mqtt.Client) -> None:
    global topic, user_information
    message_count = 1
    fan_temp = 20

    def on_publish(client, userdata, mid):
        print(f"Payload published: {str(mid)}")
    client.on_publish = on_publish
    while True:
        __showLog(client)
        if will_turn_on:
            fan_temp -= 1
            info = {
                "temperature": fan_temp,
                "status": "on"
            }
        if not will_turn_on:
            fan_temp += 1
            info = {
                "temperature": fan_temp,
                "status": "off"
            }
        time.sleep(2)
        res = client.publish(publish_topic, json.dumps(info), 0)
        status = res[0]
        if status == 0:
            print(f"Send fan status to {topic}")
        else:
            print(f"Failed to send message to {topic}")


def __disconnect(client: mqtt.Client):
    def on_disconnect(client, userdata, rc):
        print(f"Disconnected from server with reason: {str(rc)}")
    client.on_disconnect = on_disconnect
    client.disconnect()


def main() -> None:
    client = connect_mqtt()
    try:
        subscribe(client)
        client.loop_start()
        publish(client)
    except KeyboardInterrupt:
        __disconnect(client)
        client.loop_stop()


if __name__ == "__main__":
    main()
