# detect_vehicle_with_arduino_and_screen_fixed.py

import cv2
import serial
import time
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  
arduino_port = 'COM4'  
baud_rate = 9600
try:
    arduino = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  
    print("✅ Arduino connected successfully!")
except:
    print("❌ Arduino not connected. Check COM port!")
    arduino = None  


cap = cv2.streamCapture(0)

if not cap.isOpened():
    print("Camera not accessible!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame!")
        break

    results = model.predict(frame, imgsz=640, conf=0.5)[0]

    ambulance_detected = False


    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])

      
        if label.lower() == "truck":
            ambulance_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            cv2.putText(frame, f"Ambulance {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

   
    if ambulance_detected:
        status = "AMBULANCE DETECTED - GREEN LIGHT"
        traffic_color = (0, 255, 0)  # Green

        if arduino:
            arduino.write(b'GREEN\n')  
    else:
        status = "NO AMBULANCE - RED LIGHT"
        traffic_color = (0, 0, 255) 

        if arduino:
            arduino.write(b'RED\n')  

 
    cv2.putText(frame, status, (100, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, traffic_color, 2)

    cv2.imshow("Ambulance Detection (Arduino + Screen)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()