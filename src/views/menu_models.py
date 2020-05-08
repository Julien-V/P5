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


class PrintLineDB():
    def __init__(self, val, **kwargs):
        # values must be a dict
        self.val = val
        if kwargs.keys():
            self.kwargs = kwargs
        else:
            self.kwargs = False
        self.text = ''
        self.prod, self.substitute = dict(), dict()
        self.dispOrder = [
            menuC.Title,
            menuC.PrintLine
        ]
        # Get terminal size
        init_geom = menuC.PrintLine(' ')
        self.col = init_geom.col
        self.colors = init_geom.colors
        self.gen()

    def process_kwargs(self):
        pass

    def comp(self):
        b = self.colors['blue']
        B = self.colors['bold']
        end = self.colors['endc']
        for key in self.prod.keys():
            sizeKey = len(key)+6  # something like ' [ key ] '
            val = str(self.prod[key])
            prodSize = len(val)
            maxSize = int((self.col/2)-(sizeKey/2)-3)
            if key in self.substitute:
                valS = str(self.substitute[key])
                subsSize = len(valS)
            else:
                valS = list()
                subsSize = 0
            pLines = [val[i:i+maxSize] for i in range(0, prodSize, maxSize)]
            sLines = [valS[i:i+maxSize] for i in range(0, subsSize, maxSize)]
            (pl, sl) = (len(pLines), len(sLines))
            # key on top
            side = " "*maxSize
            txt = f"{end}{side} {b}{B}[ {key} ]{end} {side}"
            lineObj = menuC.PrintLine(txt)
            self.queue.append(lineObj)
            maxSize = int((self.col/2)-(len('   ||   ')/2)-3)
            if pl > sl:
                for i in range(0, pl-sl):
                    sLines.append("")
            elif pl < sl:
                for i in range(0, sl-pl):
                    pLines.append("")
            for i, elem in enumerate(pLines):
                left = (maxSize-len(elem))*" "
                s = sLines[i]
                right = " "*(maxSize-len(s))
                txt = (
                    f"{end}{left}{elem}   "
                    f"{B}{'||'}{end}   {s}{right}")
                lineObj = menuC.PrintLine(txt)
                self.queue.append(lineObj)
            sep = menuC.PrintLine("-"*(self.col-4))
            self.queue.append(sep)

    def gen(self):
        self.queue = []
        if self.kwargs:
            self.process_kwargs()
        # items
        for item in self.val.items():
            (key, val) = item
            if key[-1] == 'S':
                self.substitute[key[:-1]] = val
            else:
                self.prod[key] = val
        if self.substitute:
            self.comp()
        else:
            for item in self.prod.items():
                self.queue.append(menuC.PrintLine(item))

    def get(self):
        # sorting
        temp = list()
        for obj in self.dispOrder:
            for elem in self.queue:
                if isinstance(elem, obj):
                    temp.append(elem)
        self.queue = temp
        # display
        for elem in self.queue:
            for line in elem.get():
                print(line)
        return input('') or "0"
