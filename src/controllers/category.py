#!/usr/bin/python3
# coding : utf-8

from src.models import config as cfg


class Category():
    def __init__(self, name, model):
        self.name = name
        self.cursor = model
        self.prodList = []

    def addProduct(self, product):
        self.prodList.append(product)

    def _validate(self):
        if not isinstance(self.name, str):
            print(f"{self.name} not str")
            return False
        else:
            return True

    def insert(self):
        valid = self._validate()
        if not valid:
            return
        sql = cfg.db['insert_cat'].copy()
        sql[1] = sql[1].format(self.name)
        for query in sql:
            try:
                self.cursor.execute(query)
            except Exception as e:
                print(e)
                return
            # self.db.executeQuery(query)
