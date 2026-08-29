def detect_document_type(text):

    text_upper = text.upper()

    # PAN Card detection
    if (
        "INCOME TAX DEPARTMENT" in text_upper
        or "PERMANENT ACCOUNT NUMBER" in text_upper
    ):
        return "PAN Card"

    # Passport detection
    if (
        "PASSPORT" in text_upper
        or "REPUBLIC OF INDIA" in text_upper
    ):
        return "Indian Passport"

    return "Unknown Document"