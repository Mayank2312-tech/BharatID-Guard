import re


def extract_pan_fields(text):

    fields = {
        "Name": "Not detected",
        "Date of Birth": "Not detected",
        "PAN Number": "Not detected"
    }

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # PAN number
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    for line in lines:

        match = re.search(pan_pattern, line.upper())

        if match:
            fields["PAN Number"] = match.group()
            break

    # Date of birth
    date_pattern = r"\b\d{2}/\d{2}/\d{4}\b"

    for line in lines:

        match = re.search(date_pattern, line)

        if match:
            fields["Date of Birth"] = match.group()
            break

    # Name
    for i, line in enumerate(lines):

        if "GOVT. OF INDIA" in line.upper():

            if i + 1 < len(lines):
                fields["Name"] = lines[i + 1]

            break

    return fields


def extract_passport_fields(text):

    fields = {
        "Name": "Not detected",
        "Passport Number": "Not detected",
        "Nationality": "Not detected",
        "Date of Birth": "Not detected",
        "Gender": "Not detected",
        "Date of Issue": "Not detected",
        "Date of Expiry": "Not detected"
    }

    # Passport number
    passport_pattern = r"\b[A-Z][0-9]{7}\b"

    match = re.search(
        passport_pattern,
        text.upper()
    )

    if match:
        fields["Passport Number"] = match.group()

    # Dates
    dates = re.findall(
        r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
        text
    )

    if len(dates) >= 1:
        fields["Date of Birth"] = dates[0]

    if len(dates) >= 2:
        fields["Date of Issue"] = dates[1]

    if len(dates) >= 3:
        fields["Date of Expiry"] = dates[2]

    # Nationality
    if "INDIAN" in text.upper():
        fields["Nationality"] = "INDIAN"

    # Gender
    if re.search(r"\b(M|F)\b", text.upper()):
        fields["Gender"] = re.search(
            r"\b(M|F)\b",
            text.upper()
        ).group()

    return fields