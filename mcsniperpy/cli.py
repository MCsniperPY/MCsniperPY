import asyncio
import shutil

import typer

from mcsniperpy import Sniper
from mcsniperpy.util import logs_manager as log
from mcsniperpy.util import ping_tester
from mcsniperpy.util.name_system import next_name
from mcsniperpy.util.offset_calculator import OffsetCalculator

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
def snipe(username: str = typer.Option(None, help="The username to attempt a snipe on"),
          offset: int = typer.Option(None, help="The offset you want to use for the target username."),
          debug: bool = typer.Option(False, help="Enable debug mode."),
          color: bool = typer.Option(True, help="Colored terminal output"),
          next_sorry: int = typer.Option(None, '--next', help='Snipe the next available username.'
                                         ' It is not recommended to use this!')):
    """
    Snipe a minecraft username!
    """
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
def ping(iterations: int = typer.Option(5, help='How many times to ping Mojang\'s servers.')):
    """
    Test your ping to Mojang's servers
    """
    asyncio.get_event_loop().run_until_complete(ping_tester.ping_test(iterations))
    sniper.on_shutdown()


@app.command()
def offset_test(accuracy: int = typer.Option(20, help="How accurate do you want your offset to be?"),
                aim_for: float = typer.Option(.15, help="What time do you want to aim for?")):
    """
    Find the optimal offset for you. Note: this is not entirely accurate since it does not compensate for api lag caused\
 by other snipers
    """
    offset_calc = OffsetCalculator(accuracy=accuracy, aim_for=aim_for)
    asyncio.get_event_loop().run_until_complete(offset_calc.run())


@app.command()
def init():
    """
    Initialize MCsniperPY to be able to snipe names. This is an essential step before sniping. Please read the docs for\
 more info. https://docs.mcsnierpy.com
    """
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
