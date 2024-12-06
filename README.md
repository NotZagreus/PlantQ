# PlantQ: Smart Plant Maintenance System

Welcome to the PlantQ project! This system automates plant care by integrating smart technology to monitor soil moisture, ambient conditions, and light levels. PlantQ ensures your plants get the water and light they need to thrive.

---

## Project Features

- **Automated Watering:** The system waters plants when the soil moisture is too low.
- **Environmental Monitoring:** Displays real-time humidity and temperature levels.
- **Intelligent Lighting:** Provides adequate light using a light sensor or APIs to compensate for insufficient sunlight.

---

## How to Make This Project Work for You

### Hardware Requirements

If you haven't set up the hardware yet, you'll need the following:

1. A Raspberry Pi
2. Breadboards
3. DHT11 Sensor
4. Light Sensor
5. Moisture Sensor
6. 5V Relay
7. 5V Water Pump
8. LEDs (as many as you like)
9. Resistors
10. Male-to-Male and Male-to-Female Cables
11. *Optional:* A Breadboard Extension

### Raspberry Pi Setup

1. Turn on your Raspberry Pi.
2. Ensure the `plant.py` file is present on the device.
3. Run the file using the command:
   ```bash
   python3 PlantQ.py
   ```
4. Check for any error messages.
5. If no errors appear, the system should be up and running, recording environmental data.

### Computer Setup

1. Clone the PlantQ repository from GitHub:
   ```bash
   git clone https://github.com/NotZagreus/PlantQ
   ```
2. Import the files into an IDE, such as PyCharm.
3. Run the `app.py` file.
4. Once the application starts, open the provided link (ending in `:5000`) in your browser to access the PlantQ website.
5. Log in and enjoy monitoring and automating your plant care.

---

## Resources

- [**YouTube Video**](https://youtu.be/Cs_xcP-y0g8): Detailed walkthrough of the project.
- [**GitHub Repository**](https://github.com/NotZagreus/PlantQ): Source code and setup instructions.

---

## Final Outcome

The PlantQ system enables:

- Automatic watering based on soil moisture levels.
- Real-time monitoring of temperature and humidity.
- Intelligent lighting management to ensure optimal plant growth, even in suboptimal natural light conditions.

---

## Acknowledgments

This project was made possible by leveraging the power of Python, Raspberry Pi, and APIs to create an intelligent and adaptive plant care solution.

Happy Planting!

-Artem Kozlov
