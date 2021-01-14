import typer

from .sniper import Sniper
from .util import logs_manager as log

app = typer.Typer()

sniper = Sniper(
    log.Color(),
    log.Logger()
)


@app.command()
def snipe(username: str,
          delay: int,
          debug: bool = typer.Option(False)):
    if debug:
        sniper.logger.debug_enabled = True

    sniper.run()


@app.command()
def ping():
    #
    pass


def cli():
    try:
        app()
    except Exception as ex:
        tb = ex.__traceback__
        nl = "\n"
        sniper.logger.error(f"type: {type(ex).__name__}\nmessage: {str(ex)}")
        while tb is not None:
            sniper.logger.error(f"{tb.tb_frame.f_code.co_filename}:{tb.tb_lineno}")
            tb = tb.tb_next

    print("done")
