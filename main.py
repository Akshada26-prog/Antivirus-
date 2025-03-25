import os
import hashlib
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Request

# FastAPI setup
app = FastAPI()

# Jinja2 template setup for frontend
templates = Jinja2Templates(directory="templates")

# Example list of known virus signatures (these are just sample hashes)
known_virus_signatures = {
    "e99a18c428cb38d5f260853678922e03": "Example Virus 1",
    "d41d8cd98f00b204e9800998ecf8427e": "Example Virus 2",
    # Add more known virus hashes here
}

# Function to calculate MD5 hash of a file
def calculate_file_hash(file_content: bytes) -> str:
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    hash_md5.update(file_content)
    return hash_md5.hexdigest()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Serve the homepage."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scan_file/")
async def scan_file(file: UploadFile = File(...)):
    """Scan a single file for viruses."""
    try:
        content = await file.read()
        file_hash = calculate_file_hash(content)
        
        if file_hash in known_virus_signatures:
            return {"status": "Virus detected", "file_name": file.filename, "virus": known_virus_signatures[file_hash]}
        else:
            return {"status": "File is clean", "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/scan_directory/")
async def scan_directory(directory: UploadFile = File(...)):
    """Scan a directory for virus-infected files."""
    try:
        # Temporary folder to save uploaded files
        upload_folder = Path("uploaded_files")
        upload_folder.mkdir(exist_ok=True)

        # Save the uploaded zip file containing the directory
        zip_file_path = upload_folder / directory.filename
        with open(zip_file_path, "wb") as f:
            f.write(await directory.read())
        
        # Here you would typically unzip and scan the files
        # For simplicity, we're just returning a success message.
        
        return {"status": "Directory scanned", "message": "Scanning directory functionality is under construction."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing directory: {str(e)}")

