#!/usr/bin/python3
# coding : utf-8


class Category():
    def __init__(self, name):
        self.name = name
        self.prodList = []

    def addProduct(self, product):
        self.prodList.append(product)
