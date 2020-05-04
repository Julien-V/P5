#!/usr/bin/python3
# coding : utf-8

import json
import requests

from src.models import config as cfg

from src.controllers import product, category


class Populate():
    def __init__(self, param, db, cat_id):
        self.name = param["tag_0"]
        self.param = param
        self.db = db
        self.catId = cat_id
        self.url = cfg.url
        self.headers = cfg.headers
        self.count = 0
        self.resultList = []

    def createURL(self):
        for key in self.param:
            self.url += f"{key}={self.param[key]}"
            self.url += "&"
        self.url = self.url[:-1]

    def getAndLoad(self):
        r = requests.get(self.url, headers=self.headers)
        result = json.loads(r.text)
        return result

    def keepOnlyProductsWithNutritionGrades(self):
        prodList = self.resultList
        temp = [x for x in prodList if "nutrition_grades" in x.keys()]
        self.resultList = temp

    def insert(self):
        if not self.resultList:
            print("resultList empty")
            return
        catObj = category.Category(self.name, self.db)
        catObj.insert()
        print("lastrowid ", self.catId)
        for prod in self.resultList:
            prodObj = product.Product(self.db, self.catId)
            prodObj.get_validate_insert(prod)

    def run(self):
        self.createURL()
        result = self.getAndLoad()
        if "count" in result.keys():
            self.count = int(result["count"])
            if "products" in result.keys():
                self.resultList += result["products"]
                while self.count < len(self.resultList):
                    self.param["page"] = int(self.param["page"])+1
                    self.createURL()
                    result = self.getAndLoad()
                    if "products" in result.keys():
                        self.resultList += result["products"]
                    else:
                        break
        print(len(self.resultList))
        self.keepOnlyProductsWithNutritionGrades()
        print(len(self.resultList))
        self.insert()
        return


if __name__ == "__main__":
    pass
