import cv2
import numpy as np


def preprocess_document(image):
    """
    Preprocess an uploaded document image
    for further analysis and OCR.
    """

    # Convert PIL image to NumPy array
    image = np.array(image)

    # Convert RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    # Improve contrast
    enhanced = cv2.equalizeHist(denoised)

    return image, enhanced