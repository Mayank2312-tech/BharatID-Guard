def calculate_risk(
    validation_results=None,
    database_result=None,
    tampering_result=None,
    face_result=None
):

    score = 0
    reasons = []

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    if validation_results:

        failed = sum(
            1
            for result in validation_results
            if result.get("status") == "FAIL"
        )

        if failed > 0:

            points = min(failed * 15, 30)

            score += points

            reasons.append(
                f"{failed} document validation check(s) failed."
            )


    # -----------------------------------------
    # Database
    # -----------------------------------------

    if database_result:

        status = database_result[3]

        if status == "EXPIRED":

            score += 20

            reasons.append(
                "Document is marked as expired in the verification database."
            )

        elif status == "FLAGGED":

            score += 40

            reasons.append(
                "Document is flagged in the verification database."
            )


    # -----------------------------------------
    # Tampering
    # -----------------------------------------

    if tampering_result:

        tampering_risk = tampering_result[2]
        tampering_score = tampering_result[3]

        score += int(tampering_score * 0.3)

        if tampering_risk == "HIGH":

            reasons.append(
                "High tampering indicators detected."
            )

        elif tampering_risk == "MEDIUM":

            reasons.append(
                "Potential document manipulation detected."
            )


    # -----------------------------------------
    # Face Verification
    # -----------------------------------------

    if face_result:

        face_status = face_result.get("status")

        if face_status == "MISMATCH":

            score += 30

            reasons.append(
                "Document photograph and presented person may not match."
            )

        elif face_status == "ERROR":

            reasons.append(
                "Face verification could not be completed."
            )


    # -----------------------------------------
    # Limit score
    # -----------------------------------------

    score = min(score, 100)


    # -----------------------------------------
    # Risk level
    # -----------------------------------------

    if score >= 70:

        risk_level = "HIGH"

    elif score >= 35:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    # -----------------------------------------
    # Default explanation
    # -----------------------------------------

    if not reasons:

        reasons.append(
            "No significant verification issue detected."
        )


    return score, risk_level, reasons