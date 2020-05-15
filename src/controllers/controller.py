#!/usr/bin/python3
# coding : utf-8

import os

from src.models import config as cfg


class Controller():
    """This class controls the validity of user's anwser"""
    def __init__(self, view, model):
        """This method initializes the class
        :param view: a view (src.views.menu_models)
        :param model: a model, database or cursor"""
        self.view = view
        self.model = model

    def _clear(self):
        """This method clears the screen"""
        os.system('clear')

    def choiceMenu(self, debug=False):
        """This method controls the choice of an element in a list
        :param debug: debug set by default to False
        :return: int of user's anwser
        """
        valid = False
        while not valid:
            if not debug:
                self._clear()
            rep = self.view.get()
            choiceList = self.view.resizedResult.copy()
            # get rid of \n
            choiceList.remove(choiceList[0])
            choiceList.remove(choiceList[-1])
            if rep == cfg.back or rep == cfg.exit:
                valid = True
            else:
                try:
                    choiceList[int(rep)]
                    valid = True
                except Exception as e:
                    print(e)
                    valid = False
        return int(rep)

    def printLineDB(self, debug=False):
        """This method controls user's anwser
        :param debug: debug set by default to False
        :return: int of user's anwser
        """
        valid = False
        while not valid:
            if not debug:
                self._clear()
            rep = self.view.get()
            if rep == cfg.back or rep == cfg.exit:
                valid = True
            else:
                try:
                    r = int(rep)
                    valid = True
                except Exception as e:
                    print(e)
                    valid = False
        return int(rep)
