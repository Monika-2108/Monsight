from tools.safety_risk_tool import SafetyRiskTool


# Simulated dangerous situation
vision_result = {
    "detections": [
        {
            "object": "car",
            "confidence": 0.95,
            "horizontal_position": "CENTER",
            "vertical_position": "CENTER",
            "proximity": "NEAR"
        }
    ]
}


safety_tool = SafetyRiskTool()

result = safety_tool.assess_environment(
    vision_result
)


print("\n========================================")
print("       MONSIGHT SAFETY TEST")
print("========================================")

print("\nDetected Object: car")
print("Proximity: NEAR")

print("\nOverall Risk:")
print(result["overall_risk"])

print("\nRecommended Action:")
print(result["recommended_action"])

print("\nSafety Message:")

for detection in result["detections"]:
    print("-", detection["message"])

print("\n========================================")