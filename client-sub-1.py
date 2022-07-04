# Importing Modules
import paho.mqtt.client as mqtt
import schedule

# MQTT Broker's Address (Local Host - Mosquitto Installed on Local Machine)
brokerAddress = "127.0.0.1"

# Lists to hold data
data_one_minute = [0]
data_five_minutes = [0]
data_thirty_minutes = [0]


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


def on_message(client, userdata, message):
    topic = message.topic
    message = str(message.payload.decode("utf-8"))
    print("Message Received on Topic : " + topic + " - " + message)

    # Casting message to int and appending to lists for calculating averages
    data_one_minute.append(int(message))
    data_five_minutes.append(int(message))
    data_thirty_minutes.append(int(message))


def calculate_average(values):
    try:
        return round((sum(values) / len(values)), 2)
    except Exception as e:
        print(e)


def send_stats(timeInterval):
    if timeInterval == 1:
        subscriber_one.publish("switchDin/stats/one", calculate_average(data_one_minute))
        print(data_one_minute)
        print("1 Minute Average Published")
        data_one_minute.clear()
    elif timeInterval == 5:
        subscriber_one.publish("switchDin/stats/five", calculate_average(data_five_minutes))
        print("5 Minute Average Published")
        data_five_minutes.clear()
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
