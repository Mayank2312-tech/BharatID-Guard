import streamlit as st
from PIL import Image

from src.ocr import extract_text
from src.preprocessing import preprocess_document
from src.document_detector import detect_document_type
from src.field_extractor import (
    extract_pan_fields,
    extract_passport_fields
)
from src.validator import (
    validate_pan,
    validate_passport
)
from src.database import (
    create_database,
    add_sample_data,
    check_document
)
from src.tampering import detect_suspicious_regions


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BharatID Guard",
    page_icon="🇮🇳",
    layout="wide"
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_database()
add_sample_data()


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "ocr_result" not in st.session_state:
    st.session_state.ocr_result = []

if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = "Unknown Document"

if "fields" not in st.session_state:
    st.session_state.fields = {}

if "validation_results" not in st.session_state:
    st.session_state.validation_results = []

if "database_result" not in st.session_state:
    st.session_state.database_result = None

if "tampering_result" not in st.session_state:
    st.session_state.tampering_result = None


# =========================================================
# HEADER
# =========================================================

st.title("🇮🇳 BharatID Guard")

st.subheader(
    "AI-Based Identity & Document Screening System"
)

st.write(
    "Upload an identity or travel document to begin "
    "the verification process."
)


# =========================================================
# DOCUMENT TYPES
# =========================================================

with st.expander("📋 Documents Can Be Verified"):

    st.write("""
    1. Aadhaar Card
    2. PAN Card
    3. Voter ID Card
    4. Indian Passport
    5. Driving Licence
    6. Ration Card
    7. Birth Certificate
    8. NREGS Job Card
    9. Property Tax Receipt
    10. Electricity Bill
    11. Bank Passbook
    """)


st.divider()


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

st.header("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a document image",
    type=["jpg", "jpeg", "png"]
)


# =========================================================
# DOCUMENT PROCESSING
# =========================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.success("Document uploaded successfully!")

    # -----------------------------------------------------
    # PREPROCESSING
    # -----------------------------------------------------

    original, processed = preprocess_document(image)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Original Document")

        st.image(
            image,
            caption="Uploaded Document",
            use_container_width=True
        )

    with col2:

        st.subheader("Preprocessed Document")

        st.image(
            processed,
            caption="Processed Image",
            use_container_width=True,
            clamp=True
        )


    # =====================================================
    # OCR
    # =====================================================

    st.divider()

    st.header("🔍 OCR & Information Extraction")

    if st.button(
        "Extract Document Text",
        type="primary"
    ):

        with st.spinner("Reading document..."):

            image_path = "temp_document.png"

            image.save(image_path)

            try:

                ocr_result = extract_text(image_path)

                # Save OCR result
                st.session_state.ocr_result = ocr_result

                # Combine OCR text
                raw_text = "\n".join(
                    item["text"]
                    for item in ocr_result
                )

                st.session_state.raw_text = raw_text

                # Detect document
                document_type = detect_document_type(
                    raw_text
                )

                st.session_state.document_type = document_type


                # -------------------------------------------------
                # FIELD EXTRACTION
                # -------------------------------------------------

                if document_type == "PAN Card":

                    fields = extract_pan_fields(
                        raw_text
                    )

                elif document_type == "Indian Passport":

                    fields = extract_passport_fields(
                        raw_text
                    )

                else:

                    fields = {}


                st.session_state.fields = fields


                # -------------------------------------------------
                # VALIDATION
                # -------------------------------------------------

                if document_type == "PAN Card":

                    validation_results = validate_pan(
                        fields
                    )

                elif document_type == "Indian Passport":

                    validation_results = validate_passport(
                        fields
                    )

                else:

                    validation_results = []


                st.session_state.validation_results = (
                    validation_results
                )


                # -------------------------------------------------
                # DATABASE CHECK
                # -------------------------------------------------

                document_number = None

                if document_type == "PAN Card":

                    document_number = fields.get(
                        "PAN Number"
                    )

                elif document_type == "Indian Passport":

                    document_number = fields.get(
                        "Passport Number"
                    )


                if (
                    document_number
                    and document_number != "Not detected"
                ):

                    database_result = check_document(
                        document_number
                    )

                    st.session_state.database_result = (
                        database_result
                    )

                else:

                    st.session_state.database_result = None


                st.success(
                    "OCR processing completed successfully!"
                )


            except Exception as e:

                st.error(
                    f"Error processing document: {str(e)}"
                )


    # =====================================================
    # DISPLAY OCR RESULT
    # =====================================================

    if st.session_state.ocr_result:

        st.subheader("📄 Extracted Text")

        for item in st.session_state.ocr_result:

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    item["text"]
                )

            with col2:

                st.write(
                    f"{item['confidence']}%"
                )


    # =====================================================
    # DOCUMENT TYPE
    # =====================================================

    if (
        st.session_state.document_type
        != "Unknown Document"
    ):

        st.divider()

        st.subheader("📑 Document Type")

        st.success(
            st.session_state.document_type
        )


    # =====================================================
    # EXTRACTED INFORMATION
    # =====================================================

    if st.session_state.fields:

        st.divider()

        st.subheader("📋 Extracted Information")

        for field, value in (
            st.session_state.fields.items()
        ):

            st.write(
                f"**{field}:** {value}"
            )


    # =====================================================
    # DOCUMENT VALIDATION
    # =====================================================

    if st.session_state.validation_results:

        st.divider()

        st.header("✅ Document Validation")

        failed_checks = 0

        for result in (
            st.session_state.validation_results
        ):

            if result["status"] == "PASS":

                st.success(
                    f"✓ {result['check']}: "
                    f"{result['message']}"
                )

            else:

                failed_checks += 1

                st.error(
                    f"✗ {result['check']}: "
                    f"{result['message']}"
                )


        st.divider()


        if failed_checks == 0:

            st.success(
                "🟢 DOCUMENT APPEARS VALID"
            )

        else:

            st.warning(
                "🟠 DOCUMENT REQUIRES MANUAL REVIEW"
            )


    # =====================================================
    # DATABASE VERIFICATION
    # =====================================================

    if (
        st.session_state.fields
        and st.session_state.document_type
        != "Unknown Document"
    ):

        st.divider()

        st.header("🗄️ Verification Database")

        document_number = None

        if (
            st.session_state.document_type
            == "PAN Card"
        ):

            document_number = (
                st.session_state.fields.get(
                    "PAN Number"
                )
            )

        elif (
            st.session_state.document_type
            == "Indian Passport"
        ):

            document_number = (
                st.session_state.fields.get(
                    "Passport Number"
                )
            )


        if (
            document_number
            and document_number != "Not detected"
        ):

            st.write(
                f"Searching database for: "
                f"**{document_number}**"
            )


            database_result = (
                st.session_state.database_result
            )


            if database_result:

                (
                    db_type,
                    db_number,
                    holder_name,
                    status
                ) = database_result


                if status == "VALID":

                    st.success(
                        f"🟢 Database Status: {status}"
                    )

                elif status == "EXPIRED":

                    st.warning(
                        f"🟠 Database Status: {status}"
                    )

                elif status == "FLAGGED":

                    st.error(
                        f"🔴 Database Status: {status}"
                    )


                st.write(
                    f"**Record Holder:** "
                    f"{holder_name}"
                )


            else:

                st.info(
                    "🔵 Document number not found "
                    "in verification database."
                )


        else:

            st.warning(
                "Document number could not be extracted."
            )


    # =====================================================
    # TAMPERING DETECTION
    # =====================================================
# =====================================================
# TAMPERING DETECTION
# =====================================================

if st.session_state.ocr_result:

    st.divider()

    st.header("🛡️ Tampering Detection")

    if st.button("Analyze Document for Tampering"):

        with st.spinner("Analyzing document..."):

            try:

                (
                    suspicious_image,
                    ela_image,
                    risk,
                    tampering_score,
                    tampering_evidence
                ) = detect_suspicious_regions(
                    image,
                    st.session_state.validation_results
                )

                # Save result
                st.session_state.tampering_result = (
                    suspicious_image,
                    ela_image,
                    risk,
                    tampering_score,
                    tampering_evidence
                )

            except Exception as e:

                st.error(
                    f"Tampering analysis error: {str(e)}"
                )


# =====================================================
# DISPLAY TAMPERING RESULT
# =====================================================

if st.session_state.tampering_result:

    (
        suspicious_image,
        ela_image,
        risk,
        tampering_score,
        tampering_evidence
    ) = st.session_state.tampering_result

    st.subheader("🔎 Tampering Analysis")

    # -------------------------------------------------
    # SCORE
    # -------------------------------------------------

    st.metric(
        label="Tampering Screening Score",
        value=f"{tampering_score}/100"
    )

    # -------------------------------------------------
    # RISK LEVEL
    # -------------------------------------------------

    if risk == "LOW":

        st.success(
            "🟢 Tampering Risk: LOW"
        )

    elif risk == "MEDIUM":

        st.warning(
            "🟠 Tampering Risk: MEDIUM"
        )

    else:

        st.error(
            "🔴 Tampering Risk: HIGH"
        )

    # -------------------------------------------------
    # EVIDENCE
    # -------------------------------------------------

    st.subheader("🔎 Analysis Evidence")

    if tampering_evidence:

        for evidence in tampering_evidence:

            st.write(
                f"• {evidence}"
            )

    else:

        st.write(
            "No significant anomalies detected."
        )

    # -------------------------------------------------
    # IMAGES
    # -------------------------------------------------

    st.subheader("🖼️ Forensic Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            suspicious_image,
            caption="Suspicious Regions",
            use_container_width=True
        )

    with col2:

        st.image(
            ela_image,
            caption="ELA Analysis",
            use_container_width=True,
            clamp=True
        )

    # -------------------------------------------------
    # DISCLAIMER
    # -------------------------------------------------

    st.info(
        "This analysis identifies image-forensic "
        "anomalies and should be treated as a screening "
        "signal, not definitive proof of document forgery. "
        "Final verification should be performed by an "
        "authorized officer."
    )