from config import paths_settings
from config.component_settings import settings, settings_manager
from config.message_bus_settings import message_bus_add, message_bus_settings

__all__ = [
    'paths_settings',  # пути приложения
    'settings', 'settings_manager',  # настройки приложения основанные на схеме из schemas.py
    'message_bus_add', 'message_bus_settings',  # шина сообщений (логирование, общение компонентов)
]
