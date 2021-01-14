from os.path import abspath, dirname


class Config:
    def __init__(self):
        directory = dirname(dirname(dirname(dirname(abspath(__file__)))))

        with open(directory + "/data/config.txt", "r") as f:
            config = {}

            for line in f.readlines():
                if line.startswith("#"):
                    continue
                line = line.rstrip()
                line = line.split(':')

                key = line[0]
                value = line[1]

                config[key] = value


def get(value):
    return config[value]
