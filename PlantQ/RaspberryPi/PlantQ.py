import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import adafruit_dht
import board
from gpiozero import LED
import time
import busio
import adafruit_tsl2561

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# LED for MQTT-controlled light
LED_PIN = 27
GPIO.setup(LED_PIN, GPIO.OUT)

# Moisture Sensor Setup
MOISTURE_CHANNEL = 4
GPIO.setup(MOISTURE_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Relay pin setup for water pump
RELAY_PIN = 23  # GPIO 23 corresponds to physical pin 16
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # Ensure the relay is off initially

# Temperature/Humidity Sensor Setup
dht_device = adafruit_dht.DHT11(board.D17)

# LED for temperature indicator
#temp_led = LED(26)  # GPIO 26

# I2C Setup for TSL2561
i2c = busio.I2C(board.SCL, board.SDA)
tsl = adafruit_tsl2561.TSL2561(i2c)

# Configure TSL2561
tsl.enable = True
tsl.gain = 1

# MQTT Settings
BROKER = "localhost"
PORT = 1883
MOISTURE_TOPIC = "sensor/moisture"
TEMP_HUMID_TOPIC = "sensor/temperature"
LUX_TOPIC = "sensor/lux"
LED_TOPIC = "sensor/led"

# Callback for MQTT LED control
def on_message(client, userdata, msg):
    message = msg.payload.decode().strip()
    if message == "ON":
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        print("LED turned ON")
    elif message == "OFF":
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
        print("LED turned OFF")

# MQTT Client Setup
client = mqtt.Client()
client.on_connect = lambda c, u, f, rc: client.subscribe(LED_TOPIC)
client.on_message = on_message

# Connect to MQTT Broker
client.connect(BROKER, PORT)
client.loop_start()

try:
    while True:
        # Moisture Sensor
        moisture_status = "Dry" if GPIO.input(MOISTURE_CHANNEL) else "Wet"
        print(f"Moisture Status: {moisture_status}")
        client.publish(MOISTURE_TOPIC, moisture_status)

        # Control water pump based on moisture status
        if moisture_status == "Dry":
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Activate relay
            print("Pump activated to water the plant")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Deactivate relay
            print("Pump deactivated as soil is wet")

        # Temperature and Humidity Sensor
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None and humidity is not None:
                print(f"Temperature: {temperature}C, Humidity: {humidity}%")
                client.publish(TEMP_HUMID_TOPIC, f"Temperature: {temperature}C, Humidity: {humidity}%")
               # if temperature > 25:
               #     temp_led.on()
               # else:
               #     temp_led.off()
        except RuntimeError as error:
            print(f"Runtime error: {error.args[0]}")
        except Exception as error:
            dht_device.exit()
            raise error

        # TSL2561 Luminosity Sensor
        lux = tsl.lux
        print(f"Ambient Light Level: {lux} lux")
        client.publish(LUX_TOPIC, f"Ambient Light Level: {lux} lux")

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")
finally:
    GPIO.cleanup()
    client.disconnect()

