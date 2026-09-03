import cv2
import numpy as np


def detect_suspicious_regions(image):

    # Convert image to OpenCV format
    img = np.array(image)

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize for consistent processing
    scale = 800 / img.shape[1]

    if scale < 1:
        new_width = 800
        new_height = int(img.shape[0] * scale)

        img = cv2.resize(
            img,
            (new_width, new_height)
        )

    # JPEG recompression
    encode_param = [
        int(cv2.IMWRITE_JPEG_QUALITY),
        90
    ]

    success, encoded = cv2.imencode(
        ".jpg",
        img,
        encode_param
    )

    if not success:
        return img, None, 0

    recompressed = cv2.imdecode(
        encoded,
        cv2.IMREAD_COLOR
    )

    # Calculate ELA difference
    difference = cv2.absdiff(
        img,
        recompressed
    )

    gray = cv2.cvtColor(
        difference,
        cv2.COLOR_BGR2GRAY
    )

    # Improve visibility
    ela = cv2.normalize(
        gray,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # Threshold suspicious regions
    threshold_value = np.mean(ela) + (1.5 * np.std(ela))

    _, mask = cv2.threshold(
        ela,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    # Remove tiny noise
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # Find suspicious contours
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    suspicious = img.copy()

    suspicious_area = 0

    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore extremely small regions
        if area > 100:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            cv2.rectangle(
                suspicious,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            suspicious_area += area

    total_area = img.shape[0] * img.shape[1]

    suspicious_percentage = (
        suspicious_area / total_area
    ) * 100

    # Risk classification
    if suspicious_percentage < 0.5:
        risk = "LOW"

    elif suspicious_percentage < 2:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    return suspicious, ela, risk