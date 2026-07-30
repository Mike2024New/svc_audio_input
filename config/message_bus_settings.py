import uuid
from config import paths_settings
from config import settings
from infrastructure_message_bus import message_bus_factory, MessagePrintSettings, FileLogSettings

"""
Настройка шины сообщений компонента.
Логирование в файл. Печать в терминал.
"""

__all__ = ['message_bus_add', 'message_bus_settings']

message_bus_add, message_bus_settings = message_bus_factory(
    component_id=str(uuid.uuid4())[:8],
    component_name=settings.name,
    print_message=True,
    # подключение сообщений
    message_print_settings=MessagePrintSettings(
        print_date=True,
        raw_message=False,
        ignore_levels=[],
        ignore_levels_invers=False,
    ),
    # подключение логирования в файл
    file_log_json_path=paths_settings.LOGS_FILE_PATH,
    file_log_settings=FileLogSettings(
        max_files=10,
        max_size_mb=10,
        rotation_disable=False,
    )
)

if __name__ == '__main__':
    message_bus_add(subcomponent='a', message='start', level='warning')
    message_bus_settings.set_trace_id(trace_id='#000')
