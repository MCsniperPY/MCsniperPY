from time import time
import requests
from datetime import timedelta
from colorama import Fore, init
import readchar
init()


def get_latency(added_latency):
    start_latency = time()
    requests.post(f"https://api.mojang.com/")
    latency = time() - start_latency
    latency = latency * 1000 * 3 + added_latency
    latency = timedelta(milliseconds=latency)
    print("sniping", latency, "ms before drop time.")
    return latency


def print_title():
    print("\n")
    print(f"""
{Fore.CYAN}┌──────────────────────────────────────────────────────────────────────────────────────┐
{Fore.CYAN}│{Fore.RESET}  ███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ {Fore.BLUE}██████╗ ██╗   ██╗
{Fore.CYAN}│{Fore.RESET}  ████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗{Fore.BLUE}██╔══██╗╚██╗ ██╔╝
{Fore.CYAN}│{Fore.RESET}  ██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝{Fore.BLUE}██████╔╝ ╚████╔╝     
 {Fore.RESET}  ██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗{Fore.BLUE}██╔═══╝   ╚██╔╝     {Fore.CYAN}│
 {Fore.RESET}  ██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║{Fore.BLUE}██║        ██║      {Fore.CYAN}│
 {Fore.RESET}  ╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝{Fore.BLUE}╚═╝        ╚═╝      {Fore.CYAN}│
{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────────────┘
{Fore.GREEN}Developed by @Kqzz#0001 on Discord {Fore.BLUE}| Discord server: https://discord.gg/jZm4qNF
{Fore.GREEN}THIS SNIPER IS 100% FREE ON GITHUB""", Fore.RESET)
# The outer border of the main text was inspired by typhon sniper | Yeah. I know that this looks like a mess but it actually looks good when rendered properly.


def ask_option(options):
    i = 1
    # loop through options and print
    custom_info(f"select a number 1 - {len(options)}")
    for option in options:
        print(f"{i}). {option}")
        i += 1
    # main function loop
    # Doesn't end until a correct answer is given
    while True:
        try:
            # takes an input using readchar's readkey function
            choice = int(readchar.readkey())
            options[choice - 1]
            # returns the option the user selected by list index
            return choice - 1
        except (ValueError, IndexError):
            print("please enter a valid option")


def custom_input(message):
    print(f"{Fore.BLUE}[input] {Fore.RESET}", end='')
    input_return = input(message)
    return input_return


def custom_info(message):
    print(f"{Fore.BLUE}[info] {Fore.RESET}{message}")
