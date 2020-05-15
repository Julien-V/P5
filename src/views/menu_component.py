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
        # \n self.text \n
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
        # [+] self.text >>>
        self.line = (
            f"{B}[{g}+{end}{B}] "
            f"{self.text} >>> {end}")

    def get(self):
        return input(self.line)


class PrintList(menu.MenuItem):
    """This class (a subclass of menu.MenuItem) prints a list"""
    def __init__(self, values, num=True, indent=3, limit=15):
        """This method initializes the class and call gen() method
        :param values: list to display
        :param num: numerotation beside list elem, set by default to True
        :param indent: number of indent, set by default to 3
        :param limit: max number of list element to be displayed,
        set by default to 15
        """
        super().__init__(indent)
        self.values = values
        self.num = num
        self.limit = limit
        self.pages = list()
        self.page = 0
        self.gen()

    def linesLengthCheck(self):
        """This method adds extra spaces to all element
        .center() is sensible to the length of a str
        """
        # we want a nicely displayed list
        lineSize = max([len(x) for x in self.result])
        temp = []
        for line in self.result:
            if len(line) < lineSize:
                line += " "*(lineSize-len(line))
            temp.append(line)
        self.result = temp
        self.result.append("\n\n")

    def gen(self):
        """This method formats all elements in self.values
        and add them to self.result then self.result is resized to
        match self.limit
        """
        b = self.colors["blue"]
        B = self.colors["bold"]
        end = self.colors["endc"]
        # "[] val"
        self.result.append("\n\n")
        for id_item, item in enumerate(self.values):
            if self.num:
                # [id_item] item
                line = (
                    f"{B}[{b}{id_item}{end}{B}]{end} "
                    f"{item}")
                self.result.append(line)
            else:
                # [*] item
                line = (
                    f"{B}[{b}*{end}{B}]{end} "
                    f"{item}")
                self.result.append(line)
        # list into sublists of size self.limit
        # for future implementation of pages
        lim = self.limit
        r = self.result
        # slice a list into multiple sublist (with their length matching limit)
        temp = [r[i:i+lim] for i in range(0, len(r), lim)]
        self.pages = temp
        self.result = temp[self.page]
        self.linesLengthCheck()

    def genNextPage(self):
        """This method displays the next page of the list
        .. note: method unused
        """
        if len(self.result)-1 > self.page:
            self.page += 1
        else:
            self.page = 0
        self.result = self.pages[self.page]

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
        # [*] self.text
        line = (
            f"{B}{b}[*] {end}{B}"
            f"{self.text}{end}"
            )
        self.result.append(line)

    def get(self):
        for line in self.result:
            yield line.center(int(self.col/self.indent))
