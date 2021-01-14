import shutil

import colorama
from colorama import init

init()
logs = []


class Color:

    def __init__(self, color=True):
        if color:
            self.red = colorama.Fore.RED
            self.l_red = colorama.Fore.LIGHTRED_EX
            self.green = colorama.Fore.GREEN
            self.l_green = colorama.Fore.LIGHTGREEN_EX
            self.yellow = colorama.Fore.YELLOW
            self.l_yellow = colorama.Fore.LIGHTYELLOW_EX
            self.blue = colorama.Fore.BLUE
            self.l_blue = colorama.Fore.LIGHTBLUE_EX
            self.magenta = colorama.Fore.MAGENTA
            self.l_magenta = colorama.Fore.LIGHTMAGENTA_EX
            self.cyan = colorama.Fore.CYAN
            self.l_cyan = colorama.Fore.LIGHTCYAN_EX
            self.white = colorama.Fore.WHITE
        else:
            self.disable()

    def disable(self):
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

    def enable(self):
        self.red = colorama.Fore.RED
        self.l_red = colorama.Fore.LIGHTRED_EX
        self.green = colorama.Fore.GREEN
        self.l_green = colorama.Fore.LIGHTGREEN_EX
        self.yellow = colorama.Fore.YELLOW
        self.l_yellow = colorama.Fore.LIGHTYELLOW_EX
        self.blue = colorama.Fore.BLUE
        self.l_blue = colorama.Fore.LIGHTBLUE_EX
        self.magenta = colorama.Fore.MAGENTA
        self.l_magenta = colorama.Fore.LIGHTMAGENTA_EX
        self.cyan = colorama.Fore.CYAN
        self.l_cyan = colorama.Fore.LIGHTCYAN_EX
        self.white = colorama.Fore.WHITE


class Logger:

    def __init__(self):
        self.info_enabled = True
        self.warn_enabled = True
        self.error_enabled = True
        self.success_enabled = True
        self.debug_enabled = True

    def info(self, message):
        if self.info_enabled:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}info{colorama.Fore.WHITE}] {message}")

    def warn(self, message):
        if self.warn_enabled:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}warn{colorama.Fore.WHITE}] {message}")

    def error(self, message):
        if self.error_enabled:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.RED}error{colorama.Fore.WHITE}] {message}")

    def success(self, message):
        if self.succcess_enabled:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.GREEN}success{colorama.Fore.WHITE}] {message}")

    def debug(self, message):
        if self.debug_enabled:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTCYAN_EX}debug{colorama.Fore.WHITE}] {message}")

    def custom_input(self, message) -> str:
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}input{colorama.Fore.WHITE}] {message}", end=" ")
        i = input()
        return i

    def shutdown(self):
        # Does nothing.
        # Could be used to:
        # send all logs to a discord channel,
        # send logs to a file uploading service to check back on later,
        # etc...
        pass


def on_load():
    width = shutil.get_terminal_size().columns
    print(f"""{color.cyan}███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗
████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝
██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝ 
██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝   ╚██╔╝  
██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║██║        ██║   
╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝   
""".center(width))
    print(f"{color.cyan}Created by Kqzz#0001".center(width))
    print(f"Git: github.com/MCSniperPY | Discord: https://mcsniperpy.github.io/discord".center(width))

    # print("[+] You are on the latest version [+]".center(width))
