#!/usr/bin/python3
# coding : utf-8

import getpass

# config.py here(src/models) or in src/ with core.py ?

locale = "fr"
title = "Projet 5"

# Dict

db = dict()

db["name"] = "openff"
db["create_file_name"] = "create-db.sql"
db["create_file_path"] = "src/models/"

db["connect"] = {
    'user': getpass.getuser(),
}

db["error"] = {
    1044: "",
    1698: "Invalid Password, Access Denied"
}

db["Uerror"] = "Unknown Error : \n {}"

db["show"] = "SHOW DATABASES"

db["test"] = "SELECT * from Categories"

db["insert_cat"] = ["LOCK TABLES Categories WRITE", (
    """INSERT INTO Categories """
    """(category_name) VALUES ("{}")"""),
    "UNLOCK TABLES"
]

db["insert_prod"] = ["LOCK TABLES Products WRITE", (
    """INSERT INTO Products """
    """(product_name, brands, code, """
    """categories, category_id, nutrition_grades, """
    """stores, added_timestamp) """
    """VALUES ("{}", "{}", {}, """
    """"{}", {}, "{}", """
    """"{}", {})"""), "UNLOCK TABLES"]


db["product_check"] = {
    'product_name': str,
    'brands': str,
    'code': int,
    'categories': str,
    'nutrition_grades': str,
    'stores': str,
}

db["product_type"] = db["product_check"].copy()
db["product_type"]["category_id"] = int
db["product_type"]["added_timestamp"] = int

db["product_val"] = db['product_type'].keys()


db['displayByCat'] = "SELECT * FROM Products WHERE category_id = {}"
db['displaySByCat'] = (
    """SELECT * FROM Products """
    """WHERE category_id = {} AND substitute_id IS NOT NULL""")
db['displaySAll'] = (
    """SELECT * FROM Products WHERE substitute_id IS NOT NULL""")

db['subst'] = (
    """SELECT * FROM Products """
    """WHERE category_id = {} """
    """ORDER BY nutrition_grades""")

db['prodUpdate'] = (
    """UPDATE Products """
    """SET {} = {}, """
    """{} = {} """
    """WHERE id = {}""")

db['prod'] = """SELECT * FROM Products WHERE id = {}"""

# Requests

headers = {'user-agent': 'OC_P5/0.1'}
# url = "https://{}.openfoodfacts.org/categorie/{}.json"
url = "https://{}.openfoodfacts.org/cgi/search.pl?".format(locale)

param = {
    "action": "process",
    "page": 1,
    # only 200 to avoid timeout
    "page_size": 200,
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "",
    "json": True
}

cat = ["desserts-au-chocolat", "boissons-instantanees"]
cat.append("cereales-au-chocolat")

# Menu :

menu = dict()
menu['start'] = [
    ["Substituer un aliment", "Afficher les aliments substitués"],
    "Menu", title]

menu['catChoice'] = [
    cat, "Substituer",
    "Choix de la catégorie"
]

menu['display'] = [["By Category", "All"], "Afficher", "Afficher"]
menu['displayByCat'] = [cat, "Catégorie", "Afficher par catégorie"]
