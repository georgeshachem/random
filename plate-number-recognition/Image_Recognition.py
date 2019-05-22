import sys
from openalpr import Alpr
import picamera
from time import sleep
import sqlite3
import time
import paho.mqtt.client as mqtt

pi_id = 123

mqtt_broker_address = "212.98.137.194"
mqtt_port = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.username_pw_set("user", "bonjour")
client.on_connect = on_connect
client.connect(mqtt_broker_address, mqtt_port, 60)

alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data/")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")

conn = sqlite3.connect('blacklist.db')
c = conn.cursor()

with picamera.PiCamera() as camera:
    camera.start_preview()
    camera.rotation = 180
    sleep(5)
    while True:
        try:
            camera.capture('/home/pi/Desktop/test.jpg')  # Capturing the image
            print('Done')

            results = alpr.recognize_file("/home/pi/Desktop/test.jpg")

            try:
                plate = results['results'][0]['candidates'][0]['plate']
                confidence = results['results'][0]['candidates'][0]['confidence']
                print("Plate: {}".format(plate))
                print("Confidence: {}".format(confidence))
            except Exception as e:
                print(e)

            c.execute("SELECT number FROM blacklist")
            x = c.fetchall()
            x = [i[0] for i in x]

            if plate in x:
                print("Blacklist")
                data = dict()
                data['NbrPlate'] = plate
                data['Time'] = int(time.time())
                data['ID'] = pi_id
                client.publish("blacklist_ul", payload=data)
            else:
                print("Good")

            sleep(5)
        except Exception as e:
            print(e)
            camera.stop_preview()
            camera.start_preview()
            camera.rotation = 180
            sleep(5)
        finally:
            camera.stop_preview()
        sleep(5)
