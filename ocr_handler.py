import pytesseract
from PIL import Image
import numpy as np
import io
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_file):
    image_bytes = image_file.read()
    image_file.seek(0)

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(img)

    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    max_size = 2000
    h, w = gray.shape
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        gray = cv2.resize(
            gray,
            (int(w * scale), int(h * scale)),
            interpolation=cv2.INTER_AREA
        )

    return gray


def extract_text_from_image(image_file):
    try:
        img = preprocess_image(image_file)

        text = pytesseract.image_to_string(
            img,
            config="--oem 3 --psm 6"
        )

        if len(text.strip()) < 30:
            text = pytesseract.image_to_string(
                img,
                config="--oem 3 --psm 11"
            )

        return text.strip(), 1.0 if text.strip() else 0.0

    except Exception as e:
        print(f"OCR error: {str(e)}")
        return "", 0.0
