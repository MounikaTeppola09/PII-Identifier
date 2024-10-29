# PII-Identifier

# Overview
The PII Identifier is a Python-based application designed to identify and extract Personally Identifiable Information (PII) terms from input text or files. This application is built using FastAPI and Flask, allowing for easy integration with web frameworks for API calls. It utilizes a main dataset (Deny_List.py) containing a comprehensive list of PII terms.

# Features
Extract PII Entities: The application can extract various PII entities such as names, email addresses, phone numbers, and more from input text or uploaded files.
Web API: Provides endpoints for interaction using both FastAPI and Flask.
Cross-Origin Resource Sharing (CORS): Enabled to allow requests from different origins.

# Getting Started

# Installation
Clone the repository:

git clone https://github.com/MounikaTeppola09/PII-Identifier.git
cd PII-Identifier

# Install the required dependencies:

pip install -r requirements.txt

# Running the Application
You can run the application using either FastAPI, Flask or VSCode.

**Running FastAPI**

    Start the FastAPI application:
    
    uvicorn app_FastAPI:app --reload
    
**Access the API documentation:**

    Open your web browser and go to http://localhost:8000/docs to access the interactive API documentation.

**Running Flask**

    Start the Flask application:
    
    python app_PostMan.py
    
**Access the API:**

    The Flask app will run on http://127.0.0.1:5000. You can test the /extract_entities endpoint using Postman or any HTTP client.

**Running the Main Code in VSCode**

If you want to run the main logic for PII extraction directly:

Open the pii_identifier.py file in Visual Studio Code (VSCode).

Make sure the required libraries are installed as specified in requirements.txt.

    Run the script:
    
    You can use the built-in terminal in VSCode to execute the following command:
    
    python pii_identifier.py

# API Endpoints
1. /extract_entities
**Method:** POST

**Description:** Extract PII entities from the provided input.

**Parameters:**

input_file_path (optional): Path to an input file containing text.

input_text (optional): Text from which to extract PII entities.

entities_to_extract (optional): List of entities to extract.

input_file (optional): Upload a file directly.

**Response:**

JSON object containing the extracted PII entities.

**Requirements**

The requirements.txt file includes the following dependencies:

- `fastapi`
- `uvicorn`
- `flask`
- `flask-cors`

You can install them all using the command provided in the Installation section.
