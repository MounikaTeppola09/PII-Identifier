from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pii_identifier import main
from typing import List
from fastapi.staticfiles import StaticFiles


app = FastAPI()

static_path = "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend's actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.post('/extract_entities')
async def extract_entities(
    input_file_path: str = Form(None),
    input_text: str = Form(None),
    entities_to_extract: str = Form([]),
    input_file: UploadFile = File(None)
    
):
    print(entities_to_extract)
    try:
        if not input_file_path and not input_text and not input_file:
            raise HTTPException(stats_code=400, detail="Either 'input_file_path' or 'input_text' must be provided.")
        
        if input_file:
            # Save the uploaded file to a temporary location
            with open(input_file_path, 'wb') as temp_file:
                temp_file.write(input_file.file.read())
            input_file_path = input_file.filename

        results = main(
            input_file_path=input_file_path,
            input_text=input_text,
            entities_to_extract=eval(entities_to_extract)
        )
        
        return JSONResponse(content=results)
   
    except Exception as e:
        print(f"An error occurred in the main function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#uvicorn app_FastAPI:app --reload
