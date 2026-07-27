import config
import asyncio
from core import Engine
from fastapi import APIRouter, WebSocket

ATTEMPTS_LIMIT = 5  # количество пропущенных чанков (после этого сокет закрывается)

__all__ = [
    'routers_list',
]

app_router = APIRouter(tags=[config.settings.name])

component = Engine()
queue = asyncio.Queue()  # безразмерная очередь для передачи чанков
stop_recorder = asyncio.Event()


def callback(chunk):
    # Преобразование чанка из numpy array в список (для сериализации в json)
    chunk_list = chunk.flatten().tolist() if hasattr(chunk, 'tolist') else list(chunk)
    queue.put_nowait(chunk_list)  # запись чанка в очередь


@app_router.get('/parameters/')
def parameters():
    """Текущие параметры компонента"""
    return component.parameters


@app_router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Клиент подключился")

    # запуск микрофона, в качестве callback функция которая добавляет чанк в очередь
    component.start(callback=callback)

    try:
        # цикл бесконечно посылает чанки
        attempts = 0
        while not stop_recorder.is_set():
            try:
                chunk = await asyncio.wait_for(queue.get(), timeout=1.0)
                await websocket.send_json({'chunk': chunk})
                attempts = 0
            except asyncio.TimeoutError:
                if attempts >= ATTEMPTS_LIMIT:
                    break
                attempts += 1
                continue
    except Exception as err:
        print(err)
    finally:
        component.stop()
        try:
            await websocket.close()
        except (RuntimeError, Exception):
            pass  # соединение уже закрыто
        stop_recorder.clear()
        print(f'Соединение остановлено')


routers_list = [app_router]
