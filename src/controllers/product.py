#!/usr/bin/python3
# coding : utf-8

from datetime import datetime

from src.models import config as cfg


class Product():
    def __init__(self, model, category_id):
        # self.view = view
        self.cursor = model
        self.cat_id = category_id
        self.spec = dict()

    def get_validate_insert(self, prod, update=False):
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
            update['substituedID'] = prod['id']
            self._update(update)

    def _validate_product_spec(self):
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
        s = self.spec
        sql = cfg.sql['insert_prod']
        sql = sql.format(
            s['product_name'], s['brands'], s['code'],
            s['categories'], s['category_id'], s['nutrition_grades'],
            s['stores'], s['url'], s['added_timestamp']
            )
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return
            # self.db.executeQuery(query)

    def _update(self, update):
        ts = int(datetime.now().timestamp())
        # control ?
        sql = cfg.sql['prodUpdate']
        key = 'substitute_id'
        sql = sql.format(
            key,
            update[key],
            'updated_timestamp',
            ts,
            update['substituedID'])
        self.cursor.execute(sql)
