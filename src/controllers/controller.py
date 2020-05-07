#!/usr/bin/python3
# coding : utf-8

import os

from src.views import menu
from src.views import menu_component
from src.views import menu_models

from src.models import db
from src.models import config as cfg


class Controller():
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def _clear(self):
        os.system('clear')

    def choiceMenu(self, choiceList, debug=False):
        valid = False
        while not valid:
            if not debug:
                self._clear()
            rep = int(self.view.get())
            # back not yet supported
            if rep == 99:
                valid = True
            else:
                try:
                    choiceList[rep]
                    valid = True
                except Exception as e:
                    print(e)
                    valid = False
        return rep
