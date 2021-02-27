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
        close(1)
    # ^ reads every line from a file and splits into a :
    for line in lines:  # This variable cannot be referenced before assignment due to close()

        if len(line) in (2, 5):
            accounts.append(Account(*line))
        else:
            log.error(f"accounts.txt invalid account on line {lines.index(line) + 1}")

    log.debug("loaded accounts from file")

    if len(accounts) == 0:
        log.error("No accounts were loaded from file. Please check accounts.txt and try again.")
        close(0)

    if len(accounts) == 1:
        log.info(f"{len(accounts)} account has been loaded from file.")
    else:
        log.info(f"{len(accounts)} accounts have been loaded from file.")
    return accounts


def parse_accs_string(accounts_string) -> List[Account]:
    accounts = list()
    for line in accounts_string.split('\n'):

        if len(line) in (2, 5):
            accounts.append(Account(*line))
        else:
            log.error(f"accounts.txt invalid account on line {lines.index(line) + 1}")

    log.debug("loaded accounts from string")

    if len(accounts) == 0:
        log.error("No accounts were loaded from string. Please check accounts.txt and try again.")
        close(0)

    if len(accounts) == 1:
        log.info(f"{len(accounts)} account has been loaded from string.")
    else:
        log.info(f"{len(accounts)} accounts have been loaded from string.")
    return accounts


def close(code) -> None:
    log.input(f"Press enter to exit:")
    sys.exit(code)
