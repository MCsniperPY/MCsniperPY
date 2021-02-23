import os
from os.path import dirname

import configparser

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

    def __init__(self, dir):
        pass


def population_back_config():
    config = configparser.ConfigParser()
    config['sniper'] = {"init_path": os.getcwd()}

    with open(os.path.join(dirname(dirname(dirname(__file__))), "data", "config.ini"), "w") as f:
        config.write(f)

    with open(os.path.join(config['sniper']['init_path'], "accounts.txt"), "w") as f:
        f.write("""Clear this file and write accounts in this format
email:pass:answer:answer:answer

or

email:pass

you can separate those accounts by a new line if you would like to use multiple accounts.""")
    
    log.info("successfully initialized sniper")
