"""
Author : Harkaran Singh
Year : 2022
"""

# Importing Modules
import paho.mqtt.client as mqtt
import random as rd
import time

# MQTT Broker's Address (Local Host - Mosquitto Installed on Local Machine)
brokerAddress = "127.0.0.1"


def on_connect(client, userdata, flags, rc):
    """
    Call Back function when the client recieves a response from the broker.
    :param userdata: User Private Data
    :param client: The client which is connected to the Broker
    :param rc: Connection Result. {0: Successful, 1-5 Refused due to various reasons}
    """
    # If connected
    if rc == 0:
        print("Connected to Broker at " + brokerAddress)

    # If not connected
    else:
        print("Not connected | Received : " + rc)


def on_disconnect(client, userdata, flags, rc=0):
    """
    The Callback Function when the client disconnects from the Broker
    :param client: The client to be disconnected
    :param userdata: User Private Data
    :param rc: Disconnection Result.
    """
    print("Disconnected to Broker at " + brokerAddress)


def randomNumberPublisher(client):
    """
    A function which randomly publishes an integer value at random intervals to a MQTT Broker
    :param client: The client from which the message is to be published to the broker
    :return: None
    """

    # Generates a random number between 1 and 100
    randomNumber = rd.randint(1, 100)

    # Generates a random interval between 1 and 30 (Seconds)
    randomInterval = rd.randint(1, 30)

    # Published random number to a topic to the broker
    client.publish("switchDin/randomNumber", randomNumber)

    # Prints out confirmation of message published
    print("Message Published to: " + brokerAddress + " | Value: " + str(randomNumber))

    # A random interval before the next number is published
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
