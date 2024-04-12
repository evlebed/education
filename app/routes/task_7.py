from time import time
import logging
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

output_log = logging.getLogger("output")
client_host: ContextVar[str | None] = ContextVar("client_host", default=None)

"""
Задание_7. Логирование в FastAPI с использованием middleware.

Написать конфигурационный файл для логгера "output"
Формат выводимых логов:
[CURRENT_DATETIME] {file: line} LOG_LEVEL - | EXECUTION_TIME_SEC | HTTP_METHOD | URL | STATUS_CODE |
[2023-12-15 00:00:00] {example:62} INFO | 12 | GET | http://localhost/example | 200 |


Дописать класс CustomMiddleware.
Добавить middleware в приложение (app).
"""
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Load request ID from headers if present. Generate one otherwise."""
        start_time = time()
        try:
            client_host.set(request.client.host)
            output_log.info(f"Accepted request {request.method} {request.url}")

            response = await call_next(request)

            formatted_message = f'| {round(time() - start_time, 3)} | {request.method} | {request.url} | {response.status_code} |'
            output_log.info(formatted_message)
            return response
        except:
            formatted_message = f'| {round(time() - start_time, 3)} | {request.method} | {request.url} | 500 |'
            output_log.error(formatted_message)
            response = Response("Internal Server Error", status_code=500)

            return response
