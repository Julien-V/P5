#!/usr/bin/python3
# coding : utf-8

from src.views import menu_component as menuC


class ChoiceList():
    def __init__(self, values, text="", title=False, **kwargs):
        self.values = values
        self.text = text
        self.title = title
        self.result = []
        if kwargs.keys():
            self.kwargs = kwargs
        else:
            self.kwargs = False
        self.gen()

    def process_kwargs(self):
        if 'lines' in self.kwargs.keys():
            for line in self.kwargs['lines']:
                printLineObject = menuC.PrintLine(line)
                self.queue.append(printLineObject)

    def gen(self):
        self.queue = []
        if self.title:
            titleObject = menuC.Title(self.title)
            self.queue.append(titleObject)
        printListObject = menuC.PrintList(self.values)
        self.queue.append(printListObject)
        if self.kwargs:
            self.process_kwargs()
        # Input:
        self.promptObject = menuC.Prompt(self.text)

    def get(self):
        for elem in self.queue:
            for line in elem.get():
                print(line)
        return self.promptObject.get()
