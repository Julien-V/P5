#!/usr/bin/python3
# coding : utf-8

from src import core


def main(debug):
    app = core.App(debug=debug)
    app.run()


if __name__ == "__main__":
    main(False)
