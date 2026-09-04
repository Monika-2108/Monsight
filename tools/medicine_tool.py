import re
import cv2
import pytesseract
import pyttsx3


class MedicineTool:

    def __init__(self):
        self.engine = pyttsx3.init()

    def read_medicine_label(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            return {
                "status": "error",
                "message": "Unable to read the image."
            }

        # Preprocess image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2)

        # OCR
        text = pytesseract.image_to_string(gray)

        text = text.strip()

        if not text:
            return {
                "status": "error",
                "message": "No readable medicine information was detected."
            }

        # Extract medicine name
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        medicine_name = lines[0] if lines else "Not detected"

        # Extract strength
        strength_match = re.search(
            r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml)\b",
            text,
            re.IGNORECASE
        )

        strength = (
            strength_match.group(0)
            if strength_match
            else "Not detected"
        )

        # Extract expiry date
        expiry_match = re.search(
            r"(?:EXP|EXPIRY|EXP\.?)\s*[:\-]?\s*"
            r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}"
            r"|\d{1,2}[\/\-]\d{2,4}"
            r"|\d{2,4}[\/\-]\d{1,2})",
            text,
            re.IGNORECASE
        )

        expiry = (
            expiry_match.group(1)
            if expiry_match
            else "Not detected"
        )

        result = {
            "status": "success",
            "medicine_name": medicine_name,
            "strength": strength,
            "expiry": expiry,
            "label_text": text
        }

        # Safety message
        message = (
            "Medicine label information has been read. "
            "Please verify the information with a doctor or pharmacist "
            "before using the medicine."
        )

        self.engine.say(message)
        self.engine.runAndWait()

        return result


if __name__ == "__main__":

    tool = MedicineTool()

    image_path = input(
        "Enter the path of the medicine label image: "
    )

    result = tool.read_medicine_label(image_path)

    print("\n===== MONSIGHT MEDICINE TOOL =====")

    if result["status"] == "success":

        print("Medicine Name:", result["medicine_name"])
        print("Strength:", result["strength"])
        print("Expiry:", result["expiry"])

        print("\nDetected Label Text:")
        print(result["label_text"])

    else:
        print("Error:", result["message"])