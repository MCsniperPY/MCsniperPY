import asyncio
import shutil

import typer

from mcsniperpy import Sniper
from mcsniperpy.util import logs_manager as log
from mcsniperpy.util import ping_tester
from mcsniperpy.util.name_system import next_name

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
def snipe(username: str = typer.Option(None),
          offset: int = typer.Option(None),
          debug: bool = typer.Option(False),
          color: bool = typer.Option(True),
          next_sorry: int = typer.Option(None, '--next')):
    if debug:
        sniper.log.debug_enabled = True

    if not color:
        sniper.color.disable()

    if next_sorry is not None:
        username = next_name(searches=next_sorry)

    startup()

    asyncio.get_event_loop().run_until_complete(sniper.run(username, offset))
    sniper.on_shutdown()


@app.command()
def ping(iterations: int = typer.Option(5)):
    asyncio.get_event_loop().run_until_complete(ping_tester.ping_test(iterations))
    sniper.on_shutdown()


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
    finally:
        sniper.on_shutdown()


if __name__ == '__name__':
    cli()
