import os
import sys
from typing import List

from mcsniperpy.util.classes.account import Account
from mcsniperpy.util.logs_manager import Logger as log
from mcsniperpy.util.request_manager import RequestManager


def is_float(num):
    """Checks if a number is a valid float

    Args:
        n: number to check
    Returns:
        a boolean saying if n is a valid float"""
    try:
        float(num)
        return True
    except ValueError:
        return False


def parse_accs(file_path) -> List[Account]:
    accounts = list()
    log.debug(f"accounts path: {file_path}")
    if os.path.isfile(file_path):
        lines = [line.strip().split(":") for line in open(file_path).readlines()]
    else:
        log.error("accounts.txt file not found!")
        close(1)
    # ^ reads every line from a file and splits into a :
    for (
        line
    ) in lines:
        # This variable cannot be referenced before assignment due to close()
        if line[0].startswith("#"):
            pass  # This line is ignored because it is a "comment"
        elif len(line) in (2, 5):
            accounts.append(
                Account(*line)
            )  # While this line is difficult to read, it creates an Account object.
        else:
            log.error(f"accounts.txt invalid account on line {lines.index(line) + 1}")

    log.debug("loaded accounts from file")

    if len(accounts) == 0:
        log.error(
            "No accounts were loaded from file. Please check accounts.txt and try again."
        )
        close(0)

    if len(accounts) == 1:
        log.info(f"{len(accounts)} account has been loaded from file.")
    else:
        log.info(f"{len(accounts)} accounts have been loaded from file.")
    return accounts


def parse_accs_string(accounts_string) -> List[Account]:
    accounts = list()
    lines = accounts_string.split("\n")
    for line in lines:
        line = line.split(":")

        if len(line) in (2, 5):
            accounts.append(Account(*line))
        else:
            log.error(f"accounts.txt invalid account on line {lines.index(line) + 1}")

    log.debug("loaded accounts from string")

    if len(accounts) == 0:
        log.error(
            "No accounts were loaded from string. Please check accounts.txt and try again."
        )
        close(0)

    return accounts


def find_acc_by_email(email, accounts):
    for acc in accounts:
        if acc.email == email:
            return acc
    return None


def close(code) -> None:
    sys.exit(code)


async def upcoming(
    session: RequestManager,
    length: int = 3,
    length_op: str = "",
    searches: int = 0,
    url: str = "https://api.kqzz.me/api/namemc/upcoming",
):
    full_url = f"{url}?length_op={length_op}&length={length}&searches={searches}"
    resp, _, resp_json = await session.get(full_url)
    if resp.status < 300:
        return resp_json

    return None
