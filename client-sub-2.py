# Importing Modules
import paho.mqtt.client as mqtt

# MQTT Broker's Address (Local Host - Mosquitto Installed on Local Machine)
brokerAddress = "127.0.0.1"

# Placeholders for Average
one_minute_average = 0
five_minute_average = 0
thirty_minute_average = 0

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

while True:
    subscriber_two.loop()