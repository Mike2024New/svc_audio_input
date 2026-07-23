import config
import typer
from infrastructure_cli_utils import get_cli_app, cli_command_execute
from core import server
from typing import Literal

# получение базовых повторяющихся команд
app = get_cli_app(
    name=config.APP_NAME,
    root_dir=config.ROOT_DIR,
    exe_mode=config.EXE_MODE,
)


@app.command()
def run(
        ctx: typer.Context,
        port: int = typer.Option(8000, '--port', '-p'),
        log_level: Literal['debug', 'info', 'warning', 'error'] = typer.Option('warning', '--log-level', '-ll')

):
    """
    Запуск сервера слушающего микрофон.
    Для того, чтобы получать pcm, использовать websockets, подключась к url: 'ws://localhost:{port}/ws', например для
    порта 8000 uri будет выглядеть: `ws://localhost:8000/ws`
    Опции:
        -p (--port) - порт на котором будет запущен сервер (по умолчанию 8000)
        -ll (--log-level) - минимальный уровень логирования ('debug', 'info', 'warning', 'error')
    """
    cli_command_execute(
        lambda: server.start(port=port, log_level=log_level),
        command_name=ctx.command.name,
    )
    return


if __name__ == '__main__':
    app()
