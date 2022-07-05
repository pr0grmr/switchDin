"""
Author : Harkaran Singh
Year : 2022
"""

# Importing Modules
import paho.mqtt.client as mqtt
from prettytable import PrettyTable
from datetime import datetime

# MQTT Broker's Address (Local Host - Mosquitto Installed on Local Machine)
brokerAddress = "127.0.0.1"

# Dictionary for Average (Would be zero until first instance of stats received from the broker)
avg_dict = {
    "1-Minute": 0,
    "5-Minutes": 0,
    "30-Minutes": 0
}

# Table to print stats
stats_table = PrettyTable()
stats_table.field_names = ["Time", "1 Min Avg", "5 Min Avg", "30 Min Avg"]
stats_table.add_row([datetime.now(), avg_dict["1-Minute"], avg_dict["5-Minutes"], avg_dict["30-Minutes"]])


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


def update_dict(topic, message):
    """
    A function to update the dictionary holding average data
    :param topic: The topic received by the broker
    :param message: The message received from the broker
    """
    if topic == "switchDin/stats/one":
        avg_dict["1-Minute"] = message

    elif topic == "switchDin/stats/five":
        avg_dict["5-Minutes"] = message

    elif topic == "switchDin/stats/thirty":
        avg_dict["30-Minutes"] = message


def on_message(client, userdata, message):
    """
    The Callback Function when the client receives a message from a Broker
    :param client: The client which is receiving the data
    :param userdata: Private User Data
    :param message: An instance of MQTT Message (Class)
    """

    # Retrieving the Message Topic
    topic = message.topic

    # Retrieving the Message Payload, Decoding and Adding to variables
    message = str(message.payload.decode("utf-8"))

    # Updates dictionary of averages
    update_dict(topic, message)

    # Prints out the table
    print_table()


def print_table():
    """
    Function to update the average values and print it out to the console
    """

    # Adds a row to the table with current time stamp
    stats_table.add_row([datetime.now(), avg_dict["1-Minute"], avg_dict["5-Minutes"], avg_dict["30-Minutes"]])

    # Prints table to console
    print(stats_table)


# Creating a Client instance
subscriber_two = mqtt.Client("subscriber_two")

# Binding Call Back Function
subscriber_two.on_connect = on_connect
subscriber_two.on_disconnect = on_disconnect
subscriber_two.on_message = on_message

# Connecting client to broker
subscriber_two.connect(brokerAddress)

# Subscribing to Topic(S)
subscriber_two.subscribe("switchDin/stats/one")
subscriber_two.subscribe("switchDin/stats/five")
subscriber_two.subscribe("switchDin/stats/thirty")

# Looping forever
while True:
    subscriber_two.loop()
