import paho.mqtt.client as mqtt
import time

broker = 'rule28.i4t.swin.edu.au'
user_information = {
    "client_identifier": "Simon-Subscriber",
    "username": "103819212",
    "password": "103819212",
}
topic = [("103819212/my_private_topic", 0), ("public/#", 0)]


def connect_mqtt() -> mqtt.Client:
    global broker, user_information, topic

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!. Code " + str(rc))
        else:
            print("Failed to connect, return code " + str(rc))
    client = mqtt.Client(user_information["client_identifier"])
    client.username_pw_set(
        user_information["username"], user_information["password"])
    client.on_connect = on_connect
    client.connect(broker)
    return client


def __showLog(client: mqtt.Client) -> None:
    def on_log(client, usrData, level, buf):
        print(f"Logs: {buf}")
    client.on_log = on_log


def subscribe(client: mqtt.Client) -> None:
    global topic

    def on_message(client, userdata, msg):
        print("\n\n=========================================")
        __showLog(client)
        print(f"Topic: {msg.topic}")
        print(f"Payload: {msg.payload.decode('utf-8')}")
        print(f"QoS: {msg.qos}")
        print(f"Retain: {msg.retain}")
        print("=========================================\n\n")
    client.on_message = on_message
    client.subscribe(topic)


def main() -> None:
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    main()
