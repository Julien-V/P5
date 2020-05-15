#!/usr/bin/python3
# coding : utf-8

import os
import shutil


class MenuItem():
    """This class is the parent class of menu_component class"""
    def __init__(self, indent=1):
        """This method initializes the class
        :param indent: set by default to 1
        """
        self.geometry = shutil.get_terminal_size()
        self.col = self.geometry.columns
        self.rows = self.geometry.lines
        if not indent:
            self.indent = 1
        else:
            self.indent = indent
        self.result = []
        self.colors = {
            'yellow': '\033[93m',
            'blue': '\033[96m',
            'red': '\033[91m',
            'purple': '\033[95m',
            'green': '\033[92m',
            'bold': '\033[1m',
            'endc': '\033[0m',
        }
        if os.name != "posix":
            for key in self.colors.keys():
                self.colors[key] = ''
        pass

    def get(self):
        for line in self.result:
            yield line.center(int(self.col/self.indent))
        pass
