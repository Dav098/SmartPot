# SmartPot

# Plant Monitoring System
This repository contains the code for a plant monitoring system that utilizes an Arduino microcontroller, a Raspberry Pi, and a mobile application. The system monitors environmental conditions such as air temperature, humidity, soil moisture, and light intensity, and logs this data into a SQLite database. The mobile application allows users to view and manage this data.

# Components
## 1. Arduino
The Arduino code reads data from sensors and controls an LED strip. The sensors used are:

DHT11: Measures air temperature and humidity.
Photoresistor: Measures light intensity.
Soil Humidity Sensor (SHS): Measures soil moisture.
## 2. Raspberry Pi
The Raspberry Pi receives data from the Arduino, stores it in a SQLite database, and provides a server to handle client requests for the data.

## 3. Mobile Application
The mobile app, built with Kivy and KivyMD, allows users to view the environmental data, add new plants, save plant history, and view archived data.

# Instructions
## Arduino Setup:
Connect the sensors to the Arduino as per their respective pins.
Upload the arduino.ino code to the Arduino.

## Raspberry Pi Setup:
Connect the Raspberry Pi to the Arduino.
Ensure the Raspberry Pi is connected to the same network as the mobile device.
Run raspberrypi.py on the Raspberry Pi to start receiving and storing data from the Arduino.

## Mobile Application:
Ensure the mobile device is connected to the same network as the Raspberry Pi.
Run mobileApp.py on the mobile device to start the Kivy application (you can create apk file for android using buildozer).

## Database Management:
The database is managed through the Raspberry Pi and can be accessed through the mobile app.
Use the mobile app to add new plants, save history, and view data logs.
This plant monitoring system provides a comprehensive solution for tracking and managing plant health and environmental conditions.
