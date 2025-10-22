import paho.mqtt.client as mqtt

# ---------------------------
# Callback functions
# ---------------------------

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribe when connected
    client.subscribe("ece180d/test", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print("Received message: '{}' on topic '{}' with QoS {}".format(
        message.payload.decode(), message.topic, message.qos))

# ---------------------------
# MQTT Client setup
# ---------------------------

# 1. Create a client instance
client = mqtt.Client()

# 2. Attach callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 3. Connect to the public broker
client.connect_async("test.mosquitto.org")

# 4. Start the network loop
client.loop_start()

# 5. Keep the script running to receive messages
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnecting...")
    client.loop_stop()
    client.disconnect()

