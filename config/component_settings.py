from config import paths_settings
from infrastructure_settings_manager import get_settings_manager
from config.schemas import SchemaSettings

"""
Настройки прилолжения (читается схема из schemas.py, за тем сохраняются в settings.json, который можно редактировать в ручную) 
"""

settings_manager = get_settings_manager(
    json_file_path=paths_settings.JSON_SETTINGS_FILE_PATH,
    settings_model=SchemaSettings(),
)
settings = settings_manager.settings
