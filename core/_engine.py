import soundcard as sc
import threading

from config import settings

samplerate = settings.samplerate
blocksize = settings.blocksize


class AudioInput:
    def __init__(self):
        self.running = False
        self.parameters = None
        self.parameters = {
            'name': settings.name,
            'device': sc.default_microphone().name,
            'samplerate': samplerate,
            'blocksize': blocksize,
        }
        self._component_stop = threading.Event()

    def _audio_input_consumer(self, audio_input, callback):
        """Потребитель входного аудио, опрос микрофона с заданным samlerate"""
        with audio_input.recorder(samplerate=samplerate, channels=1) as input_recorder:
            while not self._component_stop.is_set():
                chunk = input_recorder.record(numframes=blocksize)
                if callback is not None and callable(callback):
                    callback(chunk)

    def start(self, callback):
        """Старт записи микрофона (входной PCM)"""
        if self.running:
            return
        self._component_stop.clear()
        self.running = True
        audio_input = sc.default_microphone()
        threading.Thread(
            target=self._audio_input_consumer,
            kwargs={'audio_input': audio_input, 'callback': callback}
        ).start()

    def stop(self):
        """Остановка записи микрофона"""
        if self.running is not None:
            self._component_stop.set()
            self.running = False


if __name__ == '__main__':
    recorder = AudioInput()
    print(recorder.parameters)  # можно смотреть текущие настройки
    # при запуске передать callback функцию которая будет обрабатывать чанки, например отправка по websockets
    recorder.start(callback=lambda chunk: print(chunk[:10]))
    input()
    recorder.stop()
