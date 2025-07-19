import hashlib
import os
from datetime import datetime
from fastapi import HTTPException, UploadFile



def validate_hash(file, algrothim="sha256"):
    hasher = hashlib.new(algrothim)
    while chunk := file.read(8192):
        hasher.update(chunk)
    return hasher.hexdigest()
        

def save_file(file: UploadFile, user_id: int) -> tuple[str, str]:
    unique_filename = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    file_path = os.path.join("uploads", unique_filename)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return unique_filename, file_path


def validate_file(file: UploadFile):
    max_size = 1028 * 1028 #5 bytes
    allowed_extensions = {}# put whatever you want
    if file.size > max_size:
        HTTPException(status_code=404, detail="file too big")
        return
    