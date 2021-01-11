from .classes.account import Account
from . import logs_manager as log
import sys
from os.path import dirname, abspath
import os


def get_accounts() -> list:
    accounts = []
    directory = dirname(dirname(dirname(abspath(__file__))))
    try:
        f = open(directory + '/data/accounts.txt', 'r')
    except FileNotFoundError:
        log.error('File accounts.txt not found, create one and put accounts in.')
        sys.exit(0)

    for account in f:
        account = account.strip().split(':')
        if len(account) >= 5:
            account = Account(
                email=account[0],
                password=account[1],
                security_questions=[
                    account[2], account[3], account[4]
                ]
            )

            accounts.append(account)
            continue
        elif len(account) == 2:
            account = Account(
                email=account[0],
                password=account[1]
            )

            accounts.append(account)
            continue

    f.close()
    return accounts


def get_writable_account(account):
    if len(account.security_questions) == 0:
        return account.email + ":" + account.password
    return account.email + ":" + account.password + ":".join(account.security_questions)
