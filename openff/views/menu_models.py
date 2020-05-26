#!/usr/bin/python3
# coding : utf-8

from openff.views import menu_component as menu_c


class ChoiceList:
    """This class gathers multiples components from openff.views.menu_component
    in order to create and display a view.
    This view display a list and an input to get user's anwser.
    Title, some lines before the input and input customization are optionals
    >>> cl = menu_models.ChoiceList(values)
    >>> cl.get()
    """
    def __init__(self, values, **kwargs):
        """This method initializes the class and call self.gen()
        :param values: list of values to display
        :param kwargs: optional dict for optional display
        """
        self.values = values
        if kwargs.keys():
            self.kwargs = kwargs
        else:
            self.kwargs = False
        self.text = ''
        self.resized_result = None
        self.disp_order = [
            menu_c.Title,
            menu_c.PrintList,
            menu_c.PrintLine,
        ]
        self.gen()

    def process_kwargs(self):
        """This method processes optionals parameters in self.kwargs"""
        keys = self.kwargs.keys()
        if 'lines' in keys:
            for line in self.kwargs['lines']:
                print_line_obj = menu_c.PrintLine(line)
                self.queue.append(print_line_obj)
        if 'title' in keys:
            title = self.kwargs['title']
            title_obj = menu_c.Title(title)
            self.queue.append(title_obj)
        if 'text' in keys:
            self.text = self.kwargs['text']

    def gen(self):
        """This method creates the menu components needed and
        add them to queue (list)
        """
        self.queue = []
        print_list_obj = menu_c.PrintList(self.values)
        self.resized_result = print_list_obj.result
        self.queue.append(print_list_obj)
        if self.kwargs:
            self.process_kwargs()
        temp = []
        for obj in self.disp_order:
            for elem in self.queue:
                if isinstance(elem, obj):
                    temp.append(elem)
        self.queue = temp
        # Input:
        self.prompt_obj = menu_c.Prompt(self.text)

    def get(self):
        """This method prints the result of get() method in each
        menu_components added to queue
        :return: the method get() of a
        openff.views.menu_component.Prompt object
        """
        for elem in self.queue:
            for line in elem.get():
                print(line)
        return self.prompt_obj.get()


class PrintLineDB:
    """This class gathers multiples components from openff.views.menu_component
    in order to create and display a view.
    This view display a product details (dict)
    Title, some lines before the input and input customization are optionals
    >>> pl = menu_models.PrintLineDB(values)
    >>> pl.get()
    """
    def __init__(self, val, **kwargs):
        """This method initializes the class and call self.gen()
        :param val: a product (dict)
        :param kwargs: optional dict for optional display
        """
        self.val = val
        if kwargs.keys():
            self.kwargs = kwargs
        else:
            self.kwargs = False
        self.text = ''
        self.prod, self.substitute = dict(), dict()
        self.disp_order = [
            menu_c.Title,
            menu_c.PrintLine
        ]
        # Get terminal size
        init_geom = menu_c.PrintLine(' ')
        self.col = init_geom.col
        self.colors = init_geom.colors
        self.gen()

    def process_kwargs(self):
        """This method processes optionals parameters in self.kwargs"""
        keys = self.kwargs.keys()
        if 'text' in keys:
            self.text = self.kwargs['text']

    def comp(self):
        """This method adds to queue the details of a product and
        his substitute
        """
        b = self.colors['blue']
        B = self.colors['bold']
        end = self.colors['endc']
        for key in self.prod.keys():
            size_key = len(key)+6  # something like ' [ key ] '
            val = str(self.prod[key])
            prod_size = len(val)
            max_size = int((self.col/2)-(size_key/2)-3)
            if key in self.substitute:
                val_s = str(self.substitute[key])
                subs_size = len(val_s)
            else:
                val_s = list()
                subs_size = 0
            range_p_lines = range(0, prod_size, max_size)
            range_s_lines = range(0, subs_size, max_size)
            p_lines = [val[i:i+max_size] for i in range_p_lines]
            s_lines = [val_s[i:i+max_size] for i in range_s_lines]
            (pl, sl) = (len(p_lines), len(s_lines))
            # key on top
            side = " "*max_size
            txt = f"{end}{side} {b}{B}[ {key} ]{end} {side}"
            line_obj = menu_c.PrintLine(txt)
            self.queue.append(line_obj)
            max_size = int((self.col/2)-(len('   ||   ')/2)-3)
            if pl > sl:
                for i in range(0, pl-sl):
                    s_lines.append("")
            elif pl < sl:
                for i in range(0, sl-pl):
                    p_lines.append("")
            for i, elem in enumerate(p_lines):
                left = (max_size-len(elem))*" "
                s = s_lines[i]
                right = " "*(max_size-len(s))
                txt = (
                    f"{end}{left}{elem}   "
                    f"{B}{'||'}{end}   {s}{right}")
                line_obj = menu_c.PrintLine(txt)
                self.queue.append(line_obj)
            sep = menu_c.PrintLine("-"*(self.col-4))
            self.queue.append(sep)

    def gen(self):
        """This method creates the menu components needed and
        add them to queue (list)
        """
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
                # modify display
                (key, val) = item
                g = self.colors['green']
                end = self.colors['endc']
                txt = f"{end}{g}{key} :{end} {val}{end}"
                self.queue.append(menu_c.PrintLine(txt))
        # Input:
        self.prompt_obj = menu_c.Prompt(self.text)

    def get(self):
        """This method prints the result of get() method in each
        menu_components added to queue
        :return: the result of an input
        """
        # sorting
        temp = list()
        for obj in self.disp_order:
            for elem in self.queue:
                if isinstance(elem, obj):
                    temp.append(elem)
        self.queue = temp
        # display
        for elem in self.queue:
            for line in elem.get():
                print(line)
        return self.prompt_obj.get() or "0"
