import paho.mqtt.client as mqtt
from flask import Flask, request

app = Flask(__name__)

mqtt_broker_address = "212.98.137.194"
mqtt_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


@app.route("/send-mqtt", methods=["POST"])
def send_mqtt():
    client.publish("aloha", payload='{"bonjour":2}')
    return "Ok"


if __name__ == "__main__":
    client = mqtt.Client()
    client.username_pw_set("user", "bonjour")
    client.on_connect = on_connect
    client.connect(mqtt_broker_address, mqtt_port, 60)
    app.run(debug=True)
    client.loop_forever()
