#!/usr/bin/python3
# coding : utf-8

import getpass

locale = "fr"

db = dict()

db["name"] = "openff"
db["create_file_name"] = "create-db.sql"

db["connect"] = {
    'user': getpass.getuser(),
    'password': lambda: getpass.getpass()
}

db["error"] = {
    1044: "",
    1698: "Invalid Password, Access Denied"
}

db["Uerror"] = "Unknown Error : \n {}"

db["config"] = {
  'user': getpass.getuser(),
  # 'password': getpass.getpass(),
  'host': '127.0.0.1',
  'database': db["name"],
  'raise_on_warnings': True
}

db["show"] = "SHOW DATABASES"

# name of table like {}
db["insert"] = (
    "INSERT INTO substitute "
    "(id, barcode, categories, categories_hierarchy, choosen_category, nutrition_grades, image_url) "
    "VALUES ({}, {}, {}, {}, {}, {}, {})")

db["get"] = ("SELECT * FROM substitute")
