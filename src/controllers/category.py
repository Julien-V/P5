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
        sql = cfg.sql['insert_cat']
        sql = sql.format(self.name)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return
            # self.db.executeQuery(query)
