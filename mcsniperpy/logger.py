from colorama import Fore, init

init()


def info(message):
    print(f"{Fore.WHITE}[{Fore.CYAN}info{Fore.WHITE}] {message}")


def warn(message):
    print(f"{Fore.WHITE}[{Fore.YELLOW}warn{Fore.WHITE}] {message}")


def error(message):
    print(f"{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}] {message}")


def verbose(message):
    print(f"{Fore.WHITE}[{Fore.CYAN}debug{Fore.WHITE}] {message}")


def custom_input(message):
    print(f"{Fore.WHITE}[{Fore.CYAN}input{Fore.WHITE}]", end=" ")
