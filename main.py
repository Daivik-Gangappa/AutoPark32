from machine import Pin, time_pulse_us
import utime

# Define GPIO Pins
TRIG = Pin(3, Pin.OUT)       # Ultrasonic Trigger
ECHO = Pin(2, Pin.IN)        # Ultrasonic Echo
RED_LED = Pin(15, Pin.OUT)   # Red LED (Occupied)
GREEN_LED = Pin(14, Pin.OUT) # Green LED (Available)

# Function to measure distance
def get_distance():
    TRIG.low()
    utime.sleep_us(2)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()

    duration = time_pulse_us(ECHO, 1)
    distance = (duration * 0.0343) / 2  # Convert to cm
    return distance

while True:
    # Check slot occupancy with Ultrasonic Sensor
    distance = get_distance()
    
    if distance < 10:  # Vehicle detected
        RED_LED.high()
        GREEN_LED.low()
        print("🚗 Parking Slot Occupied")
    
    else:  # No vehicle detected
        RED_LED.low()
        GREEN_LED.high()
        print("🟢 Parking Slot Available")

    utime.sleep(1)
