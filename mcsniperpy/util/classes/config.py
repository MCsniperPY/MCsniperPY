import os
from os.path import dirname

import toml

from ..logs_manager import Logger as log


class BackConfig:
    """"""

    def __init__(self):
        with open(os.path.join(dirname(dirname(dirname(__file__))), "data", "config.toml"), "r") as f:
            data = toml.loads(f.read())

            self.init_path = data["sniper"].get("init_path", "")

            if self.init_path == "":
                log.error("Failed to find MCsniperPY directory")
                log.info("To fix this open your sniping folder (or make one) and type `mcsniperpy init` in it.")
                log.info("Next, just re-run the sniper with the command you used to get here.")

    def load_init_path(self, cwd):
        self.init_path = cwd


class Config:

    def __init__(self, dir):
        pass
