**Installation and Setup Instructions**

This section provides a detailed explanation of how to install and configure all the hardware and software components required for the *Smart Traffic Management System to Reduce Ambulance Delay* project using Arduino Uno and Visual Studio.

---

### 1. Software Installation

#### (a) Visual Studio Installation

1. Download **Visual Studio** from [https://visualstudio.microsoft.com/downloads](https://visualstudio.microsoft.com/downloads).
2. During installation, select the **“Desktop development with C++”** workload to enable hardware programming support.
3. After installation, open Visual Studio and create a **new Console Application** project.
4. From the *Extensions → Manage Extensions* menu, install the **Arduino IDE for Visual Studio** extension to integrate Arduino programming directly into Visual Studio.
5. (Optional) If YOLOv8 or image processing is used, install **Python Tools for Visual Studio (PTVS)** to enable Python script integration.

---

#### (b) Arduino IDE Installation

1. Download the **Arduino IDE** from [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software).
2. Install and open the IDE.
3. Go to **Tools → Board → Boards Manager**, search for *Arduino AVR Boards*, and install it.
4. Connect your **Arduino Uno** via USB cable to your computer.
5. In the Arduino IDE, go to **Tools → Board → Arduino Uno** and select the correct **COM Port** under *Tools → Port*.
6. Verify the installation by uploading the **Blink** example sketch (File → Examples → Basics → Blink).

   * If the LED on the Arduino board starts blinking, the installation was successful.

---

#### (c) Python and YOLOv8 Setup (for Ambulance Detection)

1. Install **Python 3.10 or higher** from [https://www.python.org/downloads](https://www.python.org/downloads).
2. Open Command Prompt and install the following required libraries:

   ```
   pip install ultralytics opencv-python pyserial numpy
   ```
3. Download the YOLOv8 model weights (e.g., `yolov8n.pt`) from [https://github.com/ultralytics](https://github.com/ultralytics).
4. Test the model by running:

   ```
   yolo predict model=yolov8n.pt source='test_image.jpg'
   ```

   This should open a window showing object detection results.

---

### 2. Hardware Setup

#### (a) Components Required

* Arduino Uno board
* ESP32-CAM module (for live camera input)
* Red, Yellow, and Green LEDs (to simulate traffic lights)
* 220Ω resistors for LEDs
* Breadboard and jumper wires
* USB cable (for Arduino connection)
* 5V DC power supply (optional external power)

---

#### (b) Circuit Connections

1. Connect the **Red**, **Yellow**, and **Green** LEDs to Arduino Uno digital pins **8**, **9**, and **10** respectively, each through a 220Ω resistor.
2. Connect the **negative terminal** of all LEDs to the Arduino **GND** pin.
3. Interface the **ESP32-CAM module** with Arduino Uno:

   * TX (ESP32-CAM) → RX (Arduino Pin 0)
   * RX (ESP32-CAM) → TX (Arduino Pin 1)
   * 5V → 5V, and GND → GND
4. Power the Arduino Uno through the USB connection for programming and testing.

---

### 3. Integration with Visual Studio

1. Open Visual Studio and create a **Serial Communication Program** using C++ or Python.
2. Use the **SerialPort** library in C++ or the **pyserial** package in Python to communicate with the Arduino Uno.
3. The program should send a serial signal (e.g., “1”) to the Arduino when an ambulance is detected by the YOLOv8 model.
4. In the Arduino sketch:

   * Read the incoming serial data using `Serial.read()`.
   * If “1” is received, turn ON the Green LED (ambulance detected).
   * Otherwise, run the standard Red–Yellow–Green traffic light sequence.
5. Upload the Arduino sketch and execute the Visual Studio program to verify successful communication.

---

### 4. Testing Procedure

1. Run the YOLOv8 detection script in Visual Studio or Python environment.
2. When the ambulance is detected, the program sends a signal to the Arduino Uno.
3. The Arduino Uno switches the traffic signal to **Green**, allowing the ambulance to pass.
4. When no ambulance is detected, the Arduino follows the normal automatic signal cycle.
5. Observe the LED indicators and serial monitor output for correct operation.

---

### 5. Troubleshooting Guide

| Issue                          | Possible Cause                               | Solution                                                                |
| ------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------- |
| **Arduino not uploading code** | Wrong COM port or missing driver             | Check Device Manager and install Arduino USB drivers.                   |
| **YOLO model not working**     | Incorrect model path or missing dependencies | Verify the `yolov8n.pt` file and re-run `pip install ultralytics`.      |
| **No LED response**            | Incorrect wiring                             | Double-check circuit connections and resistor placement.                |
| **Serial communication error** | COM port conflict                            | Ensure the same COM port is used in both Visual Studio and Arduino IDE. |

---

After completing all installations and configurations, the system becomes ready to perform real-time ambulance detection, send control signals via Visual Studio, and manage traffic lights automatically using the Arduino Uno microcontroller.
