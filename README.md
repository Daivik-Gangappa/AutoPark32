# 🚗 AutoPark32 – Smart Parking System with AWS IoT Integration

This project simulates a smart parking system using **ESP32 (Wokwi)**, **MQTT (HiveMQ Cloud)**, and **AWS IoT Core** for real-time cloud-based monitoring of parking slot status.

---

## 📌 Features

- 🔄 Real-time parking slot detection (Occupied/Available)
- 📶 MQTT communication with HiveMQ (`test.mosquitto.org`)
- 🔁 Python bridge to forward messages to AWS IoT Core
- ☁️ Cloud integration with AWS for analytics, monitoring, and automation
- 🧪 Fully testable in the Wokwi simulator (no hardware required)

---

## 🧩 Architecture

```text
[Wokwi ESP32 Simulation]
        |
        | MQTT (smart_parking/status)
        v
[HiveMQ - test.mosquitto.org]
        |
        | Python MQTT Bridge
        v
[AWS IoT Core]
