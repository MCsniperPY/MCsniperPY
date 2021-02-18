from .classes.account import Account
from .logs_manager import Logger as log
import sys
from os.path import dirname, abspath
import os


def get_accounts() -> list:
    accounts = []

    directory = dirname(dirname(__file__))
    log.debug("grabbed accounts dir")

    try:
        f = open(directory + '/data/accounts.txt', 'r')
        log.debug("opened accounts.txt")
    except FileNotFoundError:
        log.error('File accounts.txt not found, create one and put accounts in.')
        sys.exit(0)

    for account in f:
        account = account.strip().split(':')
        log.debug("parsed account into split string")
        if len(account) == 5:
            account = Account(
                email=account[0],
                password=account[1],
                security_questions=[
                    account[2], account[3], account[4]
                ]
            )

            accounts.append(account)
            log.debug("parsed into account object")
            continue
        elif len(account) == 2:
            account = Account(
                email=account[0],
                password=account[1]
            )

            accounts.append(account)
            log.debug("parsed into account object")
            continue

    log.debug("parsed all accounts")
    return accounts
