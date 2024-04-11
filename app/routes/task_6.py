import os
from fastapi import APIRouter

from app.core import DataGenerator, JSONWriter, CSVWriter, YAMLWriter
from app.models import FileGenerationRequest

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}
В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""
@router.post("/generate_file", description="Задание_6. Конвертер")
async def generate_file(request_data: FileGenerationRequest) -> int:
    """Описание."""

    data_instance = DataGenerator()
    data_instance.generate(request_data.matrix_size)
    directory = os.path.dirname(__file__) + "/../files/"
    writer = None
    if request_data.file_type == "json":
        writer = JSONWriter()
    elif request_data.file_type == "csv":
        writer = CSVWriter()
    elif request_data.file_type == "yaml":
        writer = YAMLWriter()
    data_instance.to_file(path=directory, writer=writer)

    return data_instance.file_id
