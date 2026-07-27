from config import settings
from config import message_bus_add
from infrastructure_server import server_factory_v2
from api import routers_list

"""
Настройка сервера. Проброс пользовательских эндпоинтов
"""


def server_start(details):
    message_bus_add(
        subcomponent=settings.name,
        level='start',
        event='server is Running',
        message=f'server is Running: {details}',
        data=details,
    )


def server_stop(details):
    message_bus_add(
        subcomponent=settings.name,
        level='stop',
        event='server stop',
        message=f'server stop: {details}',
        data=details,
    )


def server_start_error(details):
    message_bus_add(
        subcomponent=settings.name,
        level='error',
        event='server start error',
        message=f'server start error: {details}',
        data=details,
    )


server = server_factory_v2(
    app_name=settings.name,
    # включение системных API:
    api_shudtown=True,
    api_pid=True,
    # подключение роутеров приложения:
    routers_list=routers_list,
    # функции (перед запуском сервера, после запуска, в случае ошибки):
    callback_start=server_start,
    callback_end=server_stop,
    callback_start_error=server_start_error,
)
