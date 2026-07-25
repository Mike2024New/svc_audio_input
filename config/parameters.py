import config
from infrastructure_builder import BuildParameters
from infrastructure_cli_utils import CliSettings, get_cli_app
from infrastructure_server import server_factory
from core import routers_list, component

# Порядок настроек важен

# ==========================================
#  НАСТРОЙКА СБОРКИ ПРИЛОЖЕНИЯ (pyinstaller)
# ==========================================

build_settings = BuildParameters(
    name=config.APP_NAME,
    entry_point_path=config.ROOT_DIR / 'cli.py',
    one_file=True,
    create_resources_symlink=False,
    open_folder=True,
)

# ==========================================
#  НАСТРОЙКА СЕРВЕРА
# ==========================================

# настройка сервера
server = server_factory(
    component=component,
    routers_list=routers_list,
    message_bus=config.message_bus_add,
    app_name=config.APP_NAME,
)

# ==========================================
#  НАСТРОЙКА CLI
# ==========================================

# настройка отображаемых базовых команд
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
    name=config.APP_NAME,
    root_dir=config.ROOT_DIR,
    exe_mode=config.EXE_MODE,
    build_settings=build_settings,
    cli_settings=cli_settings,
    settings=config.settings,
    settings_manager=config.settings_manager,
    server=server,
)
