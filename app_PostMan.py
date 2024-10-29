from flask import Flask, request, jsonify
from flask_cors import CORS
from pii_identifier import main
 
app = Flask(__name__)
CORS(app)
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/extract_entities', methods=['POST'])
def extract_entities():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
 
        input_file_path = data.get('input_file_path', None)
        input_text = data.get('input_text', None)
        entities_to_extract = data.get('entities_to_extract', [])
 
        if input_file_path is None and input_text is None:
            return jsonify({"error": "Either 'input_file_path' or 'input_text' must be provided."}), 400
 
        results = main(input_file_path=input_file_path, input_text=input_text, entities_to_extract=entities_to_extract)
        print(results)
        # entities = {
        #     'PERSON_NAME': results.get('PERSON_NAME', {}).get('recognized_values', []),
        #     'TITLES': results.get('TITLES', {}).get('recognized_values', []),
        #     'DATES': results.get('DATES', {}).get('recognized_values', []),
        #     'LOCATION': results.get('LOCATION', {}).get('recognized_values', []),
        #     'EMAIL': results.get('EMAIL', {}).get('recognized_values', []),
        #     'ORGANIZATION': results.get('ORGANIZATION', {}).get('recognized_values', []),
        #     'CITIZENSHIP': results.get('CITIZENSHIP',{}).get('recognized_values',[]),
        #     'PHONE_NUMBER': results.get('PHONE_NUMBER', {}).get('recognized_values', []),
        #     'CRIMINAL_HISTORY': results.get('CRIMINAL_HISTORY', {}).get('recognized_values', []),
        #     'RELIGIOUS_AFFLICATION': results.get('RELIGIOUS_AFFLICATION', {}).get('recognized_values', []),
        #     'MEDICAL_HISTORY': results.get('MEDICAL_HISTORY', {}).get('recognized_values', []),
        #     'SEXUAL_ORIENTATION': results.get('SEXUAL_ORIENTATION', {}).get('recognized_values', []),
        #     'TAX_ID': results.get('TAX_ID', {}).get('recognized_values', []),
        #     'DRIVER_LICENSE': results.get('DRIVER_LICENSE', {}).get('recognized_values', []),
        #     'BIOMETERIC_IDENTIFIER': results.get('Biometric_Identifier', {}).get('recognized_values', []),
        #     'PATIENT_ID': results.get('PATIENT_ID', {}).get('recognized_values', []),
        #     'GENDERS': results.get('GENDERS', {}).get('recognized_values', []),
        #     'AAA_NUMBERS': results.get('AAA_NUMBERS', {}).get('recognized_values', [])
        # }
 
        return jsonify(results)
   
    except Exception as e:
        print(f"An error occurred in the main function: {e}")
        return {"error": str(e)}
 
if __name__ == '__main__':
    app.run(debug=False)