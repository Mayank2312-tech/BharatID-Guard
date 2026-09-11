# 🇮🇳 BharatID Guard

### AI-Assisted Identity & Document Screening System

> A multi-layer identity document screening system that combines OCR, document validation, database verification, tampering screening, face verification, and risk scoring to identify suspicious documents.

---

## 🚀 Overview

**BharatID Guard** is a prototype designed to assist authorized personnel in screening identity documents quickly and systematically.

Instead of depending on a single verification method, the system combines multiple verification layers and generates an overall **risk score**.

The system can help identify:

- Invalid document information
- Expired or flagged records
- Potential document manipulation
- Possible identity mismatch
- Suspicious verification patterns

---

## 🔄 System Workflow

| Step | Module | Description |
|---|---|---|
| 1 | 📤 Document Upload | Upload identity document |
| 2 | 🖼️ Image Preprocessing | Improve image quality |
| 3 | 🔍 OCR Extraction | Extract text using PaddleOCR |
| 4 | 📄 Document Detection | Identify document type |
| 5 | 🟢 Validation | Validate extracted information |
| 6 | 🗄️ Database Verification | Compare with database records |
| 7 | ⚠️ Tampering Screening | Detect possible manipulation |
| 8 | 👤 Face Verification | Verify document face |
| 9 | 🚨 Risk Engine | Calculate risk level |
| 10 | 📊 Final Screening Result | Generate final result |


## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| 🐍 Language | Python |
| 🤖 OCR | PaddleOCR |
| 👁️ Image Processing | OpenCV |
| 👤 Face Verification | Face Matching / Verification |
| ⚙️ Backend | FastAPI, Uvicorn |
| 🗄️ Database | SQLite / PostgreSQL |
| 🎨 Frontend | HTML, CSS, JavaScript, Bootstrap |
| 🔧 Tools | Git, GitHub, VS Code |
| 📦 Libraries | NumPy, Pillow, python-dotenv |



## 📊 Risk Scoring

**🟢 LOW `0–34`** → Automated Pass

**🟠 MEDIUM `35–69`** → Manual Review

**🔴 HIGH `70–100`** → Manual Audit





## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/BharatID-Guard.git
cd BharatID-Guard

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
