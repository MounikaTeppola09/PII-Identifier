from presidio_analyzer import PatternRecognizer, AnalyzerEngine, Pattern
from presidio_anonymizer import AnonymizerEngine
from docx import Document
import datefinder
import spacy
import fitz
import re
import logging
from builtins import PendingDeprecationWarning

from Deny_List import (
    citizenship_immigration_terms, female_names, criminal_history_deny_list,
    genders, religious_affiliations, identity_terms, medical_history_deny_list, title_denylist
)
 
# Setting up logging configuration
logging.basicConfig(filename='app.log', level=logging.DEBUG)
 
#Extracting from pdf
def extract_text_from_pdf(pdf_path):
    """
    Extracts text content from a PDF file.
 
    Parameters:
    - pdf_path (str): Path to the PDF file.
 
    Returns:
    - str: Extracted text from the PDF.
    """
    text = ""
    try:
        logging.info("extracting text from pdf file")
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
            logging.info("text extracted from pdf successfully")
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise  # Raising an exception for better traceability
 
    logging.info(text)
    return text
pass
 
#Extracting from text file
def extract_text_from_text_file(text_file_path):
    """
    Extracts text content from a text file.
 
    Parameters:
    - text_file_path (str): Path to the text file.
 
    Returns:
    - str: Extracted text from the text file.
    """
    try:
 
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
 
        return text
    except Exception as e:
        logging.error(f"Error extracting text from text file: {e}")
 
    return ""
pass
 
#Extracting from document  
def extract_text_from_document(docx_file_path):
    """
    Extracts text content from a Word document.
 
    Parameters:
    - docx_file_path (str): Path to the Word document.
 
    Returns:
    - str: Extracted text from the Word document.
    """
    try:
        document = Document(docx_file_path)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logging.error(f"Error extracting text from document file: {e}")
 
    return ""
    pass
 
 
#Entity Recognizers
def citizenship_recognizer(text):
    """
    Recognizes citizenship in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized citizenship.
    """
 
    try:
        logging.info("checking for citizenship")
       
        citizenship_recognizer = PatternRecognizer(
            supported_entity="CITIZENSHIP",
            deny_list=citizenship_immigration_terms
        )
 
        citizen_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(citizenship_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["CITIZENSHIP"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            citizen_output_dict["entity_type"].append(entity_name)
            citizen_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(citizen_output_dict["entity_type"], citizen_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return citizen_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # Handle the exception or re-raise it as needed
        # For example, you might log the error, return a specific error value, or raise a custom exception.
        return {"error": str(e)}
 
def person_recognizer(text):
    logging.info(text)
    try:
        logging.info("Checking for person name")
        person_recognizer = PatternRecognizer(
            supported_entity="PERSON",
            deny_list=female_names
        )
 
        person_output_dict = {
            "entity_type": "PERSON",
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(person_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["PERSON"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            person_output_dict["recognized_values"].append(redacted_value)
 
        for value in person_output_dict["recognized_values"]:
            logging.info(f"Recognized Value: {value}")
 
        return person_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred in person_recognizer: {e}")
        return {"error": str(e)}
 
def criminal_history_recognizer(text):
    """
    Recognizes Criminal History in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Criminal History.
    """
    criminal_history_recognizer = PatternRecognizer(
        supported_entity="CRIMINAL HISTORY",
        deny_list=criminal_history_deny_list
    )
 
    criminal_history_output_dict = {
        "entity_type": [],
        "recognized_values": []
    }
 
    analyzer = AnalyzerEngine()
    analyzer.registry.add_recognizer(criminal_history_recognizer)
 
    results = analyzer.analyze(text, language='en', entities=["CRIMINAL HISTORY"])
 
    for result in results:
        entity_name = result.entity_type
        redacted_value = text[result.start:result.end]
        criminal_history_output_dict["entity_type"].append(entity_name)
        criminal_history_output_dict["recognized_values"].append(redacted_value)
 
    for entity, value in zip(criminal_history_output_dict["entity_type"], criminal_history_output_dict["recognized_values"]):
        logging.info(f"Entity Type: {entity}")
        logging.info(f"Recognized Value: {value}\n")
 
    return criminal_history_output_dict
    pass
 
def email_recognizer(text):
    """
    Recognizes Email in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Email.
    """
    try:
        logging.info("Checking for email")
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
       
        email_output_dict = {
            "entity_type": "EMAIL",
            "recognized_values": []
        }
 
        matches = email_pattern.finditer(text)
       
        for match in matches:
            redacted_value = match.group(0)
            email_output_dict["recognized_values"].append(redacted_value)
 
        for value in email_output_dict["recognized_values"]:
            logging.info(f"Recognized Value: {value}")
 
        return email_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred in email_recognizer: {e}")
        return {"error": str(e)}
 
def religious_affiliations_recognizer(text):
    """
    Recognizes Religious Affiliations in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Religious Affiliations.
    """
    try:
        logging.info("Checking for religious affiliations")
        religious_affiliations_recognizer = PatternRecognizer(
            supported_entity="RELIGIOUS AFFILIATION",
            deny_list=religious_affiliations
        )
 
        religious_affiliations_output_dict = {
            "entity_type": "RELIGIOUS AFFILIATION",
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(religious_affiliations_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["RELIGIOUS AFFILIATION"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            religious_affiliations_output_dict["recognized_values"].append(redacted_value)
 
        for value in religious_affiliations_output_dict["recognized_values"]:
            logging.info(f"Recognized Value: {value}")
 
        return religious_affiliations_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred in religious_affiliations_recognizer: {e}")
        return {"error": str(e)}
 
def sexual_orientation_recognizer(text):
    """
    Recognizes Sexual Orientation in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Sexual Orientation.
    """
    try:
        sexual_orientation_recognizer = PatternRecognizer(
            supported_entity="SEXUAL ORIENTATION",
            deny_list=identity_terms
        )
 
        sexual_orientation_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(sexual_orientation_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["SEXUAL ORIENTATION"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            sexual_orientation_output_dict["entity_type"].append(entity_name)
            sexual_orientation_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(sexual_orientation_output_dict["entity_type"], sexual_orientation_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return sexual_orientation_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
   
def driver_license_recognizer(text):
    """
    Recognizes Driver License in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Driver License.
    """
    try:
        # Define the driver's license pattern
        driver_license_pattern = Pattern(name="driver_license_pattern", regex=r"\b[A-Z0-9]{3}-[A-Z0-9]{6}-[A-Z0-9]{3}\b", score=0.85)
 
        # Create a recognizer for driver's license using the defined pattern
        driver_license_recognizer = PatternRecognizer(supported_entity="DRIVER_LICENSE_NUMBER", patterns=[driver_license_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(driver_license_recognizer)
 
        # Analyze the text for driver's license entities
        results = analyzer.analyze(text, language='en', entities=["DRIVER_LICENSE_NUMBER"])
 
        driver_license_output_dict = {
            "entity_type": "DRIVER_LICENSE_NUMBER",
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            driver_license_output_dict["recognized_values"].append(redacted_value)
 
        for value in driver_license_output_dict["recognized_values"]:
            logging.info(f"Recognized Value: {value}")
 
        return driver_license_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred in driver_license_recognizer: {e}")
        return {"error": str(e)}
 
def financial_account_recognizer(text):
    """
    Recognizes Financial Account Number in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Financial Account Number.
    """
    try:
        # Define the financial account pattern
        financial_account_pattern = Pattern(name="financial_account_pattern", regex=r"\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b", score=0.9)
 
        # Create a recognizer for financial account using the defined pattern
        financial_account_recognizer = PatternRecognizer(supported_entity="FINANCIAL_ACCOUNT_NUMBER", patterns=[financial_account_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(financial_account_recognizer)
 
        # Analyze the text for financial account entities
        results = analyzer.analyze(text, language='en', entities=["FINANCIAL_ACCOUNT_NUMBER"])
 
        financial_account_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            financial_account_output_dict["entity_type"].append(entity_name)
            financial_account_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(financial_account_output_dict["entity_type"], financial_account_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return financial_account_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def phone_number_recognizer(text):
    """
    Recognizes Phone Number in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Phone Number.
    """
    try:
        # Define the phone number pattern
        phone_number_pattern = Pattern(name="phone_number_pattern", regex=r"(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", score=0.8)
 
        # Create a recognizer for phone number using the defined pattern
        phone_number_recognizer = PatternRecognizer(supported_entity="PHONE_NUMBER", patterns=[phone_number_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(phone_number_recognizer)
 
        # Analyze the text for phone number entities
        results = analyzer.analyze(text, language='en', entities=["PHONE_NUMBER"])
 
        phone_number_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            phone_number_output_dict["entity_type"].append(entity_name)
            phone_number_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(phone_number_output_dict["entity_type"], phone_number_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return phone_number_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def biometric_identifier_recognizer(text):
    """
    Recognizes Biometric Identifier in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Biometric Identifier.
    """
    try:
        # Define the biometric identifier pattern
        biometric_identifier_pattern = Pattern(name="biometric_identifier_pattern", regex=r"\b[A-Z0-9]{10}\b", score=0.85)
 
        # Create a recognizer for biometric identifier using the defined pattern
        biometric_identifier_recognizer = PatternRecognizer(supported_entity="BIOMETRIC_IDENTIFIER", patterns=[biometric_identifier_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(biometric_identifier_recognizer)
 
        # Analyze the text for biometric identifier entities
        results = analyzer.analyze(text, language='en', entities=["BIOMETRIC_IDENTIFIER"])
 
        biometric_identifier_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            biometric_identifier_output_dict["entity_type"].append(entity_name)
            biometric_identifier_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(biometric_identifier_output_dict["entity_type"], biometric_identifier_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return biometric_identifier_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def patient_id_recognizer(text):
    """
    Recognizes Patient ID Number in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Patient ID Number.
    """
    try:
        # Define the patient ID pattern
        patient_id_pattern = Pattern(name="patient_id_pattern", regex=r"\b[A-Z]{3}-\d{5}-[A-Z0-9]{2}\b", score=0.85)
 
        # Create a recognizer for patient ID using the defined pattern
        patient_id_recognizer = PatternRecognizer(supported_entity="PATIENT_ID_NUMBER", patterns=[patient_id_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(patient_id_recognizer)
 
        # Analyze the text for patient ID entities
        results = analyzer.analyze(text, language='en', entities=["PATIENT_ID_NUMBER"])
 
        patient_id_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            patient_id_output_dict["entity_type"].append(entity_name)
            patient_id_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(patient_id_output_dict["entity_type"], patient_id_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return patient_id_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def dob_recognizer(text):
    """
    Recognizes Date of Birth in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Date of Birth.
    """
    try:
        # Define the date of birth pattern with multiple formats
        dob_pattern = Pattern(
            name="dob_pattern",
            regex=r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4}|\d{2}-\d{2}-\d{2}|\d{2}-\d{2}-\d{2}|\d{2}-\d{2}-\d{2})\b",
            score=0.85
        )
 
        # Create a recognizer for date of birth using the defined pattern
        dob_recognizer = PatternRecognizer(supported_entity="DATE_OF_BIRTH", patterns=[dob_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(dob_recognizer)
 
        # Analyze the text for date of birth entities
        results = analyzer.analyze(text, language='en', entities=["DATE_OF_BIRTH"])
 
        dob_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            dob_output_dict["entity_type"].append(entity_name)
            dob_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(dob_output_dict["entity_type"], dob_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return dob_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def medical_history_recognizer(text):
    """
    Recognizes Medical History in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Medical History.
    """
    try:
        medical_history_recognizer = PatternRecognizer(
            supported_entity="MEDICAL HISTORY",
            deny_list=medical_history_deny_list
        )
 
        medical_history_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(medical_history_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["MEDICAL HISTORY"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            medical_history_output_dict["entity_type"].append(entity_name)
            medical_history_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(medical_history_output_dict["entity_type"], medical_history_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return medical_history_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def genders_recognizer(text):
    """
    Recognizes Genders in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Genders.
    """
    try:
        genders_recognizer = PatternRecognizer(
            supported_entity="GENDER",
            deny_list=genders
        )
 
        genders_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(genders_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["GENDER"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            genders_output_dict["entity_type"].append(entity_name)
            genders_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(genders_output_dict["entity_type"], genders_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return genders_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def title_recognizer(text):
    """
    Recognizes Title in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Title.
    """
    try:
        title_recognizer = PatternRecognizer(
            supported_entity="TITLE",
            deny_list=title_denylist
        )
 
        title_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(title_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["TITLE"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
          #  title_output_dict["entity_type"].append(entity_name)
            title_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(title_output_dict["entity_type"], title_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
        title_output_dict["entity_type"] = entity_name
        return title_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def tax_id_recognizer(text):
    """
    Recognizes Tax ID Number in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Tax ID Number.
    """
    try:
        # Define the tax ID pattern
        tax_id_pattern = Pattern(name="tax_id_pattern", regex=r"\b\d{3}-\d{2}-\d{4}\b", score=0.9)
 
        # Create a recognizer for tax ID using the defined pattern
        tax_id_recognizer = PatternRecognizer(supported_entity="TAX_ID", patterns=[tax_id_pattern])
 
        # Initialize the analyzer engine and add the recognizer to the registry
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(tax_id_recognizer)
 
        # Analyze the text for tax ID entities
        results = analyzer.analyze(text, language='en', entities=["TAX_ID"])
 
        tax_id_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
 
        # Retrieve and print recognized entities and their values
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            tax_id_output_dict["entity_type"].append(entity_name)
            tax_id_output_dict["recognized_values"].append(redacted_value)
 
        for entity, value in zip(tax_id_output_dict["entity_type"], tax_id_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
 
        return tax_id_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def location_recognizer(text):
    """
    Recognizes Location in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Location.
    """
    try:
        logging.info("Checking for locations in the text")
 
        location_output_dict = {
            "entity_type": "LOCATION",
            "recognized_values": []
        }
 
        location_pattern = Pattern(
            name="location_pattern",
            regex=r"\b(?:\d+\s[A-Za-z]+\s(?:Street|Avenue|Road)|[A-Za-z]+\s(?:Street|Avenue|Road)|[A-Za-z]+\s(?:Area|Town|Village|City|State)|[A-Za-z]+\s(?:Country))\b",
            score=0.85
        )
 
        location_recognizer = PatternRecognizer(supported_entity="LOCATION", patterns=[location_pattern])
 
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(location_recognizer)
 
        results = analyzer.analyze(text, language='en', entities=["LOCATION"])
 
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            location_output_dict["recognized_values"].append(redacted_value)
 
        for value in location_output_dict["recognized_values"]:
            logging.info(f"Recognized Value: {value}")
 
        return location_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def date_recognizer(text):
    """
    Recognizes Date in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Date.
    """
    try:
        logging.info("checking for dates in the text")
 
        date_output_dict = {
            "entity_type": "DATE",
            "recognized_values": []
        }
 
        # Use datefinder to extract dates from the text
        matches = datefinder.find_dates(text)
 
        # Iterate through the matches and format recognized dates
        for match in matches:
            recognized_value = match.strftime("%b %d, %Y")
            date_output_dict["recognized_values"].append(recognized_value)
 
        for value in date_output_dict["recognized_values"]:
            logging.info(f"Recognized Value: {value}\n")
 
        return date_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def AAA_no_recognizer(text):
    """
    Recognizes AAA Number in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized AAA number.
    """
    try:
        logging.info("checking for AAA number")
        AAA_no_pattern = Pattern(name="AAA_no_pattern", regex=r"\d{2}-\d{2}-\d{4}-\d{4}", score=0.9)
        AAA_no_recognizer = PatternRecognizer(supported_entity="AAA Number", patterns=[AAA_no_pattern])
   
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(AAA_no_recognizer)
   
        results = analyzer.analyze(text, language='en', entities=["AAA Number"])
   
        AAA_no_output_dict = {
            "entity_type": [],
            "recognized_values": []
        }
   
        for result in results:
            entity_name = result.entity_type
            redacted_value = text[result.start:result.end]
            AAA_no_output_dict["entity_type"].append(entity_name)
            AAA_no_output_dict["recognized_values"].append(redacted_value)
   
        for entity, value in zip(AAA_no_output_dict["entity_type"], AAA_no_output_dict["recognized_values"]):
            logging.info(f"Entity Type: {entity}")
            logging.info(f"Recognized Value: {value}\n")
   
        return AAA_no_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def organizations_recognizer(text):
    """
    Recognizes Organizations in the text.
 
    Parameters:
    - text (str): Input text.
 
    Returns:
    - dict: Dictionary containing recognized Organizations.
    """
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
 
        org_output_dict = {
            "entity_type": "ORG",
            "recognized_values": []
        }
 
        for entity in doc.ents:
            if entity.label_ == "ORG":
                org_output_dict["recognized_values"].append(entity.text)
 
        return org_output_dict
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
 
def main(input_file_path=None, input_text=None, entities_to_extract=[]):
    try:
           
        if input_file_path:
            file_extension = input_file_path.split('.')[-1].lower()
 
            if file_extension == 'pdf':
                text = extract_text_from_pdf(input_file_path)
            elif file_extension == 'docx':
                text = extract_text_from_document(input_file_path)
            elif file_extension == 'txt':
                text = extract_text_from_text_file(input_file_path)
            else:
                logging.info("Unsupported file format. Please provide a PDF, DOCX, or TXT file.")
                return
        elif input_text:
            text = input_text
        else:
            logging.info("Please provide either an input file path or input text.")
            return
 
        mapping_entities_functions = {
            "PERSON_NAME": person_recognizer,
            "TITLES": title_recognizer,
            "DATES": date_recognizer,
            "CITIZENSHIP": citizenship_recognizer,
            "EMAIL": email_recognizer,
            "ORGANIZATION": organizations_recognizer,
            "LOCATION": location_recognizer,
            "CITIZENSHIP" : citizenship_recognizer,
            "PHONE_NUMBER" : phone_number_recognizer,
            "CRIMINAL_HISTORY" : criminal_history_recognizer,
            "RELIGIOUS_AFFLICATION" : religious_affiliations_recognizer,
            "MEDICAL_HISTORY" : medical_history_recognizer,
            "SEXUAL_ORIENTATION" : sexual_orientation_recognizer,
            "TAX_ID" : tax_id_recognizer,
            "DRIVER_LICENSE": driver_license_recognizer,
            "BIOMETERIC_IDENTIFIER" : biometric_identifier_recognizer,
            "PATIENT_ID" : patient_id_recognizer,
            "GENDERS" : genders_recognizer,
            "AAA_NUMBERS" : AAA_no_recognizer
            }
 
        results = {}
                                                       
        for entity in entities_to_extract:
            if entity in mapping_entities_functions:
                function = mapping_entities_functions[entity]
                result = function(text)
                results[entity] = result
           
       
        logging.info(results)
        return results
 
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
        return {"error": str(e)}
 