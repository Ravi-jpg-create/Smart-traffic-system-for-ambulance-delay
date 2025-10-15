import cv2
from ultralytics import YOLO

# 🔹 Load YOLOv8 pretrained model
model = YOLO('yolov8n.pt')  # Use yolov8n.pt (Nano version, fastest)

# 🔹 Open Camera
cap = cv2.VideoCapture(0)

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

    # 🔹 Check all detections
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])

        # 🔹 Only detect "truck" as "Ambulance" (change logic if needed)
        if label.lower() == "truck":  
            ambulance_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Ambulance {conf:.2f}", (x1, y1 - 10),  # Changed label to "Ambulance"
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 🔹 Simulate Traffic Light on Screen
    if ambulance_detected:
        status = "AMBULANCE DETECTED - GREEN LIGHT"
        traffic_color = (0, 255, 0)  # Green
    else:
        status = "NO AMBULANCE - RED LIGHT"
        traffic_color = (0, 0, 255)  # Red

    # 🔹 Draw Traffic Light Simulation
    light_center = (50, 50)
    light_radius = 20
    cv2.circle(frame, light_center, light_radius, traffic_color, -1)  # filled circle

    # 🔹 Display Status Text
    cv2.putText(frame, status, (100, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, traffic_color, 2)

    cv2.imshow("Ambulance Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🔹 Clean up
cap.release()
cv2.destroyAllWindows()
