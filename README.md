🇮🇳 BharatID Guard

AI-Assisted Identity & Document Screening System

BharatID Guard is a prototype identity and document screening system designed to help identify suspicious identity documents through multiple verification layers. It combines OCR, document validation, database verification, tampering screening, face verification, and risk scoring into a single Streamlit dashboard.

🚀 Features
📄 Document Upload — Upload identity document images.
🖼️ Image Preprocessing — Improve image quality using OpenCV.
🔍 OCR Extraction — Extract text using PaddleOCR.
📑 Document Detection — Identify supported document types.
📝 Field Extraction — Extract important fields such as name, DOB and document number.
✅ Document Validation — Validate extracted information using predefined rules.
🗄️ Database Verification — Check records against a prototype SQLite database.
🔬 Tampering Screening — Use ELA and image analysis to identify suspicious regions.
👤 Face Verification — Compare the document photograph with a presented person's photograph using DeepFace and FaceNet512.
⚠️ Risk Scoring — Combine multiple verification signals into a 0–100 risk score.
📊 Final Dashboard — Display verification status, risk level and reasons.
🔄 System Flow
Document Upload
       ↓
Image Preprocessing
       ↓
OCR
       ↓
Document Detection
       ↓
Field Extraction
       ↓
Validation
       ↓
Database Check
       ↓
Tampering Screening
       ↓
Face Verification
       ↓
Risk Engine
       ↓
Final Screening Result
🛠️ Technology Stack
Technology	Purpose
Python	Core development
Streamlit	Web dashboard
OpenCV	Image preprocessing & analysis
Pillow	Image handling
NumPy	Numerical/image operations
PaddleOCR	AI-based text extraction
Regex	Structured field extraction
SQLite	Prototype verification database
DeepFace	Face verification
FaceNet512	Deep-learning face model
ELA	Image-forensic tampering screening
📁 Project Structure
BharatID-Guard/
│
├── app.py
├── requirements.txt
│
└── src/
    ├── __init__.py
    ├── preprocessing.py
    ├── ocr.py
    ├── document_detector.py
    ├── field_extractor.py
    ├── validator.py
    ├── database.py
    ├── tampering.py
    ├── face_verification.py
    └── risk_engine.py
Module Overview

app.py
Main application that connects all modules and manages the Streamlit dashboard.

preprocessing.py
Processes and enhances document images before OCR.

ocr.py
Uses PaddleOCR to extract text from the document.

document_detector.py
Identifies the type of uploaded document.

field_extractor.py
Extracts structured information such as name, DOB and document number.

validator.py
Checks extracted information against predefined rules.

database.py
Handles the prototype SQLite verification database.

tampering.py
Performs image-forensic tampering screening using ELA and suspicious-region analysis.

face_verification.py
Performs face comparison using DeepFace and FaceNet512.

risk_engine.py
Combines the verification results and generates the final risk score.

📊 Risk Levels
0 – 34    → 🟢 LOW
35 – 69   → 🟠 MEDIUM
70 – 100  → 🔴 HIGH
Important

A HIGH risk score does not automatically mean the document is fake.

It means the document has enough suspicious signals to require manual verification.

🤖 Where AI Is Used

BharatID Guard is a hybrid AI-assisted system.

AI/deep learning is used in:

PaddleOCR for text recognition
DeepFace + FaceNet512 for face verification

Other components such as validation, database checking and risk scoring are primarily rule-based.

ELA-based tampering screening is an image-forensic technique, not a trained AI model.

🔐 Database

The current project uses a mock SQLite database for demonstration and testing.

It does not claim direct access to:

Government databases
Aadhaar database
PAN database
Passport Seva database
Immigration databases

For real-world deployment, authorized APIs and secure institutional verification systems would be required.

⚠️ Limitations
Current database is a prototype/mock database.
Tampering detection is currently heuristic/image-forensic based.
Face verification depends on image quality, lighting and pose.
Current document support is limited.
Production deployment would require extensive testing and security validation.
🔮 Future Enhancements
Authorized government/API integration
Advanced AI-based forgery detection
Live camera face verification
Liveness detection
QR/barcode verification
Digital-signature verification
More Indian document types
Multilingual OCR
Secure cloud deployment
Audit logs and automated alerts
▶️ Installation

Clone the repository:

git clone <your-repository-url>
cd BharatID-Guard

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

The application will open in your browser.

🎯 Project Objective

To provide a multi-layer identity-document screening system that helps operators detect suspicious documents faster and prioritize cases for manual verification.
