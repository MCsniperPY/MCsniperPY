import os

default_config = """\
timing_system:api
skin:https://namemc.com/skin/4e45a59795a252c3
skin_model:slim
change_skin:false
snipe_reqs:8
block_reqs:3
auth_delay:800
max_accs:30
auto_link_namemc:false NOT IMPLEMENTED
"""

class Config:
    def __init__(self):
        if not os.path.exists("config.txt"):
            with open("config.txt", "w") as f:
                f.write(default_config)
        with open("config.txt", "r") as f:
            self.lines = [line.strip() for line in f.readlines()]
            self.timing = self.find_parameter("timing_system")
            self.skin_model = self.find_parameter("skin_model")
            
            self.block_reqs = int(self.find_parameter("block_reqs"))
            self.snipe_reqs = int(self.find_parameter("snipe_reqs"))
            self.max_accs = int(self.find_parameter("max_accs"))
            self.auth_delay = int(self.find_parameter("auth_delay"))

            self.change_skin = self.find_bool("change_skin", False)
            self.webhooks = self.find_all("wh")

            self.skin = self.find_parameter("skin")
            if "namemc.com/skin" in self.skin:
                self.skin = f"https://namemc.com/texture/{self.skin.split('/')[-1]}.png"
            
            self.custom_announce = self.find_parameter("custom_announce")
            if self.custom_announce is None:
                del self.custom_announce

    def find_parameter(self, parameter):
        for line in self.lines:
            line = line.split(":")
            if line[0].lower() == parameter:
                return line[1]

    def find_bool(self, parameter, default):
        parameter = self.find_parameter(parameter)
        if parameter == "true":
            return True
        elif parameter == "false":
            return False
        else:
            return default

    def find_all(self, parameter):
        options = []
        for line in self.lines:
            line = line.split(":")
            if line[0] == parameter:
                options.append(line[1])
        return options