import readchar
from colorama import Fore


def ask_yes_no(question):
    print(Fore.BLUE + "[input] " + Fore.RESET + question + " (y/n)" + ": ", end='')
    while True:
        # takes an input using readchar's readkey function
        choice = readchar.readkey()
        # checks if the input is y, n, or an incorrect option. Loops again if incorrect.
        if choice == 'y':
            print('')
            return True
        elif choice == 'n':
            print('')
            return False
        else:
            print(f"please choose y or n, not \"{choice}\".")
