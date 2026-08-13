🛡️ PII Shield

Enterprise-Style Document Privacy & PII Redaction Platform

Detect → Classify → Replace → Validate → Export

PII Shield is a document privacy application designed to identify
Personally Identifiable Information (PII) inside Microsoft Word
(.docx) documents, replace detected values with consistent synthetic
values, validate the sanitized document, and provide an interactive
interface for reviewing the results.

The project combines a Python redaction engine with a Streamlit
web interface so that document sanitization can be performed without
manually editing the source document.

✨ Why PII Shield?

Sensitive information can appear throughout business documents in
paragraphs, tables, headers, and footers. Manually finding and removing
these values is slow, inconsistent, and difficult to audit.

PII Shield automates the workflow:

DOCX Document
      │
      ▼
Document Structure Analysis
      │
      ▼
PII Detection
      │
      ├── Person / Name
      ├── Email
      ├── Phone
      ├── Address
      ├── DOB / Date
      ├── SSN
      ├── Credit Card
      ├── IP Address
      └── Company
      │
      ▼
Entity Classification
      │
      ▼
Synthetic Replacement
      │
      ▼
Redacted DOCX
      │
      ▼
Post-Redaction Validation
      │
      ▼
Interactive Report + Downloads

🚀 Key Features

1. DOCX PII Detection

Upload a Microsoft Word document and analyze its contents for
potentially sensitive information.

The processing pipeline can work across:

Document paragraphs

Tables

Headers

Footers

This is important because sensitive information is not necessarily
stored only in normal paragraph text.

2. Multiple PII Categories

The detector layer supports pattern/context-based detection for
categories such as:

Category          Example

PERSON / Name   John Smith
EMAIL           john.smith@example.com
PHONE           +91 9876543210
DOB / Date      15/08/1990
SSN             123-45-6789
CREDIT_CARD     4111 1111 1111 1111
IP_ADDRESS      192.168.1.25
ADDRESS         123 Example Road, Pune
COMPANY         ABC Technologies Limited

Detection is designed around deterministic patterns and contextual
heuristics rather than requiring a large external AI model.

3. Consistent Synthetic Replacement

Detected values are not simply deleted.

PII Shield generates replacement values so that the sanitized document
remains readable.

Example:

Original:
John Smith contacted john.smith@example.com.

Redacted:
Rahul Kapoor contacted rahul.kapoor@example.com.

The replacement approach is designed to preserve document usability
while removing the original sensitive value.

4. Post-Redaction Validation

A major part of the project is the second scan.

After creating the redacted document, the system checks the sanitized
result again.

Original Document
       │
       ▼
PII Detection
       │
       ▼
Replacement
       │
       ▼
Redacted Document
       │
       ▼
Second Detection Scan
       │
       ├── 0 remaining → PASSED
       │
       └── Remaining → REVIEW

This makes the system more than a simple find-and-replace script.

🖥️ Interactive Web Application

PII Shield includes a Streamlit interface designed as an
enterprise-style privacy dashboard.

Main workspace

The application provides:

Overview

The main dashboard provides:

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

Redacted document download

Detection Explorer

Provides a detailed view of detected entities:

Type      Original             Replacement             Start   End

EMAIL     original@email.com   synthetic@email.com       120   142
PHONE     +91 XXXXXXXX         +91 XXXXXXXX              350   363
COMPANY   ABC Limited          XYZ Industries            600   613

The results can also be exported as CSV.

Before / After

Provides a direct comparison between:

Original Value
       ↓
Synthetic Replacement

This makes the replacement process transparent.

Validation

Displays:

Total detected entities

Remaining entities

Validation status

Remaining entity records when manual review is required

Audit Log

Records important processing events such as:

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
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Redaction Engine    │
                         │ redaction_engine.py  │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
             ┌────────────────┐           ┌────────────────┐
             │ PII Detectors  │           │ DOCX Processor │
             │  detectors.py  │           │                │
             └───────┬────────┘           └───────┬────────┘
                     │                             │
                     └──────────────┬──────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Synthetic Replacement│
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Validation / Re-scan │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Redacted DOCX + JSON │
                         └──────────────────────┘

📁 Project Structure

Recommended repository structure:

PII-Redaction-Tool/
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
├── input/
│   └── sample.docx
│
└── output/
    ├── redacted_prospectus.docx
    └── detection_report.json

File Responsibilities

app.py

The Streamlit presentation layer.

Responsible for:

Upload interface

Navigation

Dashboard

Detection Explorer

Before / After review

Validation report

Audit log

Downloads

Visual styling

It calls the redaction engine instead of implementing the core redaction
logic itself.

main.py

Command-line execution layer.

Useful when the application needs to be executed without the Streamlit
UI.

Typical workflow:

Input DOCX
   ↓
main.py
   ↓
Redaction
   ↓
Output DOCX
   ↓
Detection report

redaction_engine.py

Core document-processing layer.

Responsible for connecting:

DOCX parsing

Detection

Entity processing

Replacement

Validation

Output generation

The Streamlit application calls:

redact_docx_bytes(...)

to process an uploaded document.

detectors.py

Detection layer.

Contains the logic/patterns used to identify potential PII categories.

Typical detection concepts include:

Regular expressions

Pattern validation

Contextual heuristics

Entity classification

evaluator.py

Evaluation/reporting utility.

Used to evaluate detection output and validate generated reports.

test_detectors.py

Detector verification script.

Used to check whether the detector layer can identify representative PII
examples such as:

John Smith
john.smith@example.com
+91 9876543210
15/08/1990
123-45-6789
4111 1111 1111 1111
192.168.1.25
123 Example Road, Pune
ABC Technologies Limited

🔄 End-to-End Processing Flow

Step 1 --- Upload

The user uploads:

document.docx

through the Streamlit interface.

Step 2 --- Read the document

The engine reads the DOCX structure.

It processes:

Paragraphs
Tables
Headers
Footers

Step 3 --- Detect

Detector patterns search the document for potential PII.

For example:

EMAIL_PATTERN
PHONE_PATTERN

and other category-specific detection rules.

Step 4 --- Classify

Every detected value is represented as an entity containing information
such as:

Type
Original Value
Start Position
End Position

Step 5 --- Replace

The system generates a synthetic replacement.

Conceptually:

Original Entity
       │
       ▼
Entity Type
       │
       ▼
Replacement Generator
       │
       ▼
Synthetic Entity

Step 6 --- Create the redacted document

The original DOCX is transformed into a sanitized DOCX.

Example:

input/
    original.docx

output/
    PII_Shield_Redacted_original.docx

Step 7 --- Validate

The sanitized content is scanned again.

If:

remaining_count == 0

the validation status is:

PASSED

Otherwise:

REVIEW

Step 8 --- Generate reports

The application exposes:

Redacted DOCX
Detection results
Validation result
Audit information
CSV export

🛠️ Technology Stack

Technology                     Purpose

Python                         Core application language
Streamlit                      Interactive web interface
Pandas                         Result processing and tabular data
Altair                         Detection visualization
python-docx                    DOCX document processing
Regular Expressions            Pattern-based PII detection
JSON                           Detection/report serialization
PyTest / Python test scripts   Detector verification

⚙️ Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/PII-Redaction-Tool.git
cd PII-Redaction-Tool

Replace YOUR_USERNAME with your GitHub username.

2. Create a virtual environment

Windows

python -m venv venv

Activate:

.\venv\Scripts\Activate.ps1

If PowerShell blocks activation:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate again:

.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

▶️ Run the Application

Start the Streamlit interface:

streamlit run app.py

Then open the local URL shown by Streamlit, normally:

http://localhost:8501

💻 Run Without the UI

For command-line processing:

python main.py

The CLI workflow can generate:

output/redacted_prospectus.docx
output/detection_report.json

🧪 Run Detector Tests

Run:

python test_detectors.py

A successful detector test should report the expected entity categories
and a total number of detected test entities.

📊 Example Processing Result

For a large DOCX document, the application can report statistics such
as:

PII Detected       343
PII Types            5
Paragraphs        1006
Tables               76
Processing        X.X s

The exact values depend on the uploaded document and detector rules.

🔐 Privacy & Security Design

PII Shield is designed around a simple principle:

Do not expose the original sensitive value unnecessarily.

The application focuses on:

Deterministic detection

Synthetic replacement

Local document processing

Post-redaction validation

Auditable processing results

For production deployment, additional controls should be added before
handling real confidential documents.

⚠️ Limitations

PII detection is not equivalent to perfect privacy assurance.

Pattern-based systems can produce:

False positives

A value may match a pattern but not actually be PII.

Example:

123-45-6789

may match an SSN pattern even when used as dummy data.

False negatives

PII may be missed when:

Formatting is unusual

Information is embedded in images

Text is represented as shapes

The document uses uncommon structures

A value does not match an existing detector pattern

Therefore:

Validation PASSED

should be interpreted as:

No remaining PII was detected by the implemented detection rules.

It does not mathematically guarantee that every possible sensitive
value has been removed.

🌟 What Makes This Project Different?

Instead of presenting the project as only:

"Regex that replaces PII"

PII Shield is structured as a complete privacy workflow:

Detection
   +
Classification
   +
Consistent Synthetic Replacement
   +
Validation
   +
Auditability
   +
Interactive Review
   +
Export

The important differentiator is the post-redaction validation loop.

The system does not simply assume that replacement succeeded.

It checks again.

🚀 Future Enhancements

Potential next versions could include:

1. Confidence Scores

Example:

EMAIL       99%
PHONE       98%
ADDRESS     86%
PERSON      78%

This would allow users to prioritize manual review.

2. OCR-Based PII Detection

Detect PII inside scanned documents and images.

Possible pipeline:

Image
  ↓
OCR
  ↓
Extracted Text
  ↓
PII Detection
  ↓
Redaction

3. PDF Support

Extend processing from:

DOCX

to:

PDF
TXT
CSV
XLSX

4. Custom PII Rules

Allow administrators to define organization-specific patterns.

Example:

EMPLOYEE_ID
CUSTOMER_ID
POLICY_NUMBER
INTERNAL_ACCOUNT_ID

5. Redaction Policies

Create configurable policies such as:

Strict
Balanced
Minimal

A strict policy could detect more potential PII at the cost of
additional false positives.

6. Analytics Dashboard

Track:

Documents processed
PII entities detected
Most common PII category
Validation pass rate
Average processing time

7. Enterprise Audit Export

Generate:

JSON
CSV
PDF

audit reports for compliance workflows.

☁️ Deployment

The Streamlit interface can be deployed to a cloud platform capable of
running Python applications.

Typical deployment flow:

GitHub Repository
       │
       ▼
Cloud Deployment
       │
       ▼
Streamlit Application
       │
       ▼
Public / Restricted URL

Before deploying confidential documents, review:

Data retention

Uploaded-file handling

Application logs

Access control

Authentication

Storage configuration

Organization privacy requirements

Do not use a public deployment for real confidential documents without
appropriate security controls.

🧹 .gitignore

Create a .gitignore file:

# Virtual environment
venv/
.venv/

# Python
__pycache__/
*.py[cod]

# Streamlit
.streamlit/secrets.toml

# Generated output
output/*
!output/.gitkeep

# Local input documents
input/*
!input/.gitkeep

# Environment files
.env
.env.*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

Important: Do not commit real confidential documents to GitHub.

📦 Recommended requirements.txt

Your requirements file should contain the packages actually used by the
project, for example:

streamlit
pandas
altair
python-docx

If your existing detector implementation requires additional packages,
keep those dependencies in the file as well.

Install with:

pip install -r requirements.txt

🔬 Testing Strategy

The project can be tested at multiple levels.

Detector testing

python test_detectors.py

CLI processing

python main.py

UI testing

streamlit run app.py

Then verify:

DOCX upload

Analyze button

Detection Explorer

Before / After

Validation

Audit Log

Redacted DOCX download

CSV download

📋 Project Checklist

Before submission, verify:

app.py runs

main.py runs

Detector tests pass

DOCX upload works

PII detection works

Synthetic replacement works

Redacted DOCX opens correctly

Validation page works

Detection Explorer shows results

Before / After shows replacements

Audit Log records processing

DOCX download works

CSV download works

requirements.txt is updated

.gitignore exists

No confidential input documents are committed

README is included

Repository contains only final project files

🧩 Project Philosophy

PII Shield follows a simple privacy engineering workflow:

Identify
   ↓
Understand
   ↓
Transform
   ↓
Verify
   ↓
Report

The goal is not merely to hide text.

The goal is to create a repeatable, inspectable, and verifiable
document sanitization workflow.

👨‍💻 Author

Mouli Banerjee

B.Tech Computer Science & Engineering
Data Science / Data Analytics Focus

📄 License

This project is intended for educational, portfolio, and demonstration
purposes unless a separate license is provided.

⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub and sharing feedback or
improvements.

Project Status

Current version: v1.0

Status: Active development

Primary interface: Streamlit

Primary document format: Microsoft Word DOCX

Core workflow:

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