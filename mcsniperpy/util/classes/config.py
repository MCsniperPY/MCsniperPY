import configparser
import os
from os.path import dirname

from ..logs_manager import Logger as log
from ..utils import close


class BackConfig:
    """"""

    def __init__(self):
        config_path = os.path.join(dirname(dirname(dirname(__file__))), "data", "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)

        self.init_path = config["sniper"].get("init_path", "")

        if self.init_path == "":
            log.error("Failed to find MCsniperPY directory")
            log.info("To fix this open your sniping folder (or make one) and type `mcsniperpy init` in it.")
            log.info("Next, just re-run the sniper with the command you used to get here.")
            close(1)

    def load_init_path(self, cwd):
        self.init_path = cwd


class Config:

    def __init__(self, config_path):
        log.debug(f'config path: {config_path}')
        user_config = configparser.ConfigParser(allow_no_value=True)
        user_config.read(config_path)

        self.config = user_config


def populate_configs():
    config = configparser.ConfigParser()
    config['sniper'] = {"init_path": os.getcwd()}

    with open(os.path.join(dirname(dirname(dirname(__file__))), "data", "config.ini"), "w") as f:
        config.write(f)

    if os.path.isfile(os.path.join(config['sniper']['init_path'], "accounts.txt")):
        if log.yes_or_no('yes/no | overwrite current accounts file'):
            with open(os.path.join(config['sniper']['init_path'], "accounts.txt"), "w") as f:
                f.write("""Clear this file and write accounts in this format
email:pass:answer:answer:answer

or

email:pass

you can separate those accounts by a new line if you would like to use multiple accounts.""")

    if os.path.isfile(os.path.join(config['sniper']['init_path'], "config.ini")):
        if log.yes_or_no('yes/no | overwrite current config file'):
            with open(os.path.join(config['sniper']['init_path'], "config.ini"), "w") as f:
                user_config = configparser.ConfigParser(allow_no_value=True)
                user_config['sniper'] = {
                    'timing_system': 'namemc',
                    'auto_claim_namemc': 'no',
                    'snipe_requests': '3',
                }

                user_config['accounts'] = {
                    'max_accounts': '30',
                    'authentication_delay': '500',
                    'start_authentication': '720'
                }

                user_config['skin'] = {
                    'change_skin_on_snipe': 'no',
                    'skin_change_type': 'url',
                    'skin': ''
                }

                user_config.set('skin', '; skin_change_type can be url, path, or username. refer to docs for more info.')

                user_config.write(f)

    log.info("successfully initialized sniper")
