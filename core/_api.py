import asyncio
from infrastructure_server import server_factory
from core._engine import AudioInput
from fastapi import APIRouter, WebSocket
from config import settings, message_bus_add

ATTEMPTS_LIMIT = 5  # количество пропущенных чанков (после этого сокет закрывается)

__all__ = ['server']
app_router = APIRouter(tags=[settings.name])

audio_input = AudioInput()
queue = asyncio.Queue()  # безразмерная очередь для передачи чанков
stop_recorder = asyncio.Event()


def callback(chunk):
    # Преобразование чанка из numpy array в список (для сериализации в json)
    chunk_list = chunk.flatten().tolist() if hasattr(chunk, 'tolist') else list(chunk)
    queue.put_nowait(chunk_list)  # запись чанка в очередь


@app_router.get('/parameters/')
def parameters():
    """Текущие параметры компонента"""
    return audio_input.parameters


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


server = server_factory(component=audio_input, routers_list=[app_router], message_bus=message_bus_add)

if __name__ == '__main__':
    """Пример использования"""
    from time import sleep
    import threading


    def start_server():
        server.start(port=8000, log_level='warning')  # запуск сервера из внешних api


    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    input(f'Наж enter чтобы остановить сервер.\n')
    server.stop()
    server_thread.join(timeout=2)
