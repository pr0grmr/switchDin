"""
Author : Harkaran Singh
Year : 2022
"""

# Importing Modules
import paho.mqtt.client as mqtt
import schedule

# MQTT Broker's Address (Local Host - Mosquitto Installed on Local Machine)
brokerAddress = "127.0.0.1"

# Initialising Lists to hold data to be used for calculating averages
data_one_minute = [0]
data_five_minutes = [0]
data_thirty_minutes = [0]


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


def on_message(client, userdata, message):
    """
    The Callback Function when the client receives a message from a Broker
    :param client: The client which is receiving the data
    :param userdata: Private User Data
    :param message: An instance of MQTT Message (Class)
    """

    # Retrieving the message topic
    topic = message.topic

    # Retrieving and Decoding the Message Payload
    message = str(message.payload.decode("utf-8"))

    # Printing payload to console
    print("Message Received on Topic : " + topic + " - " + message)

    # Casting message to int and appending to Lists for calculating averages
    data_one_minute.append(int(message))
    data_five_minutes.append(int(message))
    data_thirty_minutes.append(int(message))


def calculate_average(values):
    """
    :param values: A list of values (ints) to calculate average.
    :return: Average of all the integers in the list
    """
    try:
        return round((sum(values) / len(values)), 2)
    except Exception as e:
        print(e)


def send_stats(timeInterval):
    """
    A function to publish stats (average) to the broker.
    :param timeInterval: Time after which the stats are send to the broker
    """

    # For 1 Minute Averages
    if timeInterval == 1:
        subscriber_one.publish("switchDin/stats/one", calculate_average(data_one_minute))
        print("1 Minute Average Published")
        data_one_minute.clear()

    # For 5 Minute Averages
    elif timeInterval == 5:
        subscriber_one.publish("switchDin/stats/five", calculate_average(data_five_minutes))
        print("5 Minute Average Published")
        data_five_minutes.clear()

    # For 30 Minute Averages
    elif timeInterval == 30:
        subscriber_one.publish("switchDin/stats/thirty", calculate_average(data_thirty_minutes))
        print("30 Minute Average Published")
        data_thirty_minutes.clear()


# Creating a Client instance
subscriber_one = mqtt.Client("subscriber_one")

# Binding Call Back Function
subscriber_one.on_connect = on_connect
subscriber_one.on_disconnect = on_disconnect
subscriber_one.on_message = on_message

# Connecting client to broker
subscriber_one.connect(brokerAddress)

# Subscribing to Topic
subscriber_one.subscribe("switchDin/randomNumber")

# Publish Stats
schedule.every().minute.do(send_stats, 1)
schedule.every(5).minutes.do(send_stats, 5)
schedule.every(30).minutes.do(send_stats, 30)

# Run Scheduler and Client Loop
while True:
    schedule.run_pending()
    subscriber_one.loop()
