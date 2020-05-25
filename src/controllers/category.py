#!/usr/bin/python3
# coding : utf-8

from src.models import config as cfg


class Category():
    """This class represents a category,
    control and insert it into database
    """
    def __init__(self, name, model):
        """This method initializes the class
        :param name: category name
        :param model: cursor linked to database
        """
        self.name = name
        self.cursor = model
        self.prod_list = []

    def add_product(self, product):
        """This method adds a product in self.prod_list"""
        self.prod_list.append(product)

    def _validate(self):
        """This method checks category's type
        :return: boolean
        """
        if not isinstance(self.name, str):
            print(f"{self.name} not str")
            return False
        else:
            return True

    def insert(self):
        """This method inserts this category into database"""
        valid = self._validate()
        if not valid:
            return
        sql = cfg.sql['insert_cat']
        sql_args = (self.name,)
        try:
            self.cursor.execute(sql, sql_args)
        except Exception as e:
            print(e)
            return
