import readchar


def ask_yes_no(question):
    print(question + " (y/n)" + ": ")
    while True:
        # takes an input using readchar's readkey function
        choice = readchar.readkey()
        # checks if the input is y, n, or an incorrect option. Loops again if incorrect.
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print(f"please choose y or n, not \"{choice}\".")

# Runs only if the file is being run directly rather than being imported as a module


if __name__ == '__main__':
    print(ask_yes_no("yes or no?"))
