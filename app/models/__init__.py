from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import BaseModel, validator


class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class User(BaseModel):
    name: str
    age: int
    adult: bool = None
    message: Optional[str]

    @validator('age')
    def validate_age(cls, value):
        if not 0 <= value <= 100:
            raise ValueError("Возраст не может быть меньше 0 и больше 100")
        return value

    @property
    def adult(self) -> bool:
        return self.age >= 18


class MetaMapping(BaseModel):
    list_of_ids: List[Union[int, str]]
    tags: set  


class Meta(BaseModel):
    last_modification: str
    list_of_skills: Optional[List[str]]
    mapping: MetaMapping

    @validator('last_modification')
    def validate_last_modification(cls, value):
        expected_format = "%d/%m/%Y"
        try:
            datetime.strptime(str(value), expected_format)
        except ValueError:
            raise ValueError(f"Неправильный формат даты. Ожидаемый: {expected_format}")
        return value


class BigJson(BaseModel):
    """Использует модель User."""
    user: User
    meta: Meta


class FileGenerationRequest(BaseModel):
    file_type: str
    matrix_size: int 
    
    @validator('file_type')
    def validate_file_type(cls, v):
        if v not in ['json', 'csv', 'yaml']:
            raise ValueError('Неправильный тип файла, разрешенные: "json", "csv", "yaml"')
        return v
   
    @validator('matrix_size')
    def validate_matrix_size(cls, v):
        if v > 15 or v < 4:
            raise ValueError('Размер матрицы должен быть от 4 до 15')
        return v

# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
# class User(BaseModel):
#     name: str
#     age: str
#     is_adult: bool
#     message: str = None
#
#
# class UserResponse(BaseModel):
#     pass
