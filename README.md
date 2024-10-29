# PII-Identifier

# Overview
The PII Identifier is a Python-based application designed to identify and extract Personally Identifiable Information (PII) terms from input text or files. This application is built using FastAPI and Flask, allowing for easy integration with web frameworks for API calls. It utilizes a main dataset (Deny_List.py) containing a comprehensive list of PII terms.

# Features
Extract PII Entities: The application can extract various PII entities such as names, email addresses, phone numbers, and more from input text or uploaded files.
Web API: Provides endpoints for interaction using both FastAPI and Flask.
Cross-Origin Resource Sharing (CORS): Enabled to allow requests from different origins.

# Project Structure

PII-Identifier/
│
├── app_FastAPI.py          # Contains FastAPI application
├── app_PostMan.py          # Flask application
├── Deny_List.py            # Dataset containing PII terms
├── pii_identifier.py       # Main logic for PII extraction
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

# Getting Started

# Installation
Clone the repository:

git clone https://github.com/yourusername/PII-Identifier.git
cd PII-Identifier

# Install the required dependencies:

pip install -r requirements.txt

