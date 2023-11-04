import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt
from random import randint
import json


class SimonMQTTGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simon EMQTTX")
        self.geometry("430x870")
        self.publish_topics = []
        self.default_sub_topic = [("public/#", 0)]
        self.subscirbe_topics = []
        self.client_name = ""
        self.mqtt_client = None
        self.is_connected: bool = False
        self.resizable(False, False)
        # GUI Widgets
        self.setup_ui()

    def setup_ui(self):
        # Broker Connection
        self.broker_frame = ttk.LabelFrame(
            self, text="Broker Connection", padding=(10, 5))
        self.broker_frame.grid(
            row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)

        self.host_label = ttk.Label(self.broker_frame, text="Host:")
        self.host_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.host_entry = ttk.Entry(self.broker_frame)
        self.host_entry.grid(row=0, column=1, sticky=tk.W +
                             tk.E + tk.N + tk.S, padx=5, pady=5)
        self.host_entry.insert(0, "rule28.i4t.swin.edu.au")

        self.port_label = ttk.Label(self.broker_frame, text="Port:")
        self.port_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.port_entry = ttk.Entry(self.broker_frame)
        self.port_entry.grid(row=1, column=1, sticky=tk.W +
                             tk.E + tk.N + tk.S, padx=5, pady=5)
        self.port_entry.insert(0, "1883")

        self.user_name_label = ttk.Label(self.broker_frame, text="Username")
        self.user_name_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.user_name_entry = ttk.Entry(self.broker_frame)
        self.user_name_entry.grid(
            row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
        self.user_name_entry.insert(0, "103819212")
        self.user_password_label = ttk.Label(
            self.broker_frame, text="Password")
        self.user_password_label.grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.user_pwd_entry = ttk.Entry(self.broker_frame)
        self.user_pwd_entry.grid(
            row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
        self.user_pwd_entry.insert(0, "103819212")

        self.client_label = ttk.Label(self.broker_frame, text="Client Name")
        self.client_label.grid(
            row=4, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
        self.client_entry = ttk.Entry(self.broker_frame)
        self.client_entry.grid(row=4, column=1, padx=5, pady=5)

        self.connect_btn = ttk.Button(
            self.broker_frame, text="Connect", command=self.connect_broker)
        self.connect_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Publisher
        self.pub_frame = ttk.LabelFrame(
            self, text="Publisher", padding=(10, 5))
        self.pub_frame.grid(row=1, column=0, sticky=tk.W +
                            tk.E + tk.N + tk.S, padx=10, pady=10)

        self.topic_label = ttk.Label(
            self.pub_frame, text="Topic (comma seperated):")
        self.topic_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.topic_entry = ttk.Entry(self.pub_frame)
        self.topic_entry.grid(row=0, column=1, sticky=tk.W +
                              tk.E + tk.N + tk.S, padx=5, pady=5)

        self.message_label = ttk.Label(
            self.pub_frame, text="Message:")
        self.message_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.message_entry = ttk.Entry(self.pub_frame)
        self.message_entry.grid(
            row=1, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

        self.publish_btn = ttk.Button(
            self.pub_frame, text="Publish", command=self.publish_message)
        self.publish_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Subscriber
        self.sub_frame = ttk.LabelFrame(
            self, text="Subscriber", padding=(10, 5))
        self.sub_frame.grid(row=2, column=0, sticky=tk.W +
                            tk.E + tk.N + tk.S, padx=10, pady=10)

        self.sub_topic_label = ttk.Label(
            self.sub_frame, text="Topic (Comma seperated):")
        self.sub_topic_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.sub_topic_entry = ttk.Entry(self.sub_frame)
        self.sub_topic_entry.grid(
            row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
        self.sub_topic_entry.insert(0, "public/103819212/#")

        self.subscribe_btn = ttk.Button(
            self.sub_frame, text="Subscribe", command=self.subscribe_topic)
        self.subscribe_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.sub_message_label = ttk.Label(
            self.sub_frame, text="Received Messages:")
        self.sub_message_label.grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.sub_message_text = tk.Listbox(self.sub_frame)
        self.sub_message_text.grid(
            row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

        self.is_connected_frame = ttk.LabelFrame(
            self, text="Connect status", padding=(10, 5))
        self.is_connected_frame.grid(
            row=3, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)
        self.is_connected_frame.columnconfigure(0, weight=1)
        self.connect_status = tk.Label(self.is_connected_frame)
        self.connect_status.config(
            text="Not Connected", bg="gray51", foreground="red")
        self.connect_status.grid(
            row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

    def _connect_status(self, is_connect: bool):
        if is_connect:
            self.connect_status.config(
                text="Connected", bg="gray51", foreground="green")
        else:
            self.connect_status.config(
                text="Not Connected", bg="gray51", foreground="red")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            messagebox.showinfo("Successful",
                                "Successfully connected to server, Code: " + str(rc))
            self._connect_status(True)
            self.is_connected = True
        else:
            self.is_connected = False

    def connect_broker(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        client = self.client_entry.get()
        if not host and not port:
            messagebox.showerror("Error", "Please input host and port")
        elif not client:
            messagebox.showerror("Error", "Please input client name")
        else:
            self.client_name = f"SimonEMQTTX-center-{client}"
            self.mqtt_client = mqtt.Client(self.client_name)
            if(self.user_name_entry.get() != "" and self.user_pwd_entry.get() != ""):
                self.mqtt_client.username_pw_set(
                    self.user_name_entry.get(), self.user_pwd_entry.get())
            self.mqtt_client.on_connect = self._on_connect
            try:
                self.mqtt_client.connect(host, port, 60)
                self.mqtt_client.loop_start()  # Start the loop to process incoming messages
            except ConnectionRefusedError and TimeoutError as conn_err:
                messagebox.showerror("Error", f"Connection error: {conn_err}")
                self.is_connected = False

    def _on_publish(self, client, userdata, mid):
        pass

    def publish_message(self):
        if self.is_connected == False:
            messagebox.showerror("Error, You have to connect to an MQTT first")
        else:
            self.mqtt_client.on_publish = self._on_publish
            self.publish_topics = self.topic_entry.get().split(",")
            if len(self.publish_topics) == 0:
                messagebox.showerror("Error", "Please put a topic to publish")
            else:
                message = self.message_entry.get()
                print(f"Message: {message}")
                if not message:
                    messagebox.showerror("Error", "Please put a message")
                else:
                    for topic in self.publish_topics:
                        result = self.mqtt_client.publish(topic, message, 0)
                        if result[0] == 0:
                            messagebox.showinfo(
                                "Success", f"Published message into topic {topic}")
                        else:
                            messagebox.showerror(
                                "Failed", f"Failed to publish topic to {topic}")

    def _on_message(self, client, userdata, msg):
        self.sub_message_text.insert(tk.END,
                                     msg.topic + ": " + msg.payload.decode("utf-8") + f"({msg.retain})")
        if msg.topic == "public/103819212/fan/status":
            fan_temperature = json.loads(
                msg.payload.decode("utf-8"))["temperature"]
            fan_status = json.loads(msg.payload.decode("utf-8"))["status"]

            if fan_temperature > 30 and fan_status != "on":
                result = self.mqtt_client.publish(
                    "public/103819212/fan/control", "FAN ON", 0)
                if result[0] == 0:
                    messagebox.showinfo(
                        "Success", "Fan has been turned on")
                else:
                    messagebox.showerror("Failed", "Could not send request")
            if fan_temperature < 20 and fan_status == "on":
                result = self.mqtt_client.publish(
                    "public/103819212/fan/control", "FAN OFF", 0)
                if result[0] == 0:
                    messagebox.showinfo("Success", "Fan is turned off")
                else:
                    messagebox.showerror(
                        "Failed", "Can not send the request")

        if msg.payload.decode("utf-8").lower() == "fire":
            messagebox.showwarning(
                "Warning", "The broker is having problem thus disconnect all of the clients!")
            self._connect_status(False)
            self.is_connected = False
            self.mqtt_client.disconnect()

    def subscribe_topic(self):

        if self.is_connected == False:
            messagebox.showerror("Error, You have to connect to an MQTT first")
        else:
            self.mqtt_client.on_message = self._on_message
            if not self.sub_topic_entry.get():
                messagebox.showerror(
                    "Error", "Please put a topic to subscribe")
            else:
                self.mqtt_client.subscribe(self.default_sub_topic)
                messagebox.showinfo(
                    "Subscribe", f"The global public topic has been subscribed!")
                for topic in self.sub_topic_entry.get().split(", "):
                    self.subscirbe_topics.append((topic, 0))

                self.mqtt_client.subscribe(self.subscirbe_topics)
                messagebox.showinfo(
                    "Subscribed", f"Subscribed to {[topic for topic in self.subscirbe_topics]}")
                self.mqtt_client.on_message = self._on_message
            # self.mqtt_client.subscribe(self.default_sub_topic)
            # messagebox.showinfo("Subscribe", "Start Guarding")


if __name__ == "__main__":
    app = SimonMQTTGui()
    app.mainloop()
