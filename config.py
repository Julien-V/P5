#!/usr/bin/python3
# coding : utf-8

import getpass

from openff.models import req_sql
# from openff.views import menu
from openff.views import menu_models as mm

from openff.controllers import controller as ctrl

locale = "fr"
title = "Projet 5"

back = '777'
exit = '999'

# DB
#########################

db = dict()

db["name"] = "openff"
db["create_file_name"] = "create-db.sql"
db["create_file_path"] = "openff/models/"

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
    'url': str
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
text['cat_choice'] = [
    cat, {
        'text': 'Catégorie',
        'title': 'Choix de la catégorie'
    }
]
text['prod_choice'] = [
    [], {
        'text': 'Produit',
        'title': 'Choix du produit'
    }
]
text['prod_details'] = [
    [], {
        'text': '',
        'title': ''
    }
]
text['subs_choice'] = [
    [], {
        'text': 'Substitution',
        'title': 'Choix du produit à substituer'
    }
]
text['subs_details'] = [
    [], {
        'text': '777 to go back, enter to save substitute',
        'title': ''
    }
]
# Display subs text
all_s = "Tout mes produits substitués"
text['display'] = [
    ["Par catégorie", all_s], {
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
text['disp_choice'] = [
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
# cat_choice
param_ext_cc = {
    'query': req_sql.sql['test']
}
# prod_choice
param_ext_pc = {
    '4query': 'category_id',
    'query': req_sql.sql['displayByCat'],
    'format': [
        lambda i: [i, f"{i['product_name']} // {i['brands']}"],
        lambda i: f"{i[1]} // {i[0]['nutrition_grades']}"
    ]
}
# prod_details
nG = 'nutrition_grades'


# substChoice
param_ext_sc = {
    '4query': 'category_id',
    'query': req_sql.sql['subst'],
    'process': [lambda i: [x for x in i.result if x[nG] < i.item[nG]]],
    'format': [
        lambda i: [i, f"{i['product_name']}"],
        lambda i: f"{i[1]} // {i[0]['nutrition_grades']}"
    ],
}
# display
param_ext_dc = {
    'query': req_sql.sql['displayAll'],
    'process': [
        lambda i: [
            i,
            [i.query(req_sql.sql['prod'], x['substitute_id']-1) for x in i.result]
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

""" STEP
kwargs.keys() = ['text', 'title', lines']  # possible key
args = [listValues, **kwargs]
var = [view, controller, args, paramExt]
"""

choice = mm.ChoiceList
print_line = mm.PrintLineDB
ctrller = ctrl.Controller

cat_choice = [choice, ctrller, text['cat_choice'], param_ext_cc]
prod_choice = [choice, ctrller, text['prod_choice'], param_ext_pc]
prod_details = [print_line, ctrller, text['prod_details']]
# subs_choice = [choice, ctrller, text['subs_choice'], param_ext_sc]
subs_prop = [print_line, ctrller, text['subs_details'], param_ext_sc]
end = [None, None, None]  # the end

disp_choice = [choice, ctrller, text['disp_choice'], param_ext_dc]

# Substitute
step_sub = {
    'cat_choice': cat_choice,
    'prod_choice': prod_choice,
    'subs_choice': subs_prop,
    'prod_update': end,
    'end': end
}

# Display
step_disp_all = {
    'disp_choice': disp_choice,
    'prod_details': prod_details,
    'end': end
}


"""Group of steps contained in a dict with a key 'param'
'param': [view, controller, args]
with args = [listValues, **kwargs]
"""
step_app = {
    'substitute': step_sub,
    'display': step_disp_all,
    'param': [choice, ctrller, text['start']]
}
