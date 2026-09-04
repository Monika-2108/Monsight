from ultralytics import YOLO


# ============================================================
# MONSIGHT VISION TOOL
# ============================================================

# YOLO model
model = YOLO("yolo11n.pt")

# Minimum confidence for reliable detections
CONFIDENCE_THRESHOLD = 0.35


# Objects that may be important for walking safety
HIGH_RISK_OBJECTS = {
    "car",
    "bus",
    "truck",
    "motorcycle",
    "bicycle",
    "train",
}

MEDIUM_RISK_OBJECTS = {
    "person",
    "dog",
    "cat",
    "chair",
    "bench",
    "suitcase",
}


def get_horizontal_position(center_x, image_width):
    """Determine whether an object is left, center or right."""

    if center_x < image_width / 3:
        return "LEFT"

    elif center_x < (2 * image_width / 3):
        return "CENTER"

    return "RIGHT"


def get_vertical_position(center_y, image_height):
    """Determine whether an object is above, center or below."""

    if center_y < image_height / 3:
        return "ABOVE"

    elif center_y < (2 * image_height / 3):
        return "CENTER"

    return "BELOW"


def estimate_proximity(box_width, box_height, image_width, image_height):
    """
    Estimate proximity using the object's bounding-box size.

    IMPORTANT:
    This is only an image-based approximation.
    It is NOT real-world distance measurement.
    """

    object_area = box_width * box_height
    image_area = image_width * image_height

    area_ratio = object_area / image_area

    if area_ratio > 0.25:
        return "NEAR"

    elif area_ratio > 0.08:
        return "MEDIUM"

    return "FAR"


def determine_risk(object_name, proximity, horizontal):
    """Determine a basic vision-level risk."""

    if object_name in HIGH_RISK_OBJECTS:

        if proximity == "NEAR":
            return "HIGH"

        elif proximity == "MEDIUM":
            return "MEDIUM"

        return "LOW"

    if object_name in MEDIUM_RISK_OBJECTS:

        if proximity == "NEAR":
            return "MEDIUM"

        return "LOW"

    return "LOW"


def create_message(object_name, horizontal, proximity, risk):
    """Create a simple message for MonSight."""

    if risk == "HIGH":
        return (
            f"Warning: {object_name} detected {proximity.lower()} "
            f"on the {horizontal.lower()}."
        )

    elif risk == "MEDIUM":
        return (
            f"Caution: {object_name} detected {proximity.lower()} "
            f"on the {horizontal.lower()}."
        )

    return (
        f"{object_name} detected {proximity.lower()} "
        f"on the {horizontal.lower()}."
    )


def analyze_image(image_path):
    """
    Analyze an image and return structured information
    that can later be used by the MonSight Agent.
    """

    results = model(image_path)

    detections = []

    for result in results:

        image_height, image_width = result.orig_shape

        for box in result.boxes:

            confidence = float(box.conf[0])

            # Ignore weak detections
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            class_id = int(box.cls[0])
            object_name = model.names[class_id]

            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            box_width = x2 - x1
            box_height = y2 - y1

            # Center point
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # Position
            horizontal = get_horizontal_position(
                center_x,
                image_width
            )

            vertical = get_vertical_position(
                center_y,
                image_height
            )

            # Approximate proximity
            proximity = estimate_proximity(
                box_width,
                box_height,
                image_width,
                image_height
            )

            # Risk
            risk = determine_risk(
                object_name,
                proximity,
                horizontal
            )

            # Human-readable message
            message = create_message(
                object_name,
                horizontal,
                proximity,
                risk
            )

            detection = {
                "object": object_name,
                "confidence": round(confidence, 2),
                "horizontal_position": horizontal,
                "vertical_position": vertical,
                "proximity": proximity,
                "risk": risk,
                "message": message,
            }

            detections.append(detection)

    return {
        "status": "success",
        "objects_detected": len(detections),
        "detections": detections,
    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("        MONSIGHT VISION TOOL")
    print("========================================")

    image_path = input("\nEnter image path: ")

    try:

        result = analyze_image(image_path)

        print("\nVision Analysis Complete")
        print("----------------------------------------")

        print(
            "Objects detected:",
            result["objects_detected"]
        )

        print()

        for detection in result["detections"]:

            print(
                f"Object      : {detection['object']}"
            )

            print(
                f"Confidence  : {detection['confidence']}"
            )

            print(
                f"Horizontal  : {detection['horizontal_position']}"
            )

            print(
                f"Vertical    : {detection['vertical_position']}"
            )

            print(
                f"Proximity   : {detection['proximity']}"
            )

            print(
                f"Risk        : {detection['risk']}"
            )

            print(
                f"Message     : {detection['message']}"
            )

            print("----------------------------------------")

    except Exception as error:

        print("\nERROR:")
        print(error)