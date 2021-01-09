from colorama import Fore, init

init()


class Color:

    def __init__(self, color=True):
        if color:
            self.red = Fore.RED
            self.l_red = Fore.LIGHTRED_EX
            self.green = Fore.GREEN
            self.l_green = Fore.LIGHTGREEN_EX
            self.yellow = Fore.YELLOW
            self.l_yellow = Fore.LIGHTYELLOW_EX
            self.blue = Fore.BLUE
            self.l_blue = Fore.LIGHTBLUE_EX
            self.magenta = Fore.MAGENTA
            self.l_magenta = Fore.LIGHTMAGENTA_EX
            self.cyan = Fore.CYAN
            self.l_cyan = Fore.LIGHTCYAN_EX
            self.white = color.white
        else:
            self.red = ""
            self.l_red = ""
            self.green = ""
            self.l_green = ""
            self.yellow = ""
            self.l_yellow = ""
            self.blue = ""
            self.l_blue = ""
            self.magenta = ""
            self.l_magenta = ""
            self.cyan = ""
            self.l_cyan = ""
            self.white = ""


def info(message):
    print(f"{color.white}[{color.cyan}info{color.white}] {message}")


def warn(message):
    print(f"{color.white}[{color.yellow}warn{color.white}] {message}")


def error(message):
    print(f"{color.white}[{color.red}error{color.white}] {message}")


def debug(message):
    print(f"{color.white}[{color.l_cyan}debug{color.white}] {message}")


def custom_input(message):
    print(f"{color.white}[{color.cyan}input{color.white}] {message}:", end=" ")
