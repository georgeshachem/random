import paho.mqtt.client as mqttClient
import time
import sqlite3
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    message = (message.payload.decode("utf-8"))
    print ("Message received: "  + message)
    if (message[0] == "a"):
        try:
            conn = sqlite3.connect("blacklist.db")
            c = conn.cursor()
            c.execute('INSERT INTO blacklist VALUES (?)',(message[1:],))
            conn.commit()
            print("Added to DB")
            conn.close()
        except Exception as e:
            print('sqlite error: ', e.args[0])

    elif (message[0] == "r"):
        try:
            conn = sqlite3.connect("blacklist.db")
            c = conn.cursor()
            c.execute('DELETE FROM blacklist WHERE NUMBER = (?)',(message[1:],))
            conn.commit()
            print("Deleted from DB")
            conn.close()
        except Exception as e:
            print('sqlite error: ', e.args[0])    
    else:
        print("wrong format")
 
Connected = False   #global variable for the state of the connection
 
broker_address= "212.98.137.194"  #Broker address
port = 1883                        #Broker port
user = "user"                    #Connection username
password = "bonjour"            #Connection password
 
client = mqttClient.Client()               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("blacklist_dl")
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()