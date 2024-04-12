import functools
import logging
from fastapi import APIRouter, Response

router = APIRouter(tags=["Стажировка"])

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""
def count_requests(func):
    func.request_count = 0
    @functools.wraps(func)
    async def wrapper(*args):
        func.request_count += 1
        logging.info(func.request_count)
        return await func(*args)
    return wrapper



@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests
async def new_request():
    """Возвращает кол-во сделанных запросов."""

    return Response()
