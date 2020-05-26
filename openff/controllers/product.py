#!/usr/bin/python3
# coding : utf-8

from datetime import datetime

from openff.models import req_sql
import config as cfg


class Product:
    """This class represents a product,
    control and insert its caracteristics into database
    """
    def __init__(self, model, category_id):
        """This method initializes the class
        :param model: cursor object linked to database
        :param category_id:
        """
        self.cursor = model
        self.cat_id = category_id
        self.spec = dict()

    def get_validate_insert(self, prod, update=False):
        """This method checks if all NOT NULL value exit in self.spec
        :param prod: product (dict)
        :param update: set by default to False
        """
        for key in cfg.db['product_check']:
            if key in prod.keys():
                # validate and fix can go here no ?
                if key == 'code':
                    self.spec[key] = int(prod[key])
                else:
                    self.spec[key] = prod[key]
            else:
                # view.error(errormessage)
                pass
        ts = int(datetime.now().timestamp())
        self.spec['added_timestamp'] = ts
        self.spec['category_id'] = self.cat_id
        test = self._validate_product_spec()
        if test and not update:
            self._insert()
        elif test and update:
            update['substitued_id'] = prod['id']
            self._update(update)

    def _validate_product_spec(self):
        """This method validates types and length of self.spec
        :return: True if self.spec is valided else False
        """
        s = self.spec
        missing = []
        for key in cfg.db['product_check']:
            if key in s.keys():
                if isinstance(s[key], cfg.db['product_type'][key]):
                    pass
                else:
                    print(f"{key} not a {cfg.db['product_type']}")
                if key == 'nutrition_grades':
                    if len(s['nutrition_grades']) != 1:
                        return False
            else:
                missing.append(key)
        if missing:
            # print(missing)
            return False
        return True

    def _insert(self):
        """This method inserts the product into database"""
        s = self.spec
        sql = req_sql.sql['insert_prod']
        sql_args = (
            s['product_name'], s['brands'], s['code'],
            s['categories'], s['nutrition_grades'],
            s['stores'], s['url'], s['added_timestamp']
            )
        sql2 = req_sql.sql['insert_PiC']
        try:
            self.cursor.execute(sql, sql_args)
            sql2_args = (self.cat_id, self.cursor.lastrowid)
            self.cursor.execute(sql2, sql2_args)
        except Exception as e:
            print(e)
            return

    def _update(self, update):
        """This method updates a product row
        :param update: a dict with information to update
        """
        ts = int(datetime.now().timestamp())
        # sql = UPDATE Products SET {} = {}, {}, {} WHERE id= {}
        sql = req_sql.sql['prod_update']
        key = 'substitute_id'
        sql_args = (
            update[key],
            ts,
            update['substitued_id'])
        self.cursor.execute(sql, sql_args)
