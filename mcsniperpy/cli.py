import asyncio
import shutil

import typer

from .sniper import Sniper
from .util import logs_manager as log
from .util import ping_tester

app = typer.Typer()


def startup():
    width = shutil.get_terminal_size().columns
    print(f"""{log.Color.cyan}
    ███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗
    ████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝
    ██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝ 
    ██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝   ╚██╔╝  
    ██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║██║        ██║   
    ╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝   
    """.center(width))
    print(f"{log.Color.cyan}Created by Kqzz#0001")
    print(f"Git: github.com/MCSniperPY | Discord: https://mcsniperpy.github.io/discord{log.Color.white}")


sniper = Sniper(
    log.Color,
    log.Logger
)


@app.command()
def snipe(username: str = typer.Argument(None),
          offset: int = typer.Argument(None),
          debug: bool = typer.Option(False),
          color: bool = typer.Option(True)):
    if debug:
        sniper.log.debug_enabled = True

    if not color:
        sniper.color.disable()

    startup()

    asyncio.get_event_loop().run_until_complete(sniper.run(username, offset))


@app.command()
def ping(iterations: int = typer.Option(5)):
    asyncio.get_event_loop().run_until_complete(ping_tester.ping_test(iterations))


@app.command()
def init():
    sniper.init()


def cli():
    try:
        app()
    except Exception as ex:
        tb = ex.__traceback__
        sniper.log.error(f"type: {type(ex).__name__}")
        sniper.log.error(f"message: {str(ex)}")
        while tb is not None:
            sniper.log.error(f"{tb.tb_frame.f_code.co_filename}:{tb.tb_lineno}")
            tb = tb.tb_next

    sniper.on_shutdown()
