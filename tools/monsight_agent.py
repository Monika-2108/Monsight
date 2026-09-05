import sys
from pathlib import Path
import cv2
import pyttsx3

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from voice_input import get_voice_command
from vision_tool import analyze_image
from location_tool import LocationTool
from map_route_tool import MapRouteTool
from safety_risk_tool import SafetyRiskTool
from medicine_tool import MedicineTool


class MonSightAgent:

    def __init__(self):
        self.location_tool = LocationTool()
        self.map_tool = MapRouteTool()
        self.safety_tool = SafetyRiskTool()
        self.medicine_tool = MedicineTool()
        self.engine = pyttsx3.init()

    def speak(self, message):
        print(f"\n🔊 MonSight: {message}")
        self.engine.say(message)
        self.engine.runAndWait()

    def capture_camera_image(self):
        """Automatically capture one image from the webcam."""
        print("\n📷 Opening camera...")

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            self.speak("I cannot access the camera.")
            return None

        # Give camera a moment to initialize
        for _ in range(5):
            camera.read()

        success, frame = camera.read()
        camera.release()

        if not success:
            self.speak("I could not capture an image.")
            return None

        image_path = PROJECT_ROOT / "current_view.jpg"
        cv2.imwrite(str(image_path), frame)

        print(f"📷 Image captured: {image_path}")
        return str(image_path)

    def detect_intent(self, request):

        request = request.lower()

        medicine_words = [
            "medicine",
            "medicene",
            "tablet",
            "capsule",
            "drug",
            "medication",
            "pill",
            "expiry",
            "prescription"
        ]

        navigation_words = [
            "go",
            "take me",
            "navigate",
            "direction",
            "route",
            "where is",
            "reach",
            "walk",
            "library",
            "classroom",
            "canteen"
        ]

        for word in medicine_words:
            if word in request:
                return "MEDICINE"

        for word in navigation_words:
            if word in request:
                return "NAVIGATION"

        return "SAFETY"

    def find_destination(self, request):

        request = request.lower()

        destinations = [
            "library",
            "classroom",
            "canteen"
        ]

        for destination in destinations:
            if destination in request:
                return destination

        return None

    def run_safety(self, image_path):

        print("\n===== MONSIGHT SAFETY MODE =====")

        vision = analyze_image(image_path)

        safety = self.safety_tool.assess_risk(
            vision["detections"]
        )

        risk = safety["overall_risk"]

        if risk == "CRITICAL":
            message = "Stop immediately. A critical hazard is nearby."

        elif risk == "HIGH":
            message = "Caution. A hazard is ahead."

        elif risk == "MEDIUM":
            message = "Slow down and continue carefully."

        elif any(
            hazard["action"] == "VERIFY"
            for hazard in safety["hazards"]
        ):
            message = "Possible hazard detected. Slow down and verify."

        else:
            message = "Path appears clear. Continue carefully."

        self.speak(message)

        return {
            "mode": "SAFETY",
            "decision": safety["recommended_action"],
            "risk": safety,
            "vision": vision
        }

    def run_navigation(self, image_path, destination):

        print("\n===== MONSIGHT NAVIGATION =====")

        vision = analyze_image(image_path)

        location = self.location_tool.get_status()

        route = self.map_tool.get_route(destination)

        if route["status"] != "success":

            self.speak(
                "I could not find that destination."
            )

            print(route["message"])

            return None

        safety = self.safety_tool.assess_risk(
            vision["detections"]
        )

        risk = safety["overall_risk"]

        if risk == "CRITICAL":

            decision = "STOP"
            instruction = (
                "Stop immediately and remain still."
            )

        elif risk == "HIGH":

            decision = "CAUTION"
            instruction = (
                "Proceed carefully and stay alert."
            )

        elif risk == "MEDIUM":

            decision = "SLOW_DOWN"
            instruction = (
                "Slow down and continue carefully."
            )

        else:

            decision = "CONTINUE"
            instruction = (
                "Continue along the planned route."
            )

        self.speak(instruction)

        next_step = None

        if decision != "STOP":

            next_step = route["route"][0]

            self.speak(next_step)

        return {
            "mode": "NAVIGATION",
            "decision": decision,
            "instruction": instruction,
            "vision": vision,
            "location": location,
            "route": route,
            "safety": safety,
            "next_step": next_step
        }

    def run_medicine(self, image_path):

        print("\n===== MONSIGHT MEDICINE MODE =====")

        result = self.medicine_tool.read_medicine_label(
            image_path
        )

        if result["status"] != "success":

            self.speak(
                "I could not read the medicine label."
            )

            print("Error:", result["message"])

            return result

        print(
            "Medicine Name:",
            result["medicine_name"]
        )

        print(
            "Strength:",
            result["strength"]
        )

        print(
            "Expiry:",
            result["expiry"]
        )

        self.speak(
            f"The medicine label says "
            f"{result['medicine_name']}. "
            f"Strength: {result['strength']}. "
            f"Expiry: {result['expiry']}. "
            f"Please verify this information "
            f"with a doctor or pharmacist."
        )

        return {
            "mode": "MEDICINE",
            "medicine": result
        }

    def run(self, request):

        intent = self.detect_intent(request)

        print("\nDetected Intent:", intent)

        # Automatically capture image
        image_path = self.capture_camera_image()

        if image_path is None:
            return None

        if intent == "MEDICINE":

            return self.run_medicine(image_path)

        elif intent == "NAVIGATION":

            destination = self.find_destination(request)

            if destination is None:

                self.speak(
                    "Please say the destination again."
                )

                return None

            print(
                "Destination detected:",
                destination
            )

            return self.run_navigation(
                image_path,
                destination
            )

        else:

            return self.run_safety(image_path)


if __name__ == "__main__":

    agent = MonSightAgent()

    print("\n================================")
    print("        MONSIGHT AGENT")
    print("================================")

    # USER ONLY SPEAKS
    request = get_voice_command()

    if not request:

        print("No command detected.")
        sys.exit()

    result = agent.run(request)

    print("\n================================")
    print("        MONSIGHT RESULT")
    print("================================")

    if result:
        print("Mode:", result.get("mode"))