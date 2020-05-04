#!/usr/bin/python3
# coding : utf-8

from src import core


def main():
    app = core.App(debug=False)
    while app.running:
        app.run()
        app = core.App(debug=False)


if __name__ == "__main__":
    main()
