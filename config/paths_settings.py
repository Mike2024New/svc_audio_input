import sys
from pathlib import Path

# определение корневой точки приложения
ROOT_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent

# папка с логами
LOGS_FILE_PATH = ROOT_DIR / 'logs' / 'log.jsonl'
LOGS_FILE_PATH.parent.mkdir(exist_ok=True, parents=True)
JSON_SETTINGS_FILE_PATH = Path(ROOT_DIR / 'settings.json')
