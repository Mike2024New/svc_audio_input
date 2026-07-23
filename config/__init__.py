import platform, sys
from pathlib import Path

__all__ = [
    'ROOT_DIR',
]
APP_NAME = 'llm'
IS_WINDOWS = 'windows' in platform.system().lower()

# для сборщика (pyinstaller)
EXE_MODE = getattr(sys, 'frozen', False)

# определение корневой точки приложения
ROOT_DIR = Path(sys.executable).parent if EXE_MODE else Path(__file__).parent.parent
