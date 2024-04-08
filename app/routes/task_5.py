import glob
import os
from random import randint
import shutil
from typing import Any, Union
import zipfile
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse


router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.	Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. 
В ответ на удачную загрузку файла должен приходить id для скачивания. 
b.	Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""
@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile = File(...)) -> int:
    """Описание."""
    directory = os.path.dirname(__file__) + "/../files/"
    file_id = None
    while True:
        file_id: int = randint(1,1000000)
        pattern = os.path.join(directory, f"{file_id}_" + "*")
        matching_files = glob.glob(pattern)
        if len(matching_files) == 0:
            break

    full_path = f"{directory}{file_id}_{file.filename}"
    
    with open(file.filename, "wb") as f:
        shutil.copyfileobj(file.file, f)

    zip_filename = f"{full_path}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.write(file.filename, compress_type=8, compresslevel=2)

    os.remove(file.filename)

    return file_id


@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: int) -> Any:
    """Описание."""

    directory = os.path.dirname(__file__) + "/../files/"

    pattern = os.path.join(directory, f"{file_id}_" + "*")
    matching_files = glob.glob(pattern)
    if len(matching_files) != 0:
        return FileResponse(matching_files[0], filename=os.path.basename(matching_files[0]) ,media_type='application/octet-stream')

    return JSONResponse(content={"error": "File not found"}, status_code=404)
