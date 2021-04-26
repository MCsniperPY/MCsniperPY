import asyncio

import typer

from mcsniperpy import Sniper
from mcsniperpy.util import logs_manager as log
from mcsniperpy.util import ping_tester
from mcsniperpy.util.name_system import next_name
from mcsniperpy.util.offset_calculator import OffsetCalculator

app = typer.Typer()


def startup():
    title = f"""{log.Color.cyan}
 ███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ \
 {log.Color.blue}██████╗ {log.Color.blue}██{log.Color.blue}╗  {log.Color.blue}\
 ██╗
 ████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗\
 {log.Color.blue}██╔══{log.Color.blue}██╗╚{log.Color.blue}██{log.Color.blue}╗\
 {log.Color.blue}██╔╝
 ██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝\
 {log.Color.blue}██{log.Color.blue}████╔╝ ╚{log.Color.blue}████╔╝
 ██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗\
 {log.Color.blue}█{log.Color.blue}█╔═══╝   ╚{log.Color.blue}██╔╝
 ██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║\
 {log.Color.blue}██║        {log.Color.blue}██║
 ╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝\
 ╚═╝        ╚═╝
"""
    lines = "╗║╔═╝╚"
    for line_type in lines:
        title = title.replace(
            line_type, f"{log.Color.white}%s{log.Color.cyan}" % line_type)
    print(title)
    print(f"{log.Color.cyan}Created by Kqzz#0001")
    print(
        "Git: github.com/MCSniperPY/MCsniperPY | "
        f"Discord: https://mcsniperpy.com/discord{log.Color.white}"
    )


sniper = Sniper(log.Color, log.Logger)


@app.command()
def snipe(
    username: str = typer.Option(
        None, help="The username to attempt a snipe on"),
    offset: int = typer.Option(
        None, help="The offset you want to use for the target username."
    ),
    debug: bool = typer.Option(False, help="Enable debug mode."),
    color: bool = typer.Option(True, help="Colored terminal output"),
    next_with_searches: int = typer.Option(
        None,
        "--next",
        help="Snipe the next available username."
        " It is not recommended to use this!",
    ),
):
    """
    Snipe a minecraft username!
    """
    if debug:
        sniper.log.debug_enabled = True

    if not color:
        sniper.color.disable()

    if next_with_searches is not None:
        username = next_name(searches=next_with_searches)

    startup()

    asyncio.get_event_loop().run_until_complete(sniper.run(username, offset))
    sniper.on_shutdown()


@app.command()
def ping(
    iterations: int = typer.Option(
        5, help="How many times to ping Mojang's servers.")
):
    """
    Test your ping to Mojang's servers
    """
    asyncio.get_event_loop().run_until_complete(ping_tester.ping_test(iterations))
    sniper.on_shutdown()


@app.command()
def offset_test(
    accuracy: int = typer.Option(
        20, help="How accurate do you want your offset to be?"
    ),
    aim_for: float = typer.Option(
        0.15, help="What time do you want to aim for?"),
):
    """
    Find the optimal offset for you. Note: this is not entirely accurate since\
 it does not compensate for api lag caused
 by other snipers
    """
    offset_calc = OffsetCalculator(accuracy=accuracy, aim_for=aim_for)
    asyncio.get_event_loop().run_until_complete(offset_calc.run())
    offset_calc.on_shutdown()


@app.command()
def init(no_confirm: bool = typer.Option(False, help="remove confirmation message")):
    """
    Initialize MCsniperPY to be able to snipe names. This is an essential step\
 before sniping. Please read the docs for
 more info. https://docs.mcsniperpy.com
    """
    sniper.init(no_confirm=no_confirm)


def cli():
    try:
        app()
    # pylint: disable=broad-except
    except Exception as ex:
        traceback = ex.__traceback__
        sniper.log.error(f"type: {type(ex).__name__}")
        sniper.log.error(f"message: {str(ex)}")
        while traceback is not None:
            # pylint: disable=no-member
            sniper.log.error(
                f"{traceback.tb_frame.f_code.co_filename}:{traceback.tb_lineno}"
            )
            traceback = traceback.tb_next
    finally:
        sniper.on_shutdown()


if __name__ == "__name__":
    cli()
