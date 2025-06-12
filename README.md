**🚗 AutoPark32 – Smart Parking System with Dual Cloud Integration & Dynamic Pricing (ML-Based)**



This project simulates a smart parking system using ESP32 (Wokwi) to monitor slot availability and leverages MQTT, ThingSpeak, and AWS IoT Core for cloud integration. It features dynamic pricing powered by machine learning, responsive dashboards, and scalable data routing—all without the need for physical hardware.

**📌 Features**
🔄 Real-time parking slot detection (1 = Occupied, 0 = Available)
📡 MQTT data publishing via HiveMQ (test.mosquitto.org)
🌐 Dual cloud routing:
🛰️ ThingSpeak: Visualization + API data stream
☁️ AWS IoT Core: Enterprise-grade handling via Python MQTT bridge
🧠 ML-based dynamic pricing algorithm
⚛️ ReactJS frontend for real-time dashboard and pricing display
🧪 Wokwi simulator—fully hardware-free testing

**🧠 ML-Driven Dynamic Pricing**
Our machine learning model adjusts pricing based on:
Current parking occupancy
Historical slot usage patterns
Time of day and availability trends
This allows demand-based real-time pricing similar to modern smart city systems.

**🧩 Architecture Overview**

🔁 Flow 1: AWS IoT Core (Secure Cloud Processing)

[Wokwi ESP32 Simulation] -------------------------------------> [HiveMQ - test.mosquitto.org] ------------------------------------->[AWS IoT Core]
..........................................................     MQTT (smart_parking/status)  .....................................................................                                 Python MQTT Bridge (TLS & Certs)


🔁 Flow 2: ThingSpeak + Frontend Visualization

[Wokwi ESP32 Simulation] -------------------------------------> [ThingSpeak API] ----------------------------------> [React Frontend App]


**⚙️ Tech Stack**
Microcontroller Simulation: ESP32 (Wokwi)
Protocol: MQTT
Broker: HiveMQ (test.mosquitto.org)
Backend Cloud: AWS IoT Core (TLS-secured bridge)
Frontend API: ThingSpeak
UI Layer: ReactJS (real-time visualization + dynamic pricing)
ML Integration: Python-based model trained on slot occupancy data

**🚀 How to Run**
Simulate ESP32 in Wokwi: Publishes slot status via MQTT
Run Python MQTT Bridge: Forwards data securely to AWS IoT Core
Enable ThingSpeak API: Stores real-time parking data for frontend
Launch React App: Connects to ThingSpeak API for slot + price display
