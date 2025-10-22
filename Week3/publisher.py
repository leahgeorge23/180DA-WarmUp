import paho.mqtt.client as mqtt
import numpy as np
import time

# Define callbacks (optional for publisher)
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# Create client and assign callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to broker
client.connect_async('test.mosquitto.org')
client.loop_start()

# Publish 10 random numbers to the topic
for i in range(10):
    num = float(np.random.random(1))
    print(f"Publishing {num}")
    client.publish('ece180d/test', num, qos=1)
    time.sleep(1)

# Clean up
client.loop_stop()
client.disconnect()
