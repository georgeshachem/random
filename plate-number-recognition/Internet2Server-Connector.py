import paho.mqtt.client as mqtt
import json
import requests

mqtt_broker_address = "212.98.137.194"
mqtt_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("blacklist_ul")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)

    base_url = "http://10.81.16.113:3000/Detection/create"
    headers = {
        'Content-Type': "application/json"
    }
    json_payload = json.dumps(data)
    r = requests.post(base_url, data=json_payload, headers=headers)
    print("Status Code: " + r.status_code)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("user", "bonjour")
    client.connect(mqtt_broker_address, mqtt_port, 60)
    client.loop_forever()
