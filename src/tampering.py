import cv2
import numpy as np


def detect_suspicious_regions(image, validation_results=None):

    # ---------------------------------------------------------
    # Convert PIL image to OpenCV
    # ---------------------------------------------------------

    img = np.array(image)

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # ---------------------------------------------------------
    # Resize large images
    # ---------------------------------------------------------

    max_width = 1200

    if img.shape[1] > max_width:

        scale = max_width / img.shape[1]

        new_width = max_width
        new_height = int(img.shape[0] * scale)

        img = cv2.resize(
            img,
            (new_width, new_height)
        )

    # ---------------------------------------------------------
    # JPEG Recompression
    # ---------------------------------------------------------

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
        return img, img, "LOW", 0, []

    recompressed = cv2.imdecode(
        encoded,
        cv2.IMREAD_COLOR
    )

    # ---------------------------------------------------------
    # ELA
    # ---------------------------------------------------------

    difference = cv2.absdiff(
        img,
        recompressed
    )

    gray = cv2.cvtColor(
        difference,
        cv2.COLOR_BGR2GRAY
    )

    ela = cv2.normalize(
        gray,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # Smooth small noise
    smooth = cv2.GaussianBlur(
        ela,
        (7, 7),
        0
    )

    # ---------------------------------------------------------
    # Detect high-anomaly regions
    # ---------------------------------------------------------

    mean_value = np.mean(smooth)
    std_value = np.std(smooth)

    percentile_value = np.percentile(
        smooth,
        95
    )

    threshold_value = max(
        percentile_value,
        mean_value + (1.2 * std_value)
    )

    _, mask = cv2.threshold(
        smooth,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    # ---------------------------------------------------------
    # Remove small noise
    # ---------------------------------------------------------

    kernel = np.ones(
        (7, 7),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ---------------------------------------------------------
    # Find suspicious regions
    # ---------------------------------------------------------

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    suspicious_image = img.copy()

    suspicious_regions = []

    total_area = img.shape[0] * img.shape[1]

    suspicious_area = 0

    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore tiny regions
        if area < 150:
            continue

        x, y, w, h = cv2.boundingRect(
            contour
        )

        suspicious_area += area

        suspicious_regions.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "area": area
        })

        # Highlight suspicious region
        cv2.rectangle(
            suspicious_image,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            3
        )

    # ---------------------------------------------------------
    # Calculate image anomaly percentage
    # ---------------------------------------------------------

    anomaly_percentage = (
        suspicious_area / total_area
    ) * 100

    # ---------------------------------------------------------
    # Tampering score
    # ---------------------------------------------------------

    score = 0

    evidence = []

    # Image anomaly
    if anomaly_percentage >= 0.3:

        score += 25

        evidence.append(
            "Multiple image-forensic anomaly regions detected."
        )

    elif anomaly_percentage >= 0.1:

        score += 10

        evidence.append(
            "Minor image-forensic anomalies detected."
        )

    # Number of regions
    region_count = len(suspicious_regions)

    if region_count >= 5:

        score += 20

        evidence.append(
            f"{region_count} suspicious regions detected."
        )

    elif region_count >= 2:

        score += 10

        evidence.append(
            f"{region_count} potentially suspicious regions detected."
        )

    # ---------------------------------------------------------
    # Validation failures
    # ---------------------------------------------------------

    if validation_results:

        failed_checks = [
            result
            for result in validation_results
            if result.get("status") == "FAIL"
        ]

        if failed_checks:

            score += min(
                len(failed_checks) * 20,
                40
            )

            evidence.append(
                f"{len(failed_checks)} document validation check(s) failed."
            )

    # ---------------------------------------------------------
    # Limit score
    # ---------------------------------------------------------

    score = min(score, 100)

    # ---------------------------------------------------------
    # Risk classification
    # ---------------------------------------------------------

    if score >= 60:

        risk = "HIGH"

    elif score >= 30:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    # ---------------------------------------------------------
    # If nothing detected
    # ---------------------------------------------------------

    if not evidence:

        evidence.append(
            "No significant image-forensic anomaly detected."
        )

    return (
        suspicious_image,
        ela,
        risk,
        score,
        evidence
    )