#!/usr/bin/python3
# coding : utf-8

from src import core


def main(debug=False):
    app = core.App(debug)
    app.run()


if __name__ == "__main__":
    main(True)
