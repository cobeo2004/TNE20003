import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt
from random import randint
import json


class MQTTGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simon EMQTTX")
        self.geometry("430x850")
        self.publish_topics = []
        self.subscirbe_topics = []
        self.mqtt_client = mqtt.Client(f"simonEMQTTX-{randint(100, 12892312)}")
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
        self.connect_btn = ttk.Button(
            self.broker_frame, text="Connect", command=self.connect_broker)
        self.connect_btn.grid(row=4, column=0, columnspan=2, pady=10)

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

    def connect_broker(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                messagebox.showinfo("Successful",
                                    "Successfully connected to server, Code: " + str(rc))
                self._connect_status(True)
                self.is_connected = True
            if rc == 1:
                messagebox.showerror("Failed",
                                     "Failed to connect to server, code: " + str(rc))
                self._connect_status(False)
                self.is_connected = False

        host = self.host_entry.get()
        port = int(self.port_entry.get())
        if not host and not port:
            messagebox.showerror("Error", "Please input host and port")
        else:
            if(self.user_name_entry.get() != "" and self.user_pwd_entry.get() != ""):
                self.mqtt_client.username_pw_set(
                    self.user_name_entry.get(), self.user_pwd_entry.get())
            self.mqtt_client.on_connect = on_connect
            self.mqtt_client.connect(host, port, 60)
            self.mqtt_client.loop_start()  # Start the loop to process incoming messages

    def publish_message(self):
        def on_publish(client, userdata, mid):
            for topic in self.publish_topics:
                messagebox.showinfo(
                    "Success", f"Published message {mid}: {topic}")

        if self.is_connected == False:
            messagebox.showerror("Error, You have to connect to an MQTT first")
        else:
            self.mqtt_client.on_publish = on_publish

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
                        self.mqtt_client.publish(topic, message, 0)

    def subscribe_topic(self):
        def on_message(client, userdata, msg):
            self.sub_message_text.insert(tk.END,
                                         msg.topic + ": " + msg.payload.decode("utf-8") + f"({msg.retain})")
            if msg.topic == "public/103819212/signal/status":
                signal_json = json.loads(msg.payload.decode("utf-8"))
                if str.lower(signal_json["status"]) == "danger" and str.lower(signal_json["trip-arm"]) == "de-arm":
                    will_raise = messagebox.askyesno("Alert", "Do you want to raise trip arm for signal " +
                                                     signal_json["signal"] + " status " + signal_json["status"])
                    if will_raise:
                        payload_raise = {
                            "signal": signal_json["signal"],
                            "status": signal_json["status"],
                            "trip-arm": "arm"
                        }
                        self.mqtt_client.publish(
                            "public/103819212/signal/status", json.dumps(payload_raise))
                        messagebox.showinfo(
                            "Success", "Trip arm of signal " + signal_json["signal"] + " has been raised")
                    else:
                        messagebox.showwarning("Warning",
                                               "This will result in train could pass at signal " + signal_json["signal"] + " without any safeworkings!")
                if str.lower(signal_json["status"]) != "danger" and str.lower(signal_json["trip-arm"]) == "arm":
                    will_lower = messagebox.askyesno("Alert", "Do you want to lower trip arm for signal " +
                                                     signal_json["signal"] + " status " + signal_json["status"])
                    if will_lower:
                        payload_lower = {
                            "signal": signal_json["signal"],
                            "status": signal_json["status"],
                            "trip-arm": "de-arm"
                        }
                        self.mqtt_client.publish(
                            "public/103819212/signal/status", json.dumps(payload_lower))
                        messagebox.showinfo(
                            "Success", "Trip arm of signal " + signal_json["signal"] + " has been lowered")
                    else:
                        messagebox.showwarning("Warning",
                                               "This will result in train could not pass at signal " + signal_json["signal"])
        if self.is_connected == False:
            messagebox.showerror("Error, You have to connect to an MQTT first")
        else:
            if not self.sub_topic_entry.get():
                messagebox.showerror(
                    "Error", "Please put a topic to subscribe")
            else:
                for topic in self.sub_topic_entry.get().split(", "):
                    self.subscirbe_topics.append((topic, 0))

                self.mqtt_client.subscribe(self.subscirbe_topics)
                messagebox.showinfo(
                    "Subscribed", f"Subscribed to {[topic for topic in self.subscirbe_topics]}")
                self.mqtt_client.on_message = on_message


if __name__ == "__main__":
    app = MQTTGui()
    app.mainloop()
