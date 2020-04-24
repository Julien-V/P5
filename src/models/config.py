#!/usr/bin/python3
# coding : utf-8

import getpass

locale = "fr"

# Dict

db = dict()

db["name"] = "openff"
db["create_file_name"] = "create-db.sql"

db["connect"] = {
    'user': getpass.getuser(),
    'pass': lambda: getpass.getpass()
}

db["error"] = {
    1044: "",
    1698: "Invalid Password, Access Denied"
}

db["Uerror"] = "Unknown Error : \n {}"

db["show"] = "SHOW DATABASES"


db["insert_cat"] = (
    "INSERT INTO Categories "
    "(category_name) VALUES ({})")

db["insert_prod"] = (
    "INSERT INTO Products "
    "(id, product_name, brand, barcode, "
    "categories, category_id, nutrition_grades, "
    "stores, added_timestamp) "
    "VALUES ({}, {}, {}, {}, "
    "{}, {}, {}, "
    "{}, {})")

db["get"] = ("SELECT * FROM substitute")


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
