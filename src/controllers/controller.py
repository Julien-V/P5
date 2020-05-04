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
        pass

    def _clear(self):
        os.system('clear')

    def choiceMenu(self, choiceList, debug=False):
        valid = False
        while not valid:
            if not debug:
                self._clear()
            rep = self.view.get()
            try:
                choiceList[int(rep)]
                valid = True
            except Exception as e:
                print(e)
                valid = False
        return int(rep)
