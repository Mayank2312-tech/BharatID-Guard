import streamlit as st
from PIL import Image
from src.ocr import extract_text

from src.preprocessing import preprocess_document
from src.document_detector import detect_document_type
from src.field_extractor import (
    extract_pan_fields,
    extract_passport_fields
)

st.set_page_config(
    page_title="BharatID Guard",
    page_icon="In",
    layout="wide"
)

st.title(" BharatID Guard")

st.subheader("AI-Based Identity & Document Screening System")

st.write(
    "Upload an identity or travel document or any documents to begin the verification process.")

with st.expander("Documents Can be Verified: "):
    st.write("""
    1: Aadhaar Card
    2: PAN Card
    3: Voter ID Card
    4: Indian Passport
    5: Driving Licence
    6: Ration Card
    7: Birth Certificate
    8: NREGS Job Card
    9: Property Tax Receipt
    10: Electricity Bill
    11: Bank Passbook
    """)


st.divider()

st.header("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a document image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.success("Document uploaded successfully!")

    # Preprocess image
    original, processed = preprocess_document(image)

    st.divider()

    # Display images
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

st.divider()

st.header("🔍 OCR & Information Extraction")

if st.button("Extract Document Text"):

    with st.spinner("Reading document..."):

        image_path = "temp_document.png"

        image.save(image_path)

        try:

            ocr_result = extract_text(image_path)

            st.success("OCR processing completed!")

            if ocr_result:

                st.subheader("📄 Extracted Text")

                for item in ocr_result:

                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.write(item["text"])

                    with col2:
                        st.write(
                            f'{item["confidence"]}%'
                        )

            else:

                st.warning(
                    "No readable text was detected."
                )

        except Exception as e:

            st.error(f"OCR Error: {e}")