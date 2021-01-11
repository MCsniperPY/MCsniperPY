from colorama import Fore, init
import shutil

init(autoreset=True)


def info(message):
    print(f"{Fore.WHITE}[{Fore.CYAN}info{Fore.WHITE}] {message}")


def warn(message):
    print(f"{Fore.WHITE}[{Fore.YELLOW}warn{Fore.WHITE}] {message}")


def error(message):
    print(f"{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}] {message}")


def success(message):
    print(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}] {message}")


def debug(message):
    return (f"{Fore.WHITE}[{Fore.LIGHTCYAN_EX}debug{Fore.WHITE}] %(message)s")


def custom_input(message) -> input:
    i = input(f"{Fore.WHITE}[{Fore.CYAN}input{Fore.WHITE}] {message}")
    return i


def on_load():
    width = shutil.get_terminal_size().columns
    print(f"{Fore.CYAN}MCSniperPY".center(width))
    print(f"{Fore.CYAN}Created by Kqzz#0001".center(width))
    print(f"github.com/MCSniperPY | discord.com/invite/yp69ZqtxNk".center(width))
    print("[+] You are on the latest version [+]".center(width))
