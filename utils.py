from account import Account
import logs_manager as log
import sys


def get_accounts() -> list:
    accounts = []

    try:
        f = open('accounts.txt', 'r')
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

    return accounts
