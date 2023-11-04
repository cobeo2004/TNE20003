import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt
from random import randint


class DatHoangMQTTGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("DatHoang EMQTTX")
        self.configure(bg="white")
        self.mainUI()
        self.listPublishTopics = []
        self.listTopicSubscribe = []
        self.resizable(False, False)
        self.mqtt = mqtt.Client(
            f"DatHoangDTaskEMQTTX-BOT{randint(1, 696969)}")

    def mainUI(self):
        # Broker Connection
        self.broker_frame = ttk.LabelFrame(
            self, text="Connection", padding=(10, 5))
        self.broker_frame.grid(
            row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)

        self.host_label = ttk.Label(
            self.broker_frame, text="Host:", background="white")
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
        self.user_name_entry.insert(0, "104194774")
        self.user_password_label = ttk.Label(
            self.broker_frame, text="Password")
        self.user_password_label.grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.user_pwd_entry = ttk.Entry(self.broker_frame)
        self.user_pwd_entry.grid(
            row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
        self.user_pwd_entry.insert(0, "104194774")
        self.connect_btn = ttk.Button(
            self.broker_frame, text="Connect", command=self._connect_broker)
        self.connect_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Publisher
        self.pub_frame = ttk.LabelFrame(
            self, text="Publisher", padding=(10, 5))
        self.pub_frame.grid(row=1, column=0, sticky=tk.W +
                            tk.E + tk.N + tk.S, padx=10, pady=10)

        self.topic_label = ttk.Label(
            self.pub_frame, text="Topic (seperate by comma):")
        self.topic_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.topic_entry = ttk.Entry(self.pub_frame)
        self.topic_entry.grid(row=0, column=1, sticky=tk.W +
                              tk.E + tk.N + tk.S, padx=5, pady=5)

        self.message_label = ttk.Label(
            self.pub_frame, text="Message:")
        self.message_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.entryMessage = ttk.Entry(self.pub_frame)
        self.entryMessage.grid(
            row=1, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

        self.publish_btn = ttk.Button(
            self.pub_frame, text="Publish", command=self._publish)
        self.publish_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Subscriber
        self.sub_frame = ttk.LabelFrame(
            self, text="Subscriber", padding=(10, 5))
        self.sub_frame.grid(row=2, column=0, sticky=tk.W +
                            tk.E + tk.N + tk.S, padx=10, pady=10)

        self.sub_topic_label = ttk.Label(
            self.sub_frame, text="Topic (seperate by comma):")
        self.sub_topic_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.sub_topic_entry = ttk.Entry(self.sub_frame)
        self.sub_topic_entry.grid(
            row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
        self.sub_topic_entry.insert(0, "public/104194774/#")

        self.subscribe_btn = ttk.Button(
            self.sub_frame, text="Subscribe", command=self._subscribe)
        self.subscribe_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.sub_message_label = ttk.Label(
            self.sub_frame, text="Messages:")
        self.sub_message_label.grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.textSubMessage = tk.Listbox(self.sub_frame)
        self.textSubMessage.grid(
            row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

    def _connect_broker(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                messagebox.showinfo("Successful",
                                    "Successfully connected to server, Code: " + str(rc))

        host = self.host_entry.get()
        port = int(self.port_entry.get())
        if not host and not port:
            messagebox.showerror("Error", "ERROR: Must Have Host and Port")
        else:
            if(self.user_name_entry.get() != "" and self.user_pwd_entry.get() != ""):
                self.mqtt.username_pw_set(
                    self.user_name_entry.get(), self.user_pwd_entry.get())
            self.mqtt.on_connect = on_connect
            try:
                self.mqtt.connect(host, port, 60)
                self.mqtt.loop_start()
            except TimeoutError and ConnectionRefusedError as conn_err:
                messagebox.showerror(
                    "Error", f"Failed to connect to server: {conn_err}")

    def _publish(self):
        def on_publish(client, userdata, mid):
            for topic in self.listPublishTopics:
                messagebox.showinfo(
                    "Success", f"Published message to: {topic}")

        self.mqtt.on_publish = on_publish

        self.listPublishTopics = self.topic_entry.get().split(",")
        if len(self.listPublishTopics) == 0:
            messagebox.showerror("Error", "Must have a topic to publish")
        else:
            message = self.entryMessage.get()
            print(f"Message: {message}")
            if not message:
                messagebox.showerror(
                    "Error", "Must have a message to publish")
            else:
                for topic in self.listPublishTopics:
                    self.mqtt.publish(topic, message, 0)

    def _subscribe(self):
        def on_message(client, userdata, msg):
            self.textSubMessage.insert(tk.END,
                                       msg.topic + ": " + msg.payload.decode("utf-8") + f"({msg.retain})")
        if not self.sub_topic_entry.get():
            messagebox.showerror(
                "Error", "Please put a topic to subscribe")
        else:
            for topic in self.sub_topic_entry.get().split(", "):
                self.listTopicSubscribe.append((topic, 0))

            self.mqtt.subscribe(self.listTopicSubscribe)
            messagebox.showinfo(
                "Subscribed", f"Subscribed to {(topic for topic in self.listTopicSubscribe)}")
            self.mqtt.on_message = on_message


if __name__ == "__main__":
    app = DatHoangMQTTGui()
    app.mainloop()
