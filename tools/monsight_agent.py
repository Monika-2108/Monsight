import pyttsx3

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

    # ---------------- INTENT DETECTION ----------------

    def detect_intent(self, request):

        request = request.lower()

        medicine_words = [
            "medicine", "medicene", "tablet",
            "capsule", "drug", "medication",
            "pill", "expiry", "dosage",
            "prescription"
        ]

        navigation_words = [
            "go", "take me", "navigate",
            "direction", "route", "where is",
            "reach", "walk", "library",
            "classroom", "canteen"
        ]

        for word in medicine_words:
            if word in request:
                return "MEDICINE"

        for word in navigation_words:
            if word in request:
                return "NAVIGATION"

        return "SAFETY"

    # ---------------- SAFETY ----------------

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

    # ---------------- NAVIGATION ----------------

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

    # ---------------- MEDICINE ----------------

    def run_medicine(self, image_path):

        print("\n===== MONSIGHT MEDICINE MODE =====")

        result = self.medicine_tool.read_medicine_label(
            image_path
        )

        if result["status"] != "success":

            print("Error:", result["message"])

            return result

        print("Medicine Name:", result["medicine_name"])
        print("Strength:", result["strength"])
        print("Expiry:", result["expiry"])

        return {
            "mode": "MEDICINE",
            "medicine": result
        }

    # ---------------- MAIN AGENT ----------------

    def run(
        self,
        request,
        image_path,
        destination=None
    ):

        intent = self.detect_intent(request)

        print("\nDetected Intent:", intent)

        if intent == "MEDICINE":

            return self.run_medicine(image_path)

        elif intent == "NAVIGATION":

            if destination is None:
                destination = input(
                    "Enter destination: "
                ).strip().lower()

            return self.run_navigation(
                image_path,
                destination
            )

        else:

            return self.run_safety(image_path)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    agent = MonSightAgent()

    print("\n================================")
    print("        MONSIGHT AGENT")
    print("================================")

    request = input(
        "\nWhat do you want MonSight to do? "
    )

    image_path = input(
        "Enter image path: "
    )

    destination = None

    if agent.detect_intent(request) == "NAVIGATION":

        destination = input(
            "Enter destination: "
        ).strip().lower()

    result = agent.run(
        request,
        image_path,
        destination
    )

    print("\n================================")
    print("        MONSIGHT RESULT")
    print("================================")

    if result:
        print("Mode:", result.get("mode"))