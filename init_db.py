#!/usr/bin/python3
# coding : utf-8

import json
import requests

from src.models import config as cfg

from src.controllers import product, category


class Populate():
    """This class gets all the products in a category
    and insert them in database
    """
    def __init__(self, param, db, cat_id):
        """This method initializes the class
        :param param: url arguments for the request
        :param db: database object
        :param cat_id: categorie id in table Categories
        """
        self.name = param["tag_0"]
        self.param = param
        self.db = db
        self.cat_id = cat_id
        self.url = cfg.url
        self.headers = cfg.headers
        self.count = 0
        self.result_list = []

    def create_url(self):
        """This method adds self.param keys and values to self.param"""
        for key in self.param:
            self.url += f"{key}={self.param[key]}"
            self.url += "&"
        self.url = self.url[:-1]

    def get_and_load(self):
        """This method does the request and decode returned JSON
        :return: JSON decoded by json.loads()"""
        requesting = True
        while requesting:
            try:
                r = requests.get(self.url, headers=self.headers)
                requesting = False
            except requests.exceptions.Timeout:
                print("[!] Timeout.")
            except requests.exceptions.RequestException as e:
                print(f"[!] Error : {e}")
        result = json.loads(r.text)
        return result

    def keep_nutri_g_only(self):
        """This method keeps only products with nutrition grades"""
        prod_list = self.result_list
        temp = [x for x in prod_list if "nutrition_grades" in x.keys()]
        self.result_list = temp

    def insert(self):
        """This method inserts current category and its products in database"""
        if not self.result_list:
            print("resultList empty")
            return
        cat_obj = category.Category(self.name, self.db)
        cat_obj.insert()
        print("lastrowid ", self.cat_id)
        for prod in self.result_list:
            prod_obj = product.Product(self.db, self.cat_id)
            prod_obj.get_validate_insert(prod)

    def run(self):
        self.create_url()
        result = self.get_and_load()
        if "count" in result.keys():
            self.count = int(result["count"])
            if "products" in result.keys():
                self.result_list += result["products"]
                while self.count < len(self.result_list):
                    self.param["page"] = int(self.param["page"])+1
                    self.create_url()
                    result = self.get_and_load()
                    if "products" in result.keys():
                        self.result_list += result["products"]
                    else:
                        break
        print(len(self.result_list))
        self.keep_nutri_g_only()
        print(len(self.result_list))
        self.insert()
        return


if __name__ == "__main__":
    pass
