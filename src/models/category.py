#!/usr/bin/python3
# coding : utf-8


class Category():
    def __init__(self, name, cat_id):
        self.name = name
        self.cat_id = cat_id
        self.prodList = []

    def addProduct(self, product):
        self.prodList.append(product)
