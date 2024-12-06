import os
import datetime
import paho.mqtt.client as paho
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# MQTT broker configuration
BROKER = "raspberrypi"
PORT = 1883
TOPIC = "sensor/temperature"
MOISTURE_TOPIC = "sensor/moisture"
LUX_TOPIC = "sensor/lux"
LED_TOPIC = "sensor/led"

# Dictionary to store sensors data
sensor_data = {"temperature": [], "humidity": [], "moisture": [], "lux": []}

# Hardcoded credentials for login
USERNAME = "usr"
PASSWORD = "pwd"

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    client.subscribe(MOISTURE_TOPIC)
    client.subscribe(LUX_TOPIC)

# Callback function for receiving MQTT messages
def on_message(client, userdata, msg):
    data = msg.payload.decode().split(',')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    print("Received data:", data)

    # Create directory for storing data if it doesn't exist
    directory = f'static/{current_date}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, 'data_records.txt')

    # Append received data to the file and update sensor_data dictionary
    with open(file_path, 'a') as file:
        if len(data) == 3:
            temperature = data[0].split(':')[1].strip()
            humidity = data[1].split(':')[1].strip()
            moisture = data[2].strip()
            sensor_data["temperature"].append(temperature)
            sensor_data["humidity"].append(humidity)
            sensor_data["moisture"].append(moisture)
            file.write(f"Time: {current_time}, Temperature: {temperature}, Humidity: {humidity}, Moisture: {moisture}\n")
        elif len(data) == 2:
            temperature = data[0].split(':')[1].strip()
            humidity = data[1].split(':')[1].strip()
            sensor_data["temperature"].append(temperature)
            sensor_data["humidity"].append(humidity)
            file.write(f"Time: {current_time}, Temperature: {temperature}, Humidity: {humidity}\n")
        elif len(data) == 1:
            if "Wet" in data[0]:
                sensor_data["moisture"].append("Wet")
                file.write(f"Time: {current_time}, Moisture: Wet\n")
            elif "Dry" in data[0]:
                sensor_data["moisture"].append("Dry")
                file.write(f"Time: {current_time}, Moisture: Dry\n")
            elif "lux" in data[0]:
                lux = float(data[0].split(':')[1].strip().split()[0])
                sensor_data["lux"].append(lux)
                file.write(f"Time: {current_time}, Lux: {lux}\n")
                # Control LED based on lux value
                if lux < 100:
                    client.publish(LED_TOPIC, "ON")
                else:
                    client.publish(LED_TOPIC, "OFF")
        else:
            print("Received data does not have the expected format:", data)

# Initialize MQTT client and set callback functions
client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
if client.connect(BROKER, PORT, 60) != 0:
    print("Couldn't connect to the MQTT broker")
    exit(1)

client.loop_start()

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

# Route for home page
@app.route('/home')
def home():
    return render_template("home.html")

# Route for live data page
@app.route('/live-data-page')
def live_data_page():
    return render_template("live-data.html")

# Route to fetch live data as JSON
@app.route('/live-data')
def live_data():
    latest_data = {
        "temperature": sensor_data["temperature"],
        "humidity": sensor_data["humidity"],
        "moisture": sensor_data["moisture"],
        "lux": sensor_data["lux"]
    }
    return jsonify(latest_data)

# Function to read logs from files
def read_logs():
    logs = {}
    base_dir = 'static'
    for date_dir in os.listdir(base_dir):
        date_path = os.path.join(base_dir, date_dir)
        if os.path.isdir(date_path):
            logs[date_dir] = []
            file_path = os.path.join(date_path, 'data_records.txt')
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    for line in file:
                        logs[date_dir].append(line.strip())
    return logs

# Route for logs page
@app.route('/logs')
def logs_page():
    logs = read_logs()
    return render_template("logs.html", logs=logs)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)