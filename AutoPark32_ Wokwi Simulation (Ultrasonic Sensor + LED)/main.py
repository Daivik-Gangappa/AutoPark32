from machine import Pin, time_pulse_us
import time

# Define GPIO Pins
TRIG = Pin(5, Pin.OUT)  # Ultrasonic Trigger
ECHO = Pin(18, Pin.IN)  # Ultrasonic Echo
RED_LED = Pin(15, Pin.OUT)  # Red LED (Occupied)
GREEN_LED = Pin(14, Pin.OUT)  # Green LED (Available)

# Function to measure distance
def get_distance():
    TRIG.value(0)  # Set Trigger LOW
    time.sleep_us(2)
    TRIG.value(1)  # Set Trigger HIGH
    time.sleep_us(10)
    TRIG.value(0)  # Set Trigger LOW

    duration = time_pulse_us(ECHO, 1, 30000)  # Timeout after 30ms
    if duration < 0:  # If timeout occurs
        print("⚠️ Error: No pulse received, setting distance to 1000cm")
        return 1000  # Return a large distance if no pulse is detected

    distance = (duration * 0.0343) / 2  # Convert to cm
    return distance

while True:
    distance = get_distance()
    print(f"📏 Measured Distance: {distance:.2f} cm")
    
    if distance < 10:  # Vehicle detected
        RED_LED.value(1)  # Turn ON Red LED
        GREEN_LED.value(0)  # Turn OFF Green LED
        print("🚗 Parking Slot Occupied")
    
    else:  # No vehicle detected
        RED_LED.value(0)  # Turn OFF Red LED
        GREEN_LED.value(1)  # Turn ON Green LED
        print("🟢 Parking Slot Available")

    time.sleep(1)
