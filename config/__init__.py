import platform, sys, uuid
from pathlib import Path
from config.schemas import settings
from infrastructure_settings_manager import get_settings_manager
from infrastructure_message_bus import message_bus_factory, MessagePrintSettings, FileLogSettings

__all__ = [
    'ROOT_DIR',
    'settings',  # системные настройки приложения
    'settings_manager',  # менеджер настроек
    'message_bus_add',
]
IS_WINDOWS = 'windows' in platform.system().lower()

# для сборщика (pyinstaller)
EXE_MODE = getattr(sys, 'frozen', False)

# определение корневой точки приложения
ROOT_DIR = Path(sys.executable).parent if EXE_MODE else Path(__file__).parent.parent

# папка с логами
LOGS_FILE_PATH = ROOT_DIR / 'logs' / 'log.jsonl'
LOGS_FILE_PATH.parent.mkdir(exist_ok=True, parents=True)

# загрузка настроек приложения
settings_manager = get_settings_manager(
    json_file_path=Path(ROOT_DIR / 'settings.json'),
    settings_model=settings,
)
settings = settings_manager.settings

# название приложения берется из конфигурации
APP_NAME = settings.name

# шина сообщений
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
    file_log_json_path=LOGS_FILE_PATH,
    file_log_settings=FileLogSettings(
        max_files=10,
        max_size_mb=10,
        rotation_disable=False,
    )
)
