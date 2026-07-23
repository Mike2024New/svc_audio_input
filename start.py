import os
import sys
import subprocess
from pathlib import Path

"""
Стандарт : пусковой стартовый скрипт, для сборки зависимостей и скачивания необходимых компонентов.
"""

# удалить старый uv lock, так как он может помешать обновлению
uv_lock_path = Path('./uv.lock')
if uv_lock_path.exists():
    os.remove(uv_lock_path)

cmd = [sys.executable, '-m', 'pip', 'install', 'uv']
subprocess.run(cmd, shell=False)

# загрузка всех необходимых пакетов
cmd = [sys.executable, '-m', 'uv', 'sync']
subprocess.run(cmd, shell=False)
