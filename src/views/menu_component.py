#!/usr/bin/python3
# coding : utf-8


from . import menu


class Title(menu.MenuItem):
    def __init__(self, text, indent=1):
        super().__init__(indent)
        self.text = text
        self.gen()

    def gen(self):
        B = self.colors["bold"]
        end = self.colors["endc"]
        self.result = [
            f"\n",
            f"{B}{self.text}{end}",
            f"\n"
            ]

    def get(self):
        for line in self.result:
            yield line.center(int(self.col/self.indent))


class Prompt(menu.MenuItem):
    def __init__(self, text=""):
        super().__init__()
        self.text = text
        self.line = ""
        self.gen()

    def gen(self):
        g = self.colors["green"]
        B = self.colors["bold"]
        end = self.colors["endc"]
        self.line = (
            f"{B}[{g}+{end}{B}] "
            f"{self.text} >>> {end}")

    def get(self):
        return input(self.line)


class PrintList(menu.MenuItem):
    def __init__(self, values, num=True, indent=3):
        super().__init__(indent)
        self.values = values
        self.num = num
        self.gen()

    def gen(self):
        b = self.colors["blue"]
        B = self.colors["bold"]
        end = self.colors["endc"]
        self.result.append("\n\n")
        for id_item, item in enumerate(self.values):
            if self.num:
                line = (
                    f"{B}[{b}{id_item}{end}{B}]{end} "
                    f"{item}")
                self.result.append(line)
            else:
                line = (
                    f"{B}[{b}*{end}{B}]{end} "
                    f"{item}")
                self.result.append(line)
        # center is sensible to the length of a str
        lineSize = max([len(x) for x in self.result])
        temp = []
        for line in self.result:
            if len(line) < lineSize:
                line += " "*(lineSize-len(line))
            temp.append(line)
        self.result = temp
        self.result.append("\n\n")

    def get(self):
        for line in self.result:
            yield line.center(int(self.col/self.indent))


class PrintLine(menu.MenuItem):
    def __init__(self, text, indent=1000):
        super().__init__(indent)
        self.text = text
        self.gen()

    def gen(self):
        b = self.colors["blue"]
        B = self.colors["bold"]
        end = self.colors["endc"]
        line = (
            f"{B}{b}[*] {end}{B}"
            f"{self.text}{end}"
            )
        self.result.append(line)

    def get(self):
        for line in self.result:
            yield line.center(int(self.col/self.indent))
