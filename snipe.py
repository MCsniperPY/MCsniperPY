import logs_manager as log
import sys
import utils

if __name__ == "__main__":
    log.on_load()
    log.info("Loading accounts from file.")

    accounts = utils.get_accounts()
    if len(accounts) == 0:
        log.error("No accounts were loaded from file. Please check accounts.txt and try again.")
        sys.exit(0)

    log.info(f"{len(accounts)} account(s) have been loaded from file.")
