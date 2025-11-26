import paho.mqtt.client as mqtt
import random
import time

# Define MQTT server details
BROKER = "broker.emqx.io"   # Public EMQX broker
PORT = 8083                 # WebSocket port for EMQX

TEMP_TOPIC = "sensor/temperature"
OWNER_TOPIC = "sensor/deviceOwner"


# Device owner information
STUDENT_NAME = "David Paulins"
STUDENT_ID = "A00173358"

# How often to republish owner info (seconds)
OWNER_PUBLISH_INTERVAL = 30

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to EMQX broker over WebSocket")
        # Publish owner info once right after connecting
        publish_owner_info(client)
    else:
        print(f"Failed to connect with result code {rc}")

def publish_owner_info(client):
    #Publish device ownership information to OWNER_TOPIC.
    payload = f"{STUDENT_NAME} - {STUDENT_ID}"
    client.publish(OWNER_TOPIC, payload)
    print(f"Published owner info: '{payload}' to topic {OWNER_TOPIC}")

# Main publish loop
def publish_values():
    # Create a client instance using WebSockets
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)

    client.loop_start()

    last_owner_publish = time.time()

    try:
        while True:
            # Generate random temperature between 50 and 100
            value = random.uniform(50, 100)
            client.publish(TEMP_TOPIC, value)
            print(f"Published temperature {value:.2f} to topic {TEMP_TOPIC}")
            now = time.time()
            if now - last_owner_publish >= OWNER_PUBLISH_INTERVAL:
                publish_owner_info(client)
                last_owner_publish = now

            time.sleep(2)  # Publish every 2 seconds

    except KeyboardInterrupt:
        print("Stopping MQTT Publisher...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    publish_values()
