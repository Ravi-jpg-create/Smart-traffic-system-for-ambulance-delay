##final code
import cv2
import serial
import time
import logging
from ultralytics import YOLO
import winsound

logging.basicConfig(filename='vehicle_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')


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


cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("http://192.168.51.161:81/stream")
if not cap.isOpened():
    print("Camera not accessible!")
    exit()


green_signal_time = 0
green_signal_duration = 5  
screenshot_count = 0 

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

       
        if label.lower() in ["truck", "bus"]:
            ambulance_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Ambulance {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if ambulance_detected:
        logging.info("Ambulance detected")
        status = "AMBULANCE DETECTED - GREEN LIGHT"
        traffic_color = (0, 255, 0)
        if arduino:
            arduino.write(b'GREEN\n')
        winsound.Beep(1000, 1000)
        green_signal_time = time.time()


        if screenshot_count < 2:
            filename = f"ambulance_{int(time.time())}.png"
            cv2.imwrite(filename, frame)
            screenshot_count += 1
            print(f"✅ Screenshot saved as {filename}")

    else:

        if time.time() - green_signal_time > green_signal_duration:
            status = "NO AMBULANCE - RED LIGHT"
            traffic_color = (0, 0, 255)
            if arduino:
                arduino.write(b'RED\n')
        else:
            status = "AMBULANCE DETECTED - GREEN LIGHT"
            traffic_color = (0, 255, 0)
            if arduino:
                arduino.write(b'GREEN\n')


    cv2.circle(frame, (50, 50), 20, traffic_color, -1)
    cv2.putText(frame, status, (100, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, traffic_color, 2)

    cv2.imshow("Ambulance Detection (Arduino + Screen)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
