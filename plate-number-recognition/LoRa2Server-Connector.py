import paho.mqtt.client as mqtt
import json
import base64
import requests

mqtt_broker_address = "212.98.137.194"
mqtt_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("application/14/device/2aa4de420479d196/rx")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)

    if 'data' not in data.keys():
        return 0

    data = base64.b64decode(data['data']).decode('windows-1252').split(',')[0].split('-')

    base_url = "http://10.81.16.113:3000/Detection/create"
    headers = {
        'Content-Type': "application/json"
    }
    json_payload = json.dumps({
        "NbrPlate": str(data[2]),
        "Time": str(data[1]),
        "ID": int(data[0])
    })
    r = requests.post(base_url, data=json_payload, headers=headers)
    print("Status Code: " + r.status_code)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("user", "bonjour")
    client.connect(mqtt_broker_address, mqtt_port, 60)
    client.loop_forever()
