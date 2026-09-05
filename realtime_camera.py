import cv2
from ultralytics import YOLO
from tools.safety_risk_tool import SafetyRiskTool
import pyttsx3
import time


# ============================================================
# SETTINGS
# ============================================================

CONFIDENCE_THRESHOLD = 0.35
REQUIRED_CONFIRMATIONS = 5
VOICE_COOLDOWN = 3


# ============================================================
# INITIALIZE
# ============================================================

model = YOLO("yolo11n.pt")
safety_tool = SafetyRiskTool()
voice_engine = pyttsx3.init()


def speak(message):
    print("🔊 MonSight:", message)
    voice_engine.say(message)
    voice_engine.runAndWait()


# ============================================================
# CAMERA
# ============================================================

print("\n========================================")
print("      MONSIGHT VERIFICATION SYSTEM")
print("========================================")

print("\nStarting camera...")
print("Press Q to quit.")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open camera.")
    exit()


# ============================================================
# STATE
# ============================================================

last_risk = None
confirmed_risk = None
risk_count = 0

last_message = ""
last_voice_time = 0

hazard_present = False


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    height, width = frame.shape[:2]

    # --------------------------------------------------------
    # 1. PERCEIVE
    # --------------------------------------------------------

    results = model(frame, verbose=False)

    detections = []

    for result in results:

        for box in result.boxes:

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            class_id = int(box.cls[0])
            object_name = model.names[class_id]

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            box_width = x2 - x1
            box_height = y2 - y1

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # ------------------------------------------------
            # Horizontal position
            # ------------------------------------------------

            if center_x < width / 3:
                horizontal = "LEFT"

            elif center_x < (2 * width / 3):
                horizontal = "CENTER"

            else:
                horizontal = "RIGHT"

            # ------------------------------------------------
            # Vertical position
            # ------------------------------------------------

            if center_y < height / 3:
                vertical = "ABOVE"

            elif center_y < (2 * height / 3):
                vertical = "CENTER"

            else:
                vertical = "BELOW"

            # ------------------------------------------------
            # Approximate proximity
            # ------------------------------------------------

            area_ratio = (
                (box_width * box_height)
                / (width * height)
            )

            if area_ratio > 0.25:
                proximity = "NEAR"

            elif area_ratio > 0.08:
                proximity = "MEDIUM"

            else:
                proximity = "FAR"

            detections.append({
                "object": object_name,
                "confidence": round(confidence, 2),
                "horizontal_position": horizontal,
                "vertical_position": vertical,
                "proximity": proximity
            })


    # --------------------------------------------------------
    # 2. UNDERSTAND + ASSESS
    # --------------------------------------------------------

    # SafetyRiskTool expects the detection list directly.
    safety_result = safety_tool.assess_risk(
        detections
    )

    current_risk = safety_result["overall_risk"]


    # --------------------------------------------------------
    # 3. VERIFY RISK ACROSS FRAMES
    # --------------------------------------------------------

    if current_risk == last_risk:

        risk_count += 1

    else:

        risk_count = 1
        last_risk = current_risk


    if risk_count >= REQUIRED_CONFIRMATIONS:

        confirmed_risk = current_risk


    # --------------------------------------------------------
    # 4. FIND IMPORTANT OBJECT
    # --------------------------------------------------------

    important_object = "None"

    if safety_result["hazards"]:

        risk_order = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        highest_detection = max(
            safety_result["hazards"],
            key=lambda item: risk_order.get(
                item["risk"],
                0
            )
        )

        important_object = highest_detection["object"]


    # --------------------------------------------------------
    # 5. DECIDE
    # --------------------------------------------------------

    if confirmed_risk == "CRITICAL":

        action = "STOP"

        message = (
            f"Stop immediately. "
            f"{important_object} is a critical hazard."
        )

        hazard_present = True


    elif confirmed_risk == "HIGH":

        action = "CAUTION"

        message = (
            f"Caution. "
            f"{important_object} is nearby."
        )

        hazard_present = True


    elif confirmed_risk == "MEDIUM":

        action = "SLOW DOWN"

        message = (
            f"Slow down. "
            f"{important_object} detected."
        )

        hazard_present = True


    else:

        action = "CONTINUE"

        if hazard_present:

            message = (
                "Hazard cleared. "
                "Path appears clear. Continue."
            )

            hazard_present = False

        else:

            message = "Path appears clear. Continue."


    # --------------------------------------------------------
    # 6. DISPLAY
    # --------------------------------------------------------

    annotated_frame = results[0].plot()

    cv2.putText(
        annotated_frame,
        f"Risk: {confirmed_risk}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Action: {action}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Object: {important_object}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        "VERIFYING...",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "MonSight Verification System",
        annotated_frame
    )


    # --------------------------------------------------------
    # 7. VOICE
    # --------------------------------------------------------

    current_time = time.time()

    if (
        confirmed_risk is not None
        and message != last_message
        and current_time - last_voice_time >= VOICE_COOLDOWN
    ):

        speak(message)

        last_message = message
        last_voice_time = current_time


    # --------------------------------------------------------
    # 8. RE-CHECK
    # --------------------------------------------------------

    # The loop continuously returns to the camera,
    # reassesses the environment, and verifies the risk.


    # --------------------------------------------------------
    # QUIT
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

camera.release()
cv2.destroyAllWindows()

print("\n========================================")
print("   MONSIGHT VERIFICATION STOPPED")
print("========================================")