# Importing Paho
import paho.mqtt.client as mqtt
import random as rd
import time

# MQTT Broker's Address (Local Host - Mosquitto Installed on Local Machine)
brokerAddress = "127.0.0.1"


# Binding Functions - On Connect
def on_connect(client, userdata, flags, rc):
    # If connected
    if rc == 0:
        print("Connected to Broker at " + brokerAddress)

    # If not connected
    else:
        print("Not connected | Received : " + rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected to Broker at " + brokerAddress)


def randomNumberPublisher(client):
    """
    A function which randomly publishes an integer value at random intervals to a MQTT Broker
    :param client: The client from which the message is to be published to the broker
    :return: None
    """
    randomNumber = rd.randint(1, 100)
    randomInterval = rd.randint(1, 2)
    client.publish("switchDin/randomNumber", randomNumber)
    time.sleep(randomInterval)


# Creating a Client instance
randomNumberPublisherClient = mqtt.Client("rnd_publisher")

# Binding Call Back Functions
randomNumberPublisherClient.on_connect = on_connect
randomNumberPublisherClient.on_disconnect = on_disconnect

# Connecting client to broker
randomNumberPublisherClient.connect(brokerAddress)

# Looping Forever
while True:
    # Publishing Random Number
    randomNumberPublisher(randomNumberPublisherClient)
