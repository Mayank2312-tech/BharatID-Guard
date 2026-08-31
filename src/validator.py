import re
from datetime import datetime


def validate_pan(fields):

    results = []

    pan = fields.get("PAN Number", "")
    dob = fields.get("Date of Birth", "")
    name = fields.get("Name", "")

    # PAN format
    if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan.upper()):
        results.append({
            "check": "PAN Format",
            "status": "PASS",
            "message": "PAN number format is valid."
        })
    else:
        results.append({
            "check": "PAN Format",
            "status": "FAIL",
            "message": "Invalid PAN number format."
        })

    # Name
    if name and name != "Not detected":
        results.append({
            "check": "Name",
            "status": "PASS",
            "message": "Name detected successfully."
        })
    else:
        results.append({
            "check": "Name",
            "status": "FAIL",
            "message": "Name could not be detected."
        })

    # DOB
    try:
        datetime.strptime(dob, "%d/%m/%Y")

        results.append({
            "check": "Date of Birth",
            "status": "PASS",
            "message": "Date of birth format is valid."
        })

    except ValueError:
        results.append({
            "check": "Date of Birth",
            "status": "FAIL",
            "message": "Invalid or missing date of birth."
        })

    return results


def validate_passport(fields):

    results = []

    passport = fields.get("Passport Number", "")
    dob = fields.get("Date of Birth", "")
    issue = fields.get("Date of Issue", "")
    expiry = fields.get("Date of Expiry", "")

    # Passport number
    if re.fullmatch(r"[A-Z][0-9]{7}", passport.upper()):

        results.append({
            "check": "Passport Number",
            "status": "PASS",
            "message": "Passport number format is valid."
        })

    else:

        results.append({
            "check": "Passport Number",
            "status": "FAIL",
            "message": "Invalid passport number format."
        })

    # Date validation
    try:

        dob_date = datetime.strptime(dob, "%d/%m/%Y")
        issue_date = datetime.strptime(issue, "%d/%m/%Y")
        expiry_date = datetime.strptime(expiry, "%d/%m/%Y")

        today = datetime.today()

        if dob_date >= today:

            results.append({
                "check": "Date of Birth",
                "status": "FAIL",
                "message": "Date of birth is invalid."
            })

        else:

            results.append({
                "check": "Date of Birth",
                "status": "PASS",
                "message": "Date of birth is valid."
            })

        if issue_date < expiry_date:

            results.append({
                "check": "Issue / Expiry Date",
                "status": "PASS",
                "message": "Issue date is before expiry date."
            })

        else:

            results.append({
                "check": "Issue / Expiry Date",
                "status": "FAIL",
                "message": "Issue date must be before expiry date."
            })

        if expiry_date >= today:

            results.append({
                "check": "Expiry",
                "status": "PASS",
                "message": "Document is currently valid."
            })

        else:

            results.append({
                "check": "Expiry",
                "status": "FAIL",
                "message": "Document has expired."
            })

    except ValueError:

        results.append({
            "check": "Dates",
            "status": "FAIL",
            "message": "One or more dates could not be verified."
        })

    return results