import streamlit as st
from PIL import Image

from src.preprocessing import preprocess_document

st.set_page_config(
    page_title="BharatID Guard",
    page_icon="In",
    layout="wide"
)

st.title(" BharatID Guard")

st.subheader("AI-Based Identity & Document Screening System")

st.write(
    "Upload an identity or travel document to begin the verification process."
)


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

    st.info(
        "Phase 1 processing complete. "
        "The processed image will be used by the OCR module in Phase 2."
    )