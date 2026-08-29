from paddleocr import PaddleOCR


# Initialize OCR
ocr = PaddleOCR(lang="en",enable_mkldnn=False)


def extract_text(image_path):

    results = ocr.predict(image_path)

    extracted_lines = []

    for result in results:

        # Convert result to dictionary
        data = result.json

        # Extract OCR recognition data
        if isinstance(data, str):
            import json
            data = json.loads(data)

        res = data.get("res", data)

        rec_texts = res.get("rec_texts", [])
        rec_scores = res.get("rec_scores", [])

        for text, score in zip(rec_texts, rec_scores):

            extracted_lines.append({
                "text": text,
                "confidence": round(float(score) * 100, 2)
            })

    return extracted_lines