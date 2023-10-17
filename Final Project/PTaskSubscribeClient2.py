import paho.mqtt.client as mqtt
import time

broker = 'rule28.i4t.swin.edu.au'
user_information = {
    "client_identifier": "Subscriber",
    "username": "103819212",
    "password": "103819212",
    "message": "HowdyHeyHowItsGoinMate?"
}
topic = [("103819212/my_private_topic", 0), ("public/#", 0)]


def connect_mqtt() -> mqtt.Client:
    global broker, user_information

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code " + rc)
    client = mqtt.Client(user_information["client_identifier"])
    client.username_pw_set(
        user_information["username"], user_information["password"])
    client.on_connect = on_connect
    client.connect(broker)
    return client


def subscribe(client: mqtt) -> None:
    global topic

    def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from {msg.topic}")

    client.subscribe(topic)
    client.on_message = on_message


def main() -> None:
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    main()
