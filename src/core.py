#!/usr/bin/python3
# coding : utf-8


import initDB
from src.views import menu
from src.views import menu_models as mm

from src.models import db
from src.models import config as cfg

from src.controllers import controller, product


# global debug in main ?


class App():
    def __init__(self, debug=False):
        self.debug = debug
        self.running = False
        self.first = False
        # Const
        self.sql = cfg.sql.copy()
        self.result = []
        self.item = dict()
        self.cat_id = None
        self.prod = None
        self.prodS = None
        # Step
        self.step = cfg.stepApp.copy()
        self.cwp = self.step
        self.cws = None
        self.oldPath = list()
        # DB
        # while not self.db ?
        self.loadDB()

    def loadDB(self):
        self.db = db.DB()
        self.cursor = self.db.getCursor()
        # select * from Categories;
        query = self.sql['test']
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # if Categories return empty set:
        if not result:
            self.first = True
            self.firstRun()
        else:
            self.first = False

    def firstRun(self):
        for cat_id, category in enumerate(cfg.cat):
            param = cfg.param.copy()
            param['tag_0'] = category
            pop = initDB.Populate(param, self.cursor, cat_id+1)
            pop.run()

    def displayView(self, view, ctrl, args, r):
        if view == cfg.choice:
            self.view = view(args[0], **args[1])
            self.ctrl = ctrl(self.view, self.cursor)
            rep = self.ctrl.choiceMenu(args[0], self.debug)
        elif view == cfg.printLine and self.result:
            if r >= len(self.result):
                val = self.result[0]
            else:
                val = self.result[r]
            self.view = view(val, **args[1])
            self.ctrl = ctrl(self.view, self.cursor)
            rep = self.ctrl.printLineDB(val, self.debug)
            if not self.view.substitute and rep not in [777, 999]:
                rep = r
        else:
            rep = 777
        return rep

    def formatDisplay(self, formattingRules):
        # formattingRules must be a list of lambda
        formatted = []
        for elem in self.result:
            r = elem
            for rule in formattingRules:
                r = rule(r)
            formatted.append(r)
        return formatted

    def query(self, query, rep=None):
        if isinstance(rep, int):
            q = query.format(rep+1)
        else:
            q = query
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def processResult(self, processRules):
        p = self
        for rule in processRules:
            p = rule(p)
        return p

    def updateProd(self):
        if self.product and self.prodS:
            subs = self.prodS
            prod = self.product
            prodObj = product.Product(self.cursor, prod['category_id'])
            update = {'substitute_id': subs['id']}
            prodObj.get_validate_insert(prod, update)
        else:
            if self.debug:
                print(f'prod/prodS not loaded : {self.prod}//{self.prodS}')

    def run(self):
        print('core.App running')
        self.running = True
        rep = 0
        oldRep = list()
        previous = False
        while self.running:
            resultFormatted = []
            if previous:
                previous = False
                if oldRep:
                    rep = oldRep.pop()
                else:
                    rep = 0
            exitRequested = False

            # param = [view, controller, [list, kwargs]]
            if 'param' not in self.cwp.keys():
                self.cwpIsChoosePath = False
                if self.cws is None:
                    key = list(self.cwp.keys())[0]
                    self.cws = key
                param = self.cwp[self.cws].copy()
            else:
                self.cwpIsChoosePath = True
                self.cws = None
                param = self.cwp['param'].copy()

            # loading params
            view, ctrl = param[0], param[1]
            if param[2]:
                args = param[2].copy()
            if len(param) == 4:
                paramExt = param[3]
            else:
                paramExt = dict()

            if self.debug:
                print(f"cws: {self.cws}")
                print(f"param: {param}")
                print(f"len(oldPath): {len(self.oldPath)}")
                print(f"oldRep: {oldRep}")
                print(f"rep: {rep}")

            # query
            if 'query' in paramExt.keys():
                if self.result:
                    self.item = self.result[rep]
                else:
                    self.item = self.item
                if '4query' in paramExt.keys():
                    print(self.item.keys())
                    forQuery = paramExt['4query']
                    if forQuery in self.item.keys():
                        rep = self.item[forQuery]-1
                self.result = self.query(paramExt['query'], rep)
                #   process
                if 'process' in paramExt.keys():
                    self.result = self.processResult(paramExt['process'])
            #   format choice list
            if 'format' in paramExt.keys() and self.result:
                resultFormatted = self.formatDisplay(paramExt['format'])
                args[0] = resultFormatted

            if self.debug:
                print(f"len(result): {len(self.result)}")
            #   display choice list
            if view and ctrl and args:
                rep = self.displayView(view, ctrl, args, rep)
            else:
                rep = None

            # previous and exit
            if rep == 777 or rep == 999:
                if rep == 777:
                    previous = True
                else:
                    exitRequested = True
            else:
                pass
            # changing view

            if self.cwpIsChoosePath and not exitRequested:
                if previous and self.oldPath:
                    self.cwp = self.oldPath.pop()
                elif not previous:
                    selectedKey = list(self.cwp.keys())[rep]
                    self.oldPath.append(self.cwp)
                    self.cwp = self.cwp[selectedKey]
                    oldRep.append(rep)
            elif not self.cwpIsChoosePath and not exitRequested:
                keys = list(self.cwp.keys())
                if self.cws in keys:
                    indexKey = keys.index(self.cws)
                    if indexKey > 0 and previous:
                        previousKey = keys[indexKey-1]
                        self.cws = previousKey
                    elif indexKey == 0 and previous:
                        self.cwp = self.oldPath.pop()
                    elif indexKey < len(keys)-1 and not previous:
                        oldRep.append(rep)
                        nextKey = keys[indexKey+1]
                        self.cws = nextKey
                        if nextKey == 'prodUpdate':
                            self.prodS = self.result[rep]
                            self.updateProd()
                        elif nextKey == 'end':
                            self.cwp = self.step.copy()
                            self.cws = None
                            self.oldPath = list()
                            oldRep = list()
                        elif nextKey == 'subsChoice':
                            self.product = self.result[rep]
            elif exitRequested:
                self.running = False
                print('Bye')
