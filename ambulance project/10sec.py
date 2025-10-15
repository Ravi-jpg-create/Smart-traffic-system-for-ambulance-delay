import cv2
import serial
import time
import logging
from ultralytics import YOLO
import winsound
from playsound import playsound

# 🔹 Set up logging
logging.basicConfig(filename='ambulance_detection.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# 🔹 Load YOLOv8 pretrained model
model = YOLO('yolov8n.pt')

# 🔹 Connect to Arduino
arduino_port = 'COM3'
baud_rate = 9600
try:
    arduino = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)
    print("✅ Arduino connected successfully!")
except:
    print("❌ Arduino not connected. Check COM port!")
    arduino = None

# 🔹 Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible!")
    exit()

AMBULANCE_CLASS_ID = 2  # Example, check the actual class ID of the ambulance

# Initialize the time variables for controlling green signal
green_signal_time = 0  # Timestamp when green signal was activated
green_signal_duration = 15  # Duration in seconds for green signal

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame!")
        break

    results = model.predict(frame, imgsz=640, conf=0.5)[0]

    something_detected = False

    # 🔹 Check all detections
    for box in results.boxes:
        class_id = int(box.cls[0])  # Extract class id
        if class_id == AMBULANCE_CLASS_ID:  # Check if it's an ambulance
            something_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Ambulance {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 🔹 Logging
    if something_detected:
        logging.info("Ambulance detected")
        status = "AMBULANCE DETECTED - GREEN LIGHT"
        traffic_color = (0, 255, 0)
        if arduino:
            arduino.write(b'GREEN\n')
        # 🔹 Sound alert
        winsound.Beep(1000, 1000)  # Windows beep
        # or playsound('alert_sound.mp3') for cross-platform
        green_signal_time = time.time()  # Record the time the green signal was turned on
    else:
        # If 10 seconds have passed, switch to red
        if time.time() - green_signal_time > green_signal_duration:
            status = "NO AMBULANCE - RED LIGHT"
            traffic_color = (0, 0, 255)
            if arduino:
                arduino.write(b'RED\n')
        else:
            # Keep green light on until 10 seconds pass
            status = "AMBULANCE DETECTED - GREEN LIGHT"
            traffic_color = (0, 255, 0)
            if arduino:
                arduino.write(b'GREEN\n')

    # 🔹 Draw on-screen traffic light indicator
    cv2.circle(frame, (50, 50), 20, traffic_color, -1)
    cv2.putText(frame, status, (100, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, traffic_color, 2)

    cv2.imshow("Ambulance Detection Simulation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🔹 Cleanup
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
