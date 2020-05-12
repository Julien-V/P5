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
            rep = self.view.get()
            choiceList = self.view.resizedResult.copy()
            # get rid of \n
            choiceList.remove(choiceList[0])
            choiceList.remove(choiceList[-1])
            if rep == '777' or rep == '999':
                valid = True
            else:
                try:
                    choiceList[int(rep)]
                    valid = True
                except Exception as e:
                    print(e)
                    valid = False
        return int(rep)

    def printLineDB(self, val, debug=False):
        valid = False
        while not valid:
            if not debug:
                self._clear()
            rep = self.view.get()
            if rep == '777' or rep == '999':
                valid = True
            else:
                try:
                    r = int(rep)
                    if r == 888:
                        self.view.nextSubs()
                    else:
                        valid = True
                except Exception as e:
                    print(e)
                    valid = False
        return int(rep)
