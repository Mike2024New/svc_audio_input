from pydantic import BaseModel, Field


class Settings(BaseModel):
    name: str
    samplerate: int = Field(
        default=16000,
        description='Частота дискретизации в Гц. 16000 — стандарт для речи'
    )
    blocksize: int = Field(
        default=1024,
        description='Размер аудиоблока в сэмплах. Кратен 160 (если указано не кратное значение то выполняется автоподгонка). Меньше — быстрее реакция, но выше нагрузка'
    )


settings = Settings(name='audio_input')
