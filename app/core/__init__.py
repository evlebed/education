import glob
import json
import csv
import os
from random import randint
import yaml

from abc import ABC, abstractmethod
from io import StringIO
import pandas as pd


def convert_arabic_to_roman(number: int) -> str:
    if number <= 0 or number > 3999:
        return "не поддерживается"

    roman_numerals = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
        50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
    }

    result = []
    for value, numeral in sorted(roman_numerals.items(), reverse=True):
        while number >= value:
            result.append(numeral)
            number -= value

    return ''.join(result)


def convert_roman_to_arabic(number: str) -> int:
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    arabic = 0
    prev_value = 0
    for char in reversed(number.upper()):
        if char not in roman_numerals:
            return "не поддерживается"
        value = roman_numerals[char]
        if value < prev_value:
            arabic -= value
        else:
            arabic += value
        prev_value = value

    return arabic


def average_age_by_position(file: str):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return {"error": f"Ошибка при чтении CSV файла: {e}"}

    columns_names = ["Имя", "Возраст", "Должность"]
    for col in columns_names: 
        if col not in df.columns or len(df.columns) != len(columns_names):
            return {"error": f"Файл должен содержать следующие колонки: {columns_names}"}

    try:
        df['Возраст'] = pd.to_numeric(df['Возраст'])
        avg_age_by_position = df.groupby('Должность')['Возраст'].mean().to_dict()
        return avg_age_by_position
    except Exception as e:
        return {"error": f"Ошибка при вычислении среднего возраста: {e}"}


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""
class BaseWriter(ABC):
    """Абстрактный класс с методом write для генерации файла"""

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        ...


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        json.dump(data, output)
        output.seek(0)
        return output


class CSVWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в csv формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(data)
        output.seek(0)
        return output


class YAMLWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        yaml.dump(data, output)
        output.seek(0)
        return output


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id = None

    def generate(self, matrix_size: int) -> None:
        """Генерирует матрицу данных заданного размера."""
        data: list[list[int, str, float]] = []
        for i in range(matrix_size):
            row = [
                i + 1,
                f"row_{i + 1}",
                float(i + 0.1)
            ]
            data.append(row)
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        """
        Метод для записи в файл данных после генерации.
        Если данных нет, вызывается исключение.
        :param path: путь куда сохранить файл
        :param writer: экземпляр класса-писателя (например, JSONWriter, CSVWriter, YAMLWriter)
        """
        if self.data is None:
            raise ValueError("Данные не были сгенерированы.")

        output_data = writer.write(self.data)
        file_type = None
        self.file_id = generate_unique_id(directory=path)
        if isinstance(writer, JSONWriter):
            file_type = ".json"
        elif isinstance(writer, CSVWriter):
            file_type = ".csv"
        elif isinstance(writer, YAMLWriter):
            file_type = ".yaml"  

        full_path = f"{path}{self.file_id}_{file_type}"

        with open(full_path, 'w') as f:
            f.write(output_data.getvalue())


def generate_unique_id(directory: str) -> int:
    file_id = None
    while True:
        file_id: int = randint(1,1000000)
        pattern = os.path.join(directory, f"{file_id}_*")
        matching_files = glob.glob(pattern)
        if len(matching_files) == 0:
            return file_id
