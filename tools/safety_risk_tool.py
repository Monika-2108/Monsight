class SafetyRiskTool:

    HIGH_RISK_OBJECTS = {
        "car", "bus", "truck", "motorcycle", "train"
    }

    MEDIUM_RISK_OBJECTS = {
        "person", "bicycle", "dog", "cat",
        "chair", "bench", "suitcase"
    }

    def assess_risk(self, detections):
        """
        Assess hazards using object type, proximity and confidence.
        Handles uncertainty instead of blindly trusting weak detections.
        """

        results = []

        for detection in detections:
            object_name = detection.get("object", "unknown").lower()
            proximity = detection.get("proximity", "FAR").upper()
            confidence = float(detection.get("confidence", 0))

            # Ignore extremely weak detections
            if confidence < 0.35:
                continue

            # Uncertain detection
            if confidence < 0.50:
                risk = "LOW"
                action = "VERIFY"
                message = (
                    f"Possible {object_name} detected. "
                    "Please slow down and verify."
                )

            # High-risk objects
            elif object_name in self.HIGH_RISK_OBJECTS:

                if proximity == "NEAR":
                    risk = "CRITICAL"
                    action = "STOP"
                    message = (
                        f"Stop immediately. {object_name} detected nearby."
                    )

                elif proximity == "MEDIUM":
                    risk = "HIGH"
                    action = "CAUTION"
                    message = (
                        f"Caution. {object_name} detected ahead."
                    )

                else:
                    risk = "MEDIUM"
                    action = "SLOW_DOWN"
                    message = (
                        f"Slow down. {object_name} detected."
                    )

            # Medium-risk objects
            elif object_name in self.MEDIUM_RISK_OBJECTS:

                if proximity == "NEAR":
                    risk = "MEDIUM"
                    action = "SLOW_DOWN"
                    message = (
                        f"Slow down. {object_name} detected nearby."
                    )

                else:
                    risk = "LOW"
                    action = "CONTINUE"
                    message = (
                        f"{object_name} detected. Path appears manageable."
                    )

            # Unknown objects
            else:
                risk = "LOW"
                action = "CONTINUE"
                message = (
                    f"{object_name} detected. Continue carefully."
                )

            results.append({
                "object": object_name,
                "confidence": round(confidence, 2),
                "proximity": proximity,
                "risk": risk,
                "action": action,
                "message": message
            })

        # No reliable detections
        if not results:
            return {
                "overall_risk": "LOW",
                "recommended_action": "CONTINUE",
                "message": "No reliable hazards detected.",
                "hazards": []
            }

        # Risk priority
        priority = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4
        }

        highest = max(
            results,
            key=lambda x: priority[x["risk"]]
        )

        return {
            "overall_risk": highest["risk"],
            "recommended_action": highest["action"],
            "message": highest["message"],
            "hazards": results
        }


if __name__ == "__main__":

    tool = SafetyRiskTool()

    test_detections = [
        {
            "object": "car",
            "confidence": 0.91,
            "proximity": "NEAR"
        },
        {
            "object": "person",
            "confidence": 0.82,
            "proximity": "MEDIUM"
        }
    ]

    result = tool.assess_risk(test_detections)

    print("\n===== MONSIGHT SAFETY TEST =====")
    print("Overall Risk:", result["overall_risk"])
    print("Action:", result["recommended_action"])
    print("Message:", result["message"])

    print("\nHazards:")
    for hazard in result["hazards"]:
        print(hazard)