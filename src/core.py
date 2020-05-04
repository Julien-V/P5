#!/usr/bin/python3
# coding : utf-8

import initDB

from src.views import menu
from src.views import menu_models as mm

from src.models import db
from src.models import config as cfg

from src.controllers import controller
from src.controllers import product

# App() need some serious rework


class App():
    def __init__(self, debug=False):
        self.locale = cfg.locale
        self.debug = debug
        self.running = True
        self.db = db.DB()
        self.cursor = self.db.getCursor()
        sql = cfg.db['test']
        # trying to get Categories
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # if Categories empty:
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

    def substituateMenu(self):
        args = cfg.menu["catChoice"]
        catChoice = mm.ChoiceList(args[0], args[1], args[2])
        ctrl = controller.Controller(catChoice, self.cursor)
        rep = ctrl.choiceMenu(args[0], self.debug)
        self.displayByCat(rep)

    def displayMenu(self):
        args = cfg.menu["display"]
        dispChoice = mm.ChoiceList(args[0], args[1], args[2])
        ctrl = controller.Controller(dispChoice, self.cursor)
        rep = ctrl.choiceMenu(args[0], self.debug)
        if rep == 0:
            args = cfg.menu["displayByCat"]
            dispCatChoice = mm.ChoiceList(args[0], args[1], args[2])
            ctrl = controller.Controller(dispCatChoice, self.cursor)
            rep = ctrl.choiceMenu(args[0], self.debug)
            self.displaySByCat(rep)
        else:
            self.displaySAll()

    def displayByCat(self, cat):
        # category_id start at 1 not 0
        sql = cfg.db['displayByCat'].format(cat+1)
        self.cursor = self.db.getCursor(True)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # choose product
        self.displayByProduct(result)

    def displayByProduct(self, result):
        listProd = []
        # len max will be terminal.row
        if len(result) > 20:
            result = result[:19]
        for prod in result:
            text = f"{prod['id']} // {prod['product_name']}"
            text += f" // {prod['nutrition_grades']}"
            listProd.append(text)
        title = "Choix du produit"
        dispProdChoice = mm.ChoiceList(listProd, "Produit", title)
        ctrl = controller.Controller(dispProdChoice, self.cursor)
        rep = ctrl.choiceMenu(listProd, self.debug)
        self.substituate(result[rep])

    def substituate(self, product):
        # category_id needed at this time
        cat_id = product['category_id']
        sql = cfg.db['subst'].format(cat_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        betterProducts = []
        score = product['nutrition_grades']
        for prod in result:
            # "a" < "b" = True
            if prod['nutrition_grades'] < score:
                betterProducts.append(prod)
        self.displaySedProd(product, betterProducts)

    def displaySedProd(self, oldProd, result):
        oldText = (
            "Old : "
            f"{oldProd['product_name']} // "
            f"{oldProd['nutrition_grades']}")
        kw = {
            'lines': [oldText]
        }
        listProd = []
        if len(result) > 20:
            result = result[:19]
        for prod in result:
            text = f"{prod['product_name']}"
            text += f" // {prod['nutrition_grades']}"
            listProd.append(text)
        title = "Choix du produit à substituer"
        text = "Substitution"
        dispProdChoice = mm.ChoiceList(listProd, text, title, **kw)
        ctrl = controller.Controller(dispProdChoice, self.cursor)
        rep = ctrl.choiceMenu(listProd, self.debug)
        self.updateSub(oldProd, result[rep])

    def updateSub(self, prod, subs):
        prodObj = product.Product(self.cursor, prod['category_id'])
        update = {'substitute_id': subs['id']}
        prodObj.get_validate_insert(prod, update)
        self.run()

    # 1 : Display all
    def displaySByCat(self, cat):
        sql = cfg.db['displaySByCat'].format(cat+1)
        print(sql)
        self.cursor.execute(sql)
        print(self.cursor.fetchall())
        # one day something will be written here ...

    def displaySAll(self):
        sql = cfg.db['displaySAll']
        self.cursor = self.db.getCursor(True)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print result
        self.displaySubstituate(result)

    # better graphics tomorrow, to tired atm
    def displaySubstituate(self, result):
        show = []
        for line in result:
            prod = line
            s_id = prod['substitute_id']
            sql = cfg.db['prod'].format(s_id)
            self.cursor.execute(sql)
            prodSubs = self.cursor.fetchall()[0]
            text = f"{prod['product_name']}"
            text += f" // {prod['nutrition_grades']}"
            text += f" --> {prodSubs['product_name']}"
            text += f" // {prodSubs['nutrition_grades']}"
            show.append(text)
        dispProd = mm.ChoiceList(show)
        ctrl = controller.Controller(dispProd, self.cursor)
        rep = ctrl.choiceMenu(show, self.debug)
        # self.details(rep)
        self.run()

    def run(self):
        # print menu1
        args = cfg.menu['start'].copy()
        if self.first:
            # self.errorQueue
            self.first = False
            kw = {
                'lines': ['Base de donnée crée et chargée']
            }
            args.append(kw)
            start = mm.ChoiceList(args[0], args[1], args[2], **args[3])
        else:
            # can't remember if we need else for this
            start = mm.ChoiceList(args[0], args[1], args[2])
        ctrl = controller.Controller(start, self.cursor)
        rep = ctrl.choiceMenu(args[0], False)
        # condition
        if rep == 0:
            self.substituateMenu()
        else:
            self.displayMenu()
