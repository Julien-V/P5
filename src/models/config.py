#!/usr/bin/python3
# coding : utf-8

import getpass

from src.views import menu
from src.views import menu_models as mm

from src.controllers import controller as ctrl
# config.py here(src/models) or in src/ with core.py ?

locale = "fr"
title = "Projet 5"

# DB
#########################

db = dict()

db["name"] = "openff"
db["create_file_name"] = "create-db.sql"
db["create_file_path"] = "src/models/"

db["connect"] = {
    'user': getpass.getuser(),
}

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


db["error"] = {
    1044: "",
    1698: "Invalid Password, Access Denied"
}

db["Uerror"] = "Unknown Error : \n {}"

db["show"] = "SHOW DATABASES"

# SQL
#########################

sql = dict()
sql["test"] = "SELECT * from Categories"

sql["insert_cat"] = (
    """INSERT INTO Categories """
    """(category_name) VALUES ("{}")""")

sql["insert_prod"] = (
    """INSERT INTO Products """
    """(product_name, brands, code, """
    """categories, category_id, nutrition_grades, """
    """stores, added_timestamp) """
    """VALUES ("{}", "{}", {}, """
    """"{}", {}, "{}", """
    """"{}", {})""")

sql['prodUpdate'] = (
    """UPDATE Products """
    """SET {} = {}, """
    """{} = {} """
    """WHERE id = {}""")

# SQL Subs Menu
sql['displayByCat'] = "SELECT * FROM Products WHERE category_id = {}"

sql['subst'] = (
    """SELECT * FROM Products """
    """WHERE category_id = {} """
    """ORDER BY nutrition_grades""")

sql['prod'] = """SELECT * FROM Products WHERE id = {}"""

# SQL Disp Menu
sql['displayAll'] = (
    """SELECT * FROM Products WHERE substitute_id IS NOT NULL""")

sql['disp'] = sql['displayAll']

# Requests
#########################

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


# Text for Menu
#########################

text = dict()
text['start'] = [
    ["Substituer un aliment", "Afficher les aliments substitués"], {
        'text': 'Menu',
        'title': title
    }]
# Substitute text
text['catChoice'] = [
    cat, {
        'text': 'Catégorie',
        'title': 'Choix de la catégorie'
    }
]
text['prodChoice'] = [
    [], {
        'text': 'Produit',
        'title': 'Choix du produit'
    }
]
text['prodDetails'] = [
    [], {
        'text': '',
        'title': ''
    }
]
text['subsChoice'] = [
    [], {
        'text': 'Substitution',
        'title': 'Choix du produit à substituer'
    }
]
text['subsDetails'] = [
    [], {
        'text': '',
        'title': ''
    }
]
# Display subs text
allS = "Tout mes produits substitués"
text['display'] = [
    ["Par catégorie", allS], {
        'text': 'Afficher',
        'title': 'Afficher'
    }
]
text['displayByCat'] = [
    cat, {
        'text': "Catégorie",
        'title': "Afficher par catégorie"
    }
]
text['dispChoice'] = [
    [], {
        'text': "Produit"
    }
]


# paramExt
#########################

# paramExt = dict()
# paramExt['format'] = [
#    (lambda i: i['product_name'] + " // " + str(i['barcode'])
# ]

paramExt = dict()
# catChoice
paramExtCC = {
    'query': sql['test']
}
# prodChoice
paramExtPC = {
    '4query': 'category_id',
    'query': sql['displayByCat'],
    'format': [
        lambda i: [i, f"{i['id']} // {i['product_name']}"],
        lambda i: f"{i[1]} // {i[0]['nutrition_grades']}"
    ]
}
# prodDetails
nG = 'nutrition_grades'


# substChoice
paramExtSC = {
    '4query': 'category_id',
    'query': sql['subst'],
    'process': [lambda i: [x for x in i.result if x[nG] < i.item[nG]]],
    'format': [
        lambda i: [i, f"{i['product_name']}"],
        lambda i: f"{i[1]} // {i[0]['nutrition_grades']}"
    ],
}
# display
paramExtDC = {
    'query': sql['displayAll'],
    'process': [
        lambda i: [
            i,
            [i.query(sql['prod'], x['substitute_id']-1) for x in i.result]
        ],
        lambda i: [
            i[0],
            [{k+'S': v for k, v in list(elem[0].items())} for elem in i[1]]
        ],
        lambda i: [
            i[0],
            [i[0].result[idD].update(elem) for idD, elem in enumerate(i[1])]
        ],
        lambda i: i[0].result
    ],
    'format': [
        lambda i: [i, f"{i['product_name']} // {i[nG]}"],
        lambda i: [i[0], f"{i[1]} --> {i[0]['product_nameS']}"],
        lambda i: f"{i[1]} // {i[0]['nutrition_gradesS']}"
    ]
}

# Menu :
#########################

""" STEP FORMAT
kwargs.keys() = ['text', 'title', lines']
args = [listValues, **kwargs]
var = [view, controller, args, #format with lambda?,# query ?]"""

choice = mm.ChoiceList
printLine = mm.PrintLineDB
ctrller = ctrl.Controller

catChoice = [choice, ctrller, text['catChoice'], paramExtCC]
prodChoice = [choice, ctrller, text['prodChoice'], paramExtPC]
prodDetails = [printLine, ctrller, text['prodDetails']]
subsChoice = [choice, ctrller, text['subsChoice'], paramExtSC]
# subsDetails = [choice, ctrller, text['subsDetails']]
end = [None, None, None]  # the end

dispChoice = [choice, ctrller, text['dispChoice'], paramExtDC]

# Substitute
stepSub = {
    'catChoice': catChoice,
    'prodChoice': prodChoice,
    'subsChoice': subsChoice,
    'prodUpdate': end,
    'end': end
}

# Display
stepDispAll = {
    'dispChoice': dispChoice,
    'prodDetails': prodDetails,
    'end': end
}


"""Group of steps contained in a dict with a key 'param'
'param': [view, controller, args]
with args = [listValues, **kwargs]
"""
stepApp = {
    'substitute': stepSub,
    'display': stepDispAll,
    'param': [choice, ctrller, text['start']]
}
