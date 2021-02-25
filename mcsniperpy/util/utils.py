import os
import sys
from typing import List

from .classes.account import Account
from .logs_manager import Logger as log


def parse_accs(file_path) -> List[Account]:
    accounts = list()
    log.debug(f'accounts path: {file_path}')
    if os.path.isfile(file_path):
        lines = [line.strip().split(":") for line in open(file_path).readlines()]
    else:
        log.error("accounts.txt file not found!")
    # ^ reads every line from a file and splits into a :
    for line in lines:

        if len(line) in (2, 5):
            accounts.append(Account(*line))
        else:
            print(f"[err] accounts.txt invalid account on line {lines.index(line) + 1}")

    log.debug("loaded accounts from file")
    return accounts


def close(code) -> None:
    log.input(f"Press enter to exit:")
    sys.exit(code)
