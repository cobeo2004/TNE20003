import paho.mqtt.client as mqtt
import time
import random

broker = 'rule28.i4t.swin.edu.au'
user_information = {
    "client_identifier": "Publisher",
    "username": "103819212",
    "password": "103819212",
    "message": ["haha", "hihi", "huhu", "hohe", "heko", "huha", "halal", "HSP", "erik", "ten", "hafg"]
}
topic = "103819212/my_private_topic"


def connect_mqtt() -> mqtt.Client:
    global broker, user_information

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


def publish(client: mqtt.Client) -> None:
    global topic, user_information
    message_count = 1

    def on_publish(client, userdata, mid):
        print(f"Payload published: {str(mid)}")
    client.on_publish = on_publish
    while True:
        __showLog(client)
        time.sleep(1)
        message = f"Messages: {message_count}"
        res = client.publish(topic, random.choice(
            user_information["message"]), 0)
        status = res[0]
        if status == 0:
            print(f"Send {message} to {topic}")
        else:
            print(f"Failed to send message to {topic}")
        message_count += 1
        if message_count > 10:
            break
    __disconnect(client)


def __disconnect(client: mqtt.Client):
    def on_disconnect(client, userdata, rc):
        print(f"Disconnected from server with reason: {str(rc)}")
    client.on_disconnect = on_disconnect
    client.disconnect()


def main() -> None:
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == "__main__":
    main()
