import colorama
from colorama import init

from typing import List

init(autoreset=True)
logs = List[str]


class Color:
    red = colorama.Fore.RED
    l_red = colorama.Fore.LIGHTRED_EX
    green = colorama.Fore.GREEN
    l_green = colorama.Fore.LIGHTGREEN_EX
    yellow = colorama.Fore.YELLOW
    l_yellow = colorama.Fore.LIGHTYELLOW_EX
    blue = colorama.Fore.BLUE
    l_blue = colorama.Fore.LIGHTBLUE_EX
    magenta = colorama.Fore.MAGENTA
    l_magenta = colorama.Fore.LIGHTMAGENTA_EX
    cyan = colorama.Fore.CYAN
    l_cyan = colorama.Fore.LIGHTCYAN_EX
    white = colorama.Fore.WHITE
    reset = colorama.Fore.RESET

    @classmethod
    def disable(cls):
        cls.red = ""
        cls.l_red = ""
        cls.green = ""
        cls.l_green = ""
        cls.yellow = ""
        cls.l_yellow = ""
        cls.blue = ""
        cls.l_blue = ""
        cls.magenta = ""
        cls.l_magenta = ""
        cls.cyan = ""
        cls.l_cyan = ""
        cls.white = ""
        cls.reset = ""

    @classmethod
    def enable(cls):
        cls.red = colorama.Fore.RED
        cls.l_red = colorama.Fore.LIGHTRED_EX
        cls.green = colorama.Fore.GREEN
        cls.l_green = colorama.Fore.LIGHTGREEN_EX
        cls.yellow = colorama.Fore.YELLOW
        cls.l_yellow = colorama.Fore.LIGHTYELLOW_EX
        cls.blue = colorama.Fore.BLUE
        cls.l_blue = colorama.Fore.LIGHTBLUE_EX
        cls.magenta = colorama.Fore.MAGENTA
        cls.l_magenta = colorama.Fore.LIGHTMAGENTA_EX
        cls.cyan = colorama.Fore.CYAN
        cls.l_cyan = colorama.Fore.LIGHTCYAN_EX
        cls.white = colorama.Fore.WHITE
        cls.reset = colorama.Fore.RESET


class Logger:
    logs = []

    info_enabled = True
    warn_enabled = True
    error_enabled = True
    success_enabled = True
    debug_enabled = False

    @classmethod
    def info(cls, message):

        formatted = f"{Color.white}[{Color.cyan}info{Color.white}] {message}"

        if cls.info_enabled:
            print(formatted)

    @classmethod
    def warn(cls, message):

        formatted = f"{Color.white}[{Color.yellow}warn{Color.white}] {message}"

        if cls.warn_enabled:
            print(formatted)

        cls.logs.append(formatted)

    @classmethod
    def error(cls, message):

        formatted = f"{Color.white}[{Color.red}error{Color.white}] {message}"

        if cls.error_enabled:
            print(formatted)

        cls.logs.append(formatted)

    @classmethod
    def success(cls, message):

        formatted = f"{Color.white}[{Color.green}success{Color.white}] {message}"

        if cls.success_enabled:
            print(f"{Color.white}[{Color.green}success{Color.white}] {message}")

        cls.logs.append(formatted)

    @classmethod
    def debug(cls, message):

        formatted = f"{Color.white}[{Color.l_cyan}debug{Color.white}] {message}"

        if cls.debug_enabled:
            print(formatted)

        cls.logs.append(formatted)

    @classmethod
    def input(cls, message) -> str:

        formatted = f"{Color.white}[{Color.cyan}input{Color.white}] {message}"

        print(formatted, end=" ")
        i = input()

        cls.logs.append(formatted + " " + i)

        return i

    @classmethod
    def yes_or_no(cls, message):
        i = str()
        while True:
            i = cls.input(
                f"{Color.white}[{Color.green}yes{Color.white}/{Color.l_red}no{Color.reset}]{Color.reset} "
                f"{message}"
            ).lower()
            if i in ("yes", "y"):
                return True
            elif i in ("no", "n"):
                return False
            else:
                cls.error(f"{i} is not a valid answer. please answer yes or no.")

    @classmethod
    def shutdown(cls):
        # Does nothing.
        # Could be used to:
        # send all logs to a discord channel,
        # send logs to a file uploading service to check back on later,
        # etc...
        pass
