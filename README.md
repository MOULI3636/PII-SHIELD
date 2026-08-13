🛡️ PII Shield

Enterprise-Style Document Privacy & PII Redaction Platform

<p align="center">

<strong>{=html}Detect → Classify → Replace → Validate → Review →
Export</strong>{=html}

</p>

<p align="center">

A Streamlit-based DOCX privacy platform for detecting PII, generating
consistent synthetic replacements, validating sanitized documents, and
reviewing results through an interactive dashboard.

</p>

📌 Overview

PII Shield is a document privacy application designed to identify
Personally Identifiable Information (PII) inside Microsoft Word
(.docx) documents.

It combines:

deterministic PII detection,

contextual heuristics,

synthetic replacement,

post-redaction validation,

interactive review,

audit information, and

downloadable sanitized documents.

The goal is to make document sanitization repeatable, inspectable, and
verifiable.

✨ Why PII Shield?

Sensitive information can appear in:

Paragraphs

Tables

Headers

Footers

Manually searching for these values is slow and difficult to audit.

PII Shield automates the complete workflow:

DOCX Document
      ↓
Document Structure Analysis
      ↓
PII Detection
      ↓
Entity Classification
      ↓
Synthetic Replacement
      ↓
Redacted DOCX
      ↓
Post-Redaction Validation
      ↓
Interactive Review
      ↓
Export

🚀 Key Features

1. 📄 DOCX PII Detection

Analyzes Microsoft Word documents across paragraphs, tables, headers,
and footers.

2. 🔐 Multiple PII Categories

Category        Example

PERSON        John Smith
EMAIL         john.smith@example.com
PHONE         +91 9876543210
DOB           15/08/1990
SSN           123-45-6789
CREDIT_CARD   4111 1111 1111 1111
IP_ADDRESS    192.168.1.25
ADDRESS       123 Example Road, Pune
COMPANY       ABC Technologies Limited

Detection uses deterministic patterns and contextual heuristics without
requiring a large external AI model.

3. 🔄 Consistent Synthetic Replacement

Detected values are replaced with synthetic values instead of simply
being deleted.

Original:
John Smith contacted john.smith@example.com.

Redacted:
Rahul Kapoor contacted rahul.kapoor@example.com.

This keeps the sanitized document readable while removing the original
sensitive values.

4. 🧪 Post-Redaction Validation

The redacted document is scanned again.

Redacted Document
       ↓
Second Detection Scan
       ├── 0 remaining → PASSED
       └── Remaining → REVIEW

This validation loop is one of the main differentiators of the project.

🖥️ Interactive Streamlit Dashboard

The application provides a structured privacy workspace.

🏠 Overview

DOCX upload

File information

Processing status

PII count

PII category count

Paragraph count

Table count

Processing time

Detection breakdown

Validation status

Redacted DOCX download

🔍 Detection Explorer

Review detected entities with:

Type      Original             Replacement             Start   End

EMAIL     original@email.com   synthetic@email.com       120   142
PHONE     +91 XXXXXXXX         +91 XXXXXXXX              350   363
COMPANY   ABC Limited          XYZ Industries            600   613

Detection results can also be exported as CSV.

🔄 Before / After

Compare:

Original Value
      ↓
Synthetic Replacement

🧪 Validation

Displays:

Total detected entities

Remaining entities

Validation status

Remaining records requiring review

📋 Audit Log

Records events such as:

Document uploaded

Document structure analyzed

PII detection completed

Entities processed

Synthetic replacements generated

Post-redaction validation completed

🧠 System Architecture

                    ┌──────────────────────┐
                    │     Streamlit UI     │
                    │       app.py         │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Redaction Engine    │
                    │ redaction_engine.py  │
                    └──────────┬───────────┘
                               ↓
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
        ┌────────────────┐          ┌────────────────┐
        │ PII Detectors  │          │ DOCX Processor │
        │  detectors.py  │          │                │
        └───────┬────────┘          └───────┬────────┘
                └─────────────┬─────────────┘
                              ↓
                    ┌──────────────────────┐
                    │ Synthetic Replacement│
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Validation / Re-scan │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Redacted DOCX + JSON │
                    └──────────────────────┘

📁 Project Structure

pii-shield/
│
├── app.py
├── main.py
├── redaction_engine.py
├── detectors.py
├── evaluator.py
├── test_detectors.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
└── output/
    └── .gitkeep

File Responsibilities

File                                Responsibility

app.py                            Streamlit UI, navigation,
dashboard, downloads

main.py                           Command-line execution

redaction_engine.py               Core DOCX processing pipeline

detectors.py                      PII detection and classification

evaluator.py                      Evaluation/reporting

test_detectors.py                 Detector verification

requirements.txt                  Python dependencies

🔄 End-to-End Processing

Step 1 --- Upload

The user uploads a .docx document.

Step 2 --- Read

The engine analyzes:

Paragraphs
Tables
Headers
Footers

Step 3 --- Detect

PII patterns search the document.

Examples:

EMAIL_PATTERN
PHONE_PATTERN

Step 4 --- Classify

Each detection is represented with information such as:

Type

Original value

Start position

End position

Step 5 --- Replace

A synthetic replacement is generated.

Original Entity
      ↓
Entity Type
      ↓
Replacement Generator
      ↓
Synthetic Entity

Step 6 --- Create Redacted DOCX

original.docx
      ↓
PII Shield
      ↓
PII_Shield_Redacted_original.docx

Step 7 --- Validate

The sanitized document is scanned again.

remaining_count == 0
        ↓
     PASSED

remaining_count > 0
        ↓
      REVIEW

Step 8 --- Report

The application provides:

Redacted DOCX

Detection results

Validation result

Audit information

CSV export

🛠️ Technology Stack

Technology                Purpose

Python                Core application
Streamlit             Interactive web interface
Pandas                Tabular result processing
Altair                Visualization
python-docx           DOCX processing
Regular Expressions   Pattern-based detection
JSON                  Detection/report serialization

⚙️ Installation

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/pii-shield.git
cd pii-shield

2. Create a Virtual Environment

Windows

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install Dependencies

pip install -r requirements.txt

▶️ Running the Application

Streamlit UI

streamlit run app.py

Open:

http://localhost:8501

Command Line

python main.py

Detector Tests

python test_detectors.py

🔐 Privacy & Security

PII Shield focuses on:

Deterministic detection

Synthetic replacement

Local document processing

Post-redaction validation

Auditable processing results

Important: Do not upload real confidential documents to a public
deployment without appropriate security controls.

⚠️ Limitations

PII detection is not a perfect privacy guarantee.

False Positives

A value can match a pattern without actually being PII.

False Negatives

PII may be missed when:

text is embedded in images,

text is represented as shapes,

formatting is unusual,

a value does not match an implemented detector.

Therefore:

Validation PASSED means that no remaining PII was detected by the
implemented rules. It does not mathematically guarantee that every
possible sensitive value has been removed.

🌟 What Makes PII Shield Different?

The project is designed as a complete privacy workflow rather than a
simple regex replacement script.

Detection
    +
Classification
    +
Synthetic Replacement
    +
Validation
    +
Auditability
    +
Interactive Review
    +
Export

⭐ Core Differentiator

The system does not simply assume that redaction succeeded.

It performs a second scan of the sanitized document and reports whether
detectable PII remains.

🚀 Future Enhancements

Planned possibilities include:

🎯 Confidence scores

🖼️ OCR-based PII detection

📑 PDF support

📊 XLSX / CSV support

⚙️ Custom organization-specific PII rules

🛡️ Strict / Balanced / Minimal redaction policies

📈 Analytics dashboard

📋 JSON / CSV / PDF audit exports

☁️ Deployment

Typical deployment architecture:

GitHub Repository
       ↓
Cloud Deployment
       ↓
Streamlit Application
       ↓
Public / Restricted URL

Before deploying confidential documents, review:

Data retention

Uploaded-file handling

Application logs

Access control

Authentication

Storage configuration

Organization privacy requirements

🧹 GitHub Security

Use a .gitignore such as:

venv/
.venv/

__pycache__/
*.py[cod]

.streamlit/secrets.toml

output/*
!output/.gitkeep

input/*
!input/.gitkeep

.env
.env.*

.vscode/
.idea/

.DS_Store
Thumbs.db

Never commit real confidential source documents to GitHub.

🧪 Testing Checklist

Before publishing:

app.py runs

main.py runs

Detector tests pass

DOCX upload works

PII detection works

Synthetic replacement works

Redacted DOCX opens correctly

Detection Explorer works

Before / After works

Validation works

Audit Log works

DOCX download works

CSV download works

requirements.txt is updated

.gitignore exists

No confidential documents are committed

🧩 Project Philosophy

Identify
   ↓
Understand
   ↓
Transform
   ↓
Verify
   ↓
Report

The objective is not merely to hide text.

The objective is to create a repeatable, inspectable, and verifiable
document sanitization workflow.

👨‍💻 Author

Mouli Banerjee

B.Tech Computer Science & Engineering
Data Science / Data Analytics Focus

📄 License

This project is intended for educational, portfolio, and demonstration
purposes unless a separate license is provided.

⭐ Project Status

Item             Status

Version          v1.0
Status           Active Development
Interface        Streamlit
Primary Format   Microsoft Word DOCX

Core Workflow

Upload
  ↓
Detect
  ↓
Classify
  ↓
Replace
  ↓
Validate
  ↓
Review
  ↓
Export

<p align="center">

<strong>{=html}🛡️ PII Shield --- Document Privacy & Redaction
Platform</strong>{=html}

</p>
