import typer
from snipe import test


def cli():
    def main(sad: bool = True):
        test()

    typer.run(main)
