from os.path import dirname, abspath


class Config:
    def __init__(self):
        directory = dirname(dirname(dirname(dirname(abspath(__file__)))))
        with open(directory + "/data/config.txt", "r") as f:
            global config
            config = {}

            for line in f.readlines():
                line = line.rstrip()
                line = line.split(':')

                key = line[0]
                value = line[1]

                config[key] = value

    def get(self, value):
        return config[value]
