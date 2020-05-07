#!/usr/bin/python3
# coding : utf-8

from src.views import menu_component as menuC


class ChoiceList():
    # text and title in kwargs ?
    def __init__(self, values, **kwargs):
        self.values = values
        if kwargs.keys():
            self.kwargs = kwargs
        else:
            self.kwargs = False
        self.text = ''
        self.result = []
        self.dispOrder = [
            menuC.Title,
            menuC.PrintList,
            menuC.PrintLine,
        ]
        self.gen()

    def process_kwargs(self):
        keys = self.kwargs.keys()
        if 'lines' in keys:
            for line in self.kwargs['lines']:
                printLineObject = menuC.PrintLine(line)
                self.queue.append(printLineObject)
        if 'title' in keys:
            title = self.kwargs['title']
            titleObject = menuC.Title(title)
            self.queue.append(titleObject)
        if 'text' in keys:
            self.text = self.kwargs['text']

    def gen(self):
        self.queue = []
        printListObject = menuC.PrintList(self.values)
        self.queue.append(printListObject)
        if self.kwargs:
            self.process_kwargs()
        temp = []
        for obj in self.dispOrder:
            for elem in self.queue:
                if isinstance(elem, obj):
                    temp.append(elem)
        self.queue = temp
        # Input:
        self.promptObject = menuC.Prompt(self.text)

    def get(self):
        for elem in self.queue:
            for line in elem.get():
                print(line)
        return self.promptObject.get()
