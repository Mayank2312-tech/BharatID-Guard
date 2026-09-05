import cv2
import numpy as np
import os
import tempfile

from deepface import DeepFace


def detect_and_crop_face(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read image.")

    # ---------------------------------------------------------
    # Upscale image
    # ---------------------------------------------------------

    image = cv2.resize(
        image,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # ---------------------------------------------------------
    # Face detection
    # ---------------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=4,
        minSize=(50, 50)
    )

    if len(faces) == 0:

        raise ValueError(
            "No face detected. "
            "Please use a clearer face image."
        )

    # ---------------------------------------------------------
    # Select largest face
    # ---------------------------------------------------------

    x, y, w, h = max(
        faces,
        key=lambda f: f[2] * f[3]
    )

    # ---------------------------------------------------------
    # Add margin
    # ---------------------------------------------------------

    margin_x = int(w * 0.30)
    margin_y = int(h * 0.30)

    x1 = max(0, x - margin_x)
    y1 = max(0, y - margin_y)

    x2 = min(
        image.shape[1],
        x + w + margin_x
    )

    y2 = min(
        image.shape[0],
        y + h + margin_y
    )

    face = image[
        y1:y2,
        x1:x2
    ]

    return face


def cosine_similarity(embedding1, embedding2):

    embedding1 = np.array(
        embedding1,
        dtype=np.float32
    )

    embedding2 = np.array(
        embedding2,
        dtype=np.float32
    )

    # Normalize
    embedding1 = embedding1 / (
        np.linalg.norm(embedding1) + 1e-10
    )

    embedding2 = embedding2 / (
        np.linalg.norm(embedding2) + 1e-10
    )

    similarity = np.dot(
        embedding1,
        embedding2
    )

    return float(similarity)


def verify_faces(
    document_image,
    person_image
):

    # ---------------------------------------------------------
    # Extract faces
    # ---------------------------------------------------------

    document_face = detect_and_crop_face(
        document_image
    )

    person_face = detect_and_crop_face(
        person_image
    )

    # ---------------------------------------------------------
    # Temporary files
    # ---------------------------------------------------------

    document_temp = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    person_temp = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    document_temp.close()
    person_temp.close()

    try:

        cv2.imwrite(
            document_temp.name,
            document_face
        )

        cv2.imwrite(
            person_temp.name,
            person_face
        )

        # -----------------------------------------------------
        # Generate ArcFace embeddings
        # -----------------------------------------------------

        document_embedding = DeepFace.represent(
            img_path=document_temp.name,
            model_name="ArcFace",
            detector_backend="skip",
            enforce_detection=False
        )[0]["embedding"]

        person_embedding = DeepFace.represent(
            img_path=person_temp.name,
            model_name="ArcFace",
            detector_backend="skip",
            enforce_detection=False
        )[0]["embedding"]

        # -----------------------------------------------------
        # Cosine similarity
        # -----------------------------------------------------

        similarity = cosine_similarity(
            document_embedding,
            person_embedding
        )

        # Convert cosine similarity to percentage
        similarity_percent = (
            (similarity + 1) / 2
        ) * 100

        # -----------------------------------------------------
        # Prototype threshold
        # -----------------------------------------------------

        # This is a prototype threshold,
        # NOT a calibrated biometric probability.

        if similarity >= 0.40:

            status = "MATCH"

        elif similarity >= 0.25:

            status = "REVIEW"

        else:

            status = "MISMATCH"

        return {

            "status": status,

            "similarity": round(
                similarity_percent,
                2
            ),

            "cosine_similarity": round(
                similarity,
                4
            ),

            "document_face": document_face,

            "person_face": person_face

        }

    finally:

        if os.path.exists(
            document_temp.name
        ):

            os.remove(
                document_temp.name
            )

        if os.path.exists(
            person_temp.name
        ):

            os.remove(
                person_temp.name
            )