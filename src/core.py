#!/usr/bin/python3
# coding : utf-8

import initDB

from src.views import menu
from src.views import menu_models as mm

from src.models import db
from src.models import config as cfg

from src.controllers import controller
from src.controllers import product


# global debug in main ?


class App():
    def __init__(self, debug=False):
        self.debug = debug
        self.running = False
        self.first = False
        # Const
        self.sql = cfg.sql.copy()
        self.result = []
        self.resultFormatted = []
        self.cat_id = None
        self.prod = None
        self.prodS = None
        # Step
        self.step = cfg.stepApp.copy()
        self.cwp = self.step
        self.cws = None
        self.oldPath = None
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

    def displayChoiceList(self, view, ctrl, args):
        self.view = view(args[0], **args[1])
        self.ctrl = ctrl(self.view, self.cursor)
        rep = self.ctrl.choiceMenu(args[0], self.debug)
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

    def quit(self):
        self.running = False
        print("Bye")

    def run(self):
        print('running')
        self.running = True
        rep = 0
        oldRep = rep
        previous = False
        while self.running:
            resultFormatted = []
            if previous:
                previous = False
                rep = oldRep
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
            if self.debug:
                print(param)
            view, ctrl = param[0], param[1]
            args = param[2]
            if len(param) == 4:
                paramExt = param[3]
            else:
                paramExt = dict()

            # query
            if 'query' in paramExt.keys():
                if self.result:
                    self.item = self.result[rep]
                    if '4query' in paramExt.keys():
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

            #   display choice list
            if view and ctrl and args:
                rep = self.displayChoiceList(view, ctrl, args)
            else:
                rep = None

            # previous and exit
            if rep == 77 or rep == 99:
                if rep == 77:
                    previous = True
                else:
                    exitRequested = True
            else:
                pass
            # changing view
            if exitRequested:
                self.quit()

            if self.cwpIsChoosePath:
                if previous and self.oldPath:
                    self.cws = self.oldPath
                elif not previous:
                    selectedKey = list(self.cwp.keys())[rep]
                    self.oldPath = self.cwp
                    self.cwp = self.cwp[selectedKey]
            else:
                keys = list(self.cwp.keys())
                if self.cws in keys:
                    indexKey = keys.index(self.cws)
                    if indexKey > 0 and previous:
                        previousKey = keys[indexKey-1]
                        self.cws = previousKey
                        oldRep = rep
                    elif indexKey < len(keys)-1 and not previous:
                        nextKey = keys[indexKey+1]
                        self.cws = nextKey
                        if nextKey == 'prodUpdate':
                            self.prodS = self.result[rep]
                            self.updateProd()
                        elif nextKey == 'end':
                            self.cwp = self.step.copy()
                            self.cws = None
                        elif nextKey == 'subsChoice':
                            self.product = self.result[rep]
