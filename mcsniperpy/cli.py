import logs_manager as log
import typer
from logs_manager import Color

app = typer.Typer()
color = Color(True)


@app.command()
def run(name: str = typer.Argument(...)):
    log.info(f"{color.blue} Welcome to MCsniperPY!")


def cli():
    app()
