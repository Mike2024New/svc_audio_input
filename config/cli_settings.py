import sys
from config import paths_settings
from config import settings, settings_manager
from config.server_settings import server
from config.build_settings import build_settings

# ==========================================
#  НАСТРОЙКА CLI
# ==========================================
from infrastructure_cli_utils import CliSettings, get_cli_app

# управление включением системных CLI команд:
cli_settings = CliSettings(
    enable_run_server=True,
    enable_settings_show=True,
    enable_settings_edit=True,
    enable_folder_command=True,
    enable_git_push=True,
    enable_build_command=True,
    enable_run_test=False,
    enable_run_command=False,
)

# создание cli интерфейса с пробросом необходимых настроек
app = get_cli_app(
    name=settings.name,
    root_dir=paths_settings.ROOT_DIR,
    exe_mode=getattr(sys, 'frozen', False),
    build_settings=build_settings,
    cli_settings=cli_settings,  # настройки включаемых системных команд
    settings=settings,
    settings_manager=settings_manager,
    server=server,
)
