from config import paths_settings
from config import settings
from infrastructure_builder import BuildParameters

"""
Настройка сборки .exe (bin) файла приложения.
"""

build_settings = BuildParameters(
    name=settings.name,
    entry_point_path=paths_settings.ROOT_DIR / 'cli.py',
    one_file=True,
    create_resources_symlink=False,
    open_folder=False,
    # опционально, списки с дополнительными зависимостями для приложений ( ассеты, бинарные файлы)
    add_data=[],
    add_binary=[],
    # через cli можно дополнительно задать copy_from_dist_to_target_dir -> параметр -ct в нём путь распаковки дистрибутива
)
