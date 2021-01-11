import logging

try:
    from colorama import Fore, init
except ImportError:
    print("You are missing the required modules | Please refer to the usage on how to install")
    quit()

init()
logging.basicConfig(level=logging.INFO, format='%(message)s')

sent_reqs = 0


def print_title():
    title = f"""
{Fore.CYAN}┌──────────────────────────────────────────────────────────────────────────────────────┐
{Fore.CYAN}│{Fore.RESET}  ███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ {Fore.BLUE}██████╗ ██╗   ██╗{Fore.CYAN}   │
{Fore.CYAN}│{Fore.RESET}  ████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗{Fore.BLUE}██╔══██╗╚██╗ ██╔╝{Fore.CYAN}   │
{Fore.CYAN}│{Fore.RESET}  ██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝{Fore.BLUE}██████╔╝ ╚████╔╝{Fore.CYAN}    │
│{Fore.RESET}  ██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗{Fore.BLUE}██╔═══╝   ╚██╔╝     {Fore.CYAN}│
│{Fore.RESET}  ██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║{Fore.BLUE}██║        ██║      {Fore.CYAN}│
│{Fore.RESET}  ╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝{Fore.BLUE}╚═╝        ╚═╝      {Fore.CYAN}│
{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────────────┘
{Fore.GREEN}Developed by @Kqzz#0001 on Discord {Fore.BLUE}| Discord server: https://discord.gg/jZm4qNF
{Fore.GREEN}THIS SNIPER IS 100% FREE ON GITHUB{Fore.RESET} UPDATED BY @zyl#0003"""
    print(title)



def custom_info(message):
    logging.info(f"{Fore.WHITE}[{Fore.BLUE}info{Fore.WHITE}] {Fore.RESET}{message}")


def custom_input(message):
    print(f"{Fore.WHITE}[{Fore.BLUE}input{Fore.WHITE}] {Fore.RESET}", end='')
    input_return = input(message)
    return input_return


def check_resp(status):
    if str(status)[0] == str(2):
        return True
    else:
        return False


def resp_error(message):
    print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] {message}")
