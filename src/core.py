#!/usr/bin/python3
# coding : utf-8


import init_db

from src.models import db
from src.models import config as cfg

from src.controllers import product


class App:
    """Main Class : controllers, views and models used by this class
    >>> app = core.App()
    >>> app.run()
    or with debug information :
    >>> app = core.App(True)
    >>> app.run()
    """
    def __init__(self, debug=False):
        """Class initialization and database loading
            :param debug: debug
        """
        self.debug = debug
        self.running = False
        self.first = False
        # Const
        self.sql = cfg.sql.copy()
        self.result = []
        self.item = dict()
        self.cat_id = None
        self.prod = None
        self.prod_s = None
        # Step
        self.step = cfg.step_app.copy()
        self.cwp = self.step
        self.cws = None
        self.old_path = list()
        # DB
        # while not self.db ?
        self.load_db()

    def load_db(self):
        """Load db.DB() class and execute a query to test
        the presence of rows in database
        (if not, core.App.first_run() is called)
        """
        self.db = db.DB()
        self.cursor = self.db.get_cursor()
        # select * from Categories;
        query = self.sql['test']
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # if Categories return empty set:
        if not result:
            self.first = True
            self.first_run()
        else:
            self.first = False

    def first_run(self):
        """Create a Populate object for each category
            in src.models.config.cat to get products and insert them in db
        """
        for cat_id, category in enumerate(cfg.cat):
            param = cfg.param.copy()
            param['tag_0'] = category
            pop = init_db.Populate(param, self.cursor, cat_id+1)
            pop.run()

    def display_view(self, view, ctrl, args, r):
        """This method chooses which view is given by the current step
        then create this view with appropriate controller
        :param view: a view (src.views.menu_models)
        :param ctrl: a controller (src.controllers.controller)
        :param args: args for the view
        :param r: previous user's anwser
        """
        if view == cfg.choice:
            self.view = view(args[0], **args[1])
            self.ctrl = ctrl(self.view, self.cursor)
            rep = self.ctrl.choice_menu(self.debug)
        elif view == cfg.print_line and self.result:
            if r >= len(self.result):
                val = self.result[0]
            else:
                val = self.result[r]
            self.view = view(val, **args[1])
            self.ctrl = ctrl(self.view, self.cursor)
            rep = self.ctrl.print_line_db(self.debug)
            if not self.view.substitute and rep not in [777, 999]:
                rep = r
        else:
            rep = 777
        return rep

    def format_display(self, formatting_rules):
        """format result following the list of formatting rules
        of the current step (lamda function)
        :param formatting_rules: list of lambda functions
        :return formatted: result (list) formatted
        >>> app.result
        ["test"]
        >>> fRules = [
            (lambda i: "[*]" + i,
            (lambda i: i + ".")
            ]
        >>> app.format_display(fRules)
        "[*] test."
        """
        formatted = []
        for elem in self.result:
            r = elem
            for rule in formatting_rules:
                r = rule(r)
            formatted.append(r)
        return formatted

    def query(self, query, rep=None):
        """This method executes a query on the loaded database
        :param query:  SQL string
        :param rep: anwser of the previous step, set by default to None
        :return: result of the query
        """
        if isinstance(rep, int) and "%s" in query:
            q = query
            q_args = (rep+1,)
            self.cursor.execute(q, q_args)
        else:
            q = query
            self.cursor.execute(q)
        return self.cursor.fetchall()

    def process_result(self, process_rules):
        """This method processes the result of the query following the list
        of proccessing rules of the current step
        :param process_rules: list of lambda functions
        :return: return processed data
        """
        p = self
        for rule in process_rules:
            p = rule(p)
        return p

    def update_prod(self):
        """This methode updates a product by adding a substitute_id"""
        if self.product and self.prod_s:
            subs = self.prod_s
            prod = self.product
            prod_obj = product.Product(self.cursor, prod['category_id'])
            update = {'substitute_id': subs['id']}
            prod_obj.get_validate_insert(prod, update)
        else:
            if self.debug:
                print(f'prod/prod_s not loaded : {self.prod}//{self.prod_s}')

    def run(self):
        """This method handles steps organization by :
        doing the actions required by the current step
        displaying the result
        analysing user anwser
        and changing the current step for the next/previous one
        """
        print('core.App running')
        self.running = True
        rep = 0
        old_rep = list()
        previous = False
        while self.running:
            result_formatted = []
            if previous:
                previous = False
                if old_rep:
                    rep = old_rep.pop()
                else:
                    rep = 0
            exit_requested = False

            # param = [view, controller, [list, kwargs]]
            if 'param' not in self.cwp.keys():
                self.cwp_is_intersection = False
                if self.cws is None:
                    key = list(self.cwp.keys())[0]
                    self.cws = key
                param = self.cwp[self.cws].copy()
            else:
                self.cwp_is_intersection = True
                self.cws = None
                param = self.cwp['param'].copy()

            # loading params
            view, ctrl = param[0], param[1]
            if param[2]:
                args = param[2].copy()
            if len(param) == 4:
                param_ext = param[3]
            else:
                param_ext = dict()

            if self.debug:
                print(f"cws: {self.cws}")
                print(f"param: {param}")
                print(f"len(old_path): {len(self.old_path)}")
                print(f"old_rep: {old_rep}")
                print(f"rep: {rep}")

            # query
            if 'query' in param_ext.keys():
                if self.result:
                    self.item = self.result[rep]
                else:
                    self.item = self.item
                if '4query' in param_ext.keys():
                    print(self.item.keys())
                    for_query = param_ext['4query']
                    if for_query in self.item.keys():
                        rep = self.item[for_query]-1
                self.result = self.query(param_ext['query'], rep)
                #   process
                if 'process' in param_ext.keys():
                    self.result = self.process_result(param_ext['process'])
            #   format choice list
            if 'format' in param_ext.keys() and self.result:
                result_formatted = self.format_display(param_ext['format'])
                args[0] = result_formatted

            if self.debug:
                print(f"len(result): {len(self.result)}")
            #   display choice list
            if view and ctrl and args:
                rep = self.display_view(view, ctrl, args, rep)
            else:
                rep = None

            # previous and exit
            if rep == int(cfg.back) or rep == int(cfg.exit):
                if rep == int(cfg.back):
                    previous = True
                else:
                    exit_requested = True
            else:
                pass
            # changing view

            if self.cwp_is_intersection and not exit_requested:
                if previous and self.old_path:
                    self.cwp = self.old_path.pop()
                elif not previous:
                    selected_key = list(self.cwp.keys())[rep]
                    self.old_path.append(self.cwp)
                    self.cwp = self.cwp[selected_key]
                    old_rep.append(rep)
            elif not self.cwp_is_intersection and not exit_requested:
                keys = list(self.cwp.keys())
                if self.cws in keys:
                    index_key = keys.index(self.cws)
                    if index_key > 0 and previous:
                        previousKey = keys[index_key-1]
                        self.cws = previousKey
                    elif index_key == 0 and previous:
                        self.cwp = self.old_path.pop()
                    elif index_key < len(keys)-1 and not previous:
                        old_rep.append(rep)
                        next_key = keys[index_key+1]
                        self.cws = next_key
                        if next_key == 'prod_update':
                            self.prod_s = self.result[rep]
                            self.update_prod()
                        elif next_key == 'end':
                            self.cwp = self.step.copy()
                            self.cws = None
                            self.result = list()
                            self.old_path = list()
                            old_rep = list()
                        elif next_key == 'subs_choice':
                            self.product = self.result[rep]
            elif exit_requested:
                self.running = False
                print('Bye')
