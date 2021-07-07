import configparser
import os
from pathlib import Path

from ..logs_manager import Logger as log
from ..utils import close

MCSNIPERPY_BACKEND_DIR = os.path.join(str(Path.home()), ".mcsniperpy")
MCSNIPERPY_CONFIG_FILE_PATH = os.path.join(
    MCSNIPERPY_BACKEND_DIR, "backend_config.ini")

DEFAULT_ACCOUNTS_FILE = """Clear this file and write accounts in this format
email:pass:answer:answer:answer

or

email:pass

you can separate those accounts by a new line if you would like to use multiple accounts.

# You can comment line out by making them start with a #"""


class BackConfig:
    """Backend configuration for MCsniperPY

    The main purpose of this is to store the path for the \"frontend\" directory.
    The frontend directory stores the config file and accounts file."""

    def __init__(self):

        self.config = configparser.ConfigParser()

        if not os.path.isdir(MCSNIPERPY_BACKEND_DIR):
            os.mkdir(MCSNIPERPY_BACKEND_DIR)

        if os.path.isfile(MCSNIPERPY_CONFIG_FILE_PATH):
            self.config.read(MCSNIPERPY_CONFIG_FILE_PATH)
        else:
            log.error("Failed to find MCsniperPY directory")
            log.info(
                "To fix this open your sniping folder (or make one) and type"
                " `mcsniperpy init` in it."
            )
            log.info(
                "Next, just re-run the sniper with the command you used to get here."
            )
            close(1)

        if not self.validate_sections():
            log.error(
                "invalid config file. please make sure it looks like:\n[sniper]\ninit_path ="
            )
            close(1)

    def validate_sections(self):
        necessary_sections = ["sniper"]
        sections = self.config.sections()
        log.debug(sections)
        return sections == necessary_sections


class Config:
    def __init__(self, config_path):
        log.debug(f"config path: {config_path}")
        user_config = configparser.ConfigParser(allow_no_value=True)
        user_config.read(config_path)

        self.config = user_config


def create_user_config() -> configparser.ConfigParser:
    user_config = configparser.ConfigParser(allow_no_value=True)
    user_config["sniper"] = {
        "timing_system": "ckm",
        "auto_claim_namemc": "no",
        "snipe_requests": "3",
    }

    user_config["accounts"] = {
        "max_accounts": "30",
        "authentication_delay": "500",
        "start_authentication": "720",
    }

    user_config["skin"] = {
        "change_skin_on_snipe": "no",
        "skin_change_type": "url",
        "skin": "",
        "skin_variant": "classic ;or slim"
    }

    user_config["announce"] = {
        "announce_snipe": "no",
        "announce_code": "",
        "webhook_urls": "",
        "webhook_format": "sniped `{name}` with `{searches}` searches!",
    }

    user_config.set(
        "skin",
        "; skin_change_type can be url, path, or username."
        "refer to docs for more info.",
    )

    return user_config


def populate_configs(no_confirm=False):
    if not no_confirm:
        if not log.yes_or_no(
            "Are you sure you want to initialize your config in your cwd:"
        ):
            close(1)

    config = configparser.ConfigParser()
    config["sniper"] = {"init_path": os.getcwd()}

    if not os.path.isdir(MCSNIPERPY_BACKEND_DIR):
        os.mkdir(MCSNIPERPY_BACKEND_DIR)

    with open(MCSNIPERPY_CONFIG_FILE_PATH, "w") as file:
        config.write(file)

    accounts_path = os.path.join(config["sniper"]["init_path"], "accounts.txt")
    user_config_path = os.path.join(
        config["sniper"]["init_path"], "config.ini")

    if os.path.isfile(accounts_path):
        if log.yes_or_no("Overwrite current accounts file:"):
            with open(
                os.path.join(config["sniper"]["init_path"],
                             "accounts.txt"), "w"
            ) as file:
                file.write(DEFAULT_ACCOUNTS_FILE)
    else:
        with open(
            os.path.join(config["sniper"]["init_path"], "accounts.txt"), "w"
        ) as file:
            file.write(DEFAULT_ACCOUNTS_FILE)

    if os.path.isfile(user_config_path):
        if log.yes_or_no("Overwrite current config file:"):
            with open(
                os.path.join(config["sniper"]["init_path"], "config.ini"), "w"
            ) as file:
                create_user_config().write(file)
    else:
        with open(
            os.path.join(config["sniper"]["init_path"], "config.ini"), "w"
        ) as file:
            create_user_config().write(file)

    log.info("successfully initialized sniper")
