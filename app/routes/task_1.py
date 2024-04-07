from fastapi import APIRouter


router = APIRouter(tags=["Стажировка"])


"""
Задание_1. Удаление дублей
    Реализуйте функцию соответствующую следующему описанию:
    На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
    фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
    подобные слова вне зависимости от регистра исключаются.
    На выходе должны получить уникальный список слов в нижнем регистре.

    Список слов для примера: ["Мама", "МАМА", "Мама", "папа", "ПАПА", "Мама", "ДЯдя", "брАт", "Дядя", "Дядя", "Дядя"]
    Ожидаемый результат: ["папа","брат"]
"""
@router.post("/find_in_different_registers", description="Задание_1. Удаление дублей")
async def find_in_different_registers(words: list[str]) -> list[str]:
    """
    Создаем 2 списка - один под результат, другой используется для слов к удалению
    Заходим в цикл, рассчитанный на количество элементов в исходном списке
    Функцией pop берем очередной элемент и проверяем:
        1.1 Встречается ли точно такой же элемент среди оставшихся элементов
        1.2 Находится ли элемент в списке к пропуску
        2. Находится ли элемент в результирующем списке
    Если элемент не был обнаружен в списке к пропуску и еще не находится в результирующем списке,
    добавляем его к выводу
    """
    result = []
    words_to_skip = []
    for _ in range(len(words)):
        elem = words.pop()
        if elem in words or elem.lower() in words_to_skip:
            words_to_skip.append(elem.lower())
            continue
        elif elem.lower() not in result:
            result.append(elem.lower())
    return result
