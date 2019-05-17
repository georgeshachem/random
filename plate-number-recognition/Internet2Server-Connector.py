import paho.mqtt.client as mqtt
import json
import requests
import ast

mqtt_broker_address = "212.98.137.194"
mqtt_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("blacklist_ul")


def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode('UTF-8')
        data = ast.literal_eval(data)
        print(data)

        base_url = "http://10.81.16.113:4000/Detection/create"
        headers = {
            'Content-Type': "application/json"
        }
        r = requests.post(base_url, json=data, headers=headers)
        print("Status Code: " + str(r.status_code))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("iotleb", "iotleb")
    client.connect(mqtt_broker_address, mqtt_port, 60)
    client.loop_forever()
