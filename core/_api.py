import asyncio
from infrastructure_server import server_factory
from core._engine import AudioInput
from fastapi import APIRouter, WebSocket

ATTEMPTS_LIMIT = 5  # количество пропущенных чанков (после этого сокет закрывается)

__all__ = ['server']
app_router = APIRouter(tags=['audio_input'])

audio_input = AudioInput()
queue = asyncio.Queue()  # безразмерная очередь для передачи чанков
stop_recorder = asyncio.Event()


def callback(chunk):
    # Преобразование чанка из numpy array в список (для сериализации в json)
    chunk_list = chunk.flatten().tolist() if hasattr(chunk, 'tolist') else list(chunk)
    queue.put_nowait(chunk_list)  # запись чанка в очередь


@app_router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Клиент подключился")

    # запуск микрофона, в качестве callback функция которая добавляет чанк в очередь
    audio_input.start(callback=callback)

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
        audio_input.stop()
        try:
            await websocket.close()
        except (RuntimeError, Exception):
            pass  # соединение уже закрыто
        stop_recorder.clear()
        print(f'Соединение остановлено')


server = server_factory(component=audio_input, routers_list=[app_router])

if __name__ == '__main__':
    server.start(port=8000, log_level='debug')
