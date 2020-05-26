#!/usr/bin/python3
# coding : utf-8

# SQL
#########################

sql = dict()
sql["test"] = "SELECT * from Categories"

sql["insert_cat"] = (
    """INSERT INTO Categories """
    """(category_name) VALUES (%s)""")

sql["insert_PiC"] = (
    """INSERT INTO Prod_in_Cat """
    """(category_id, product_id) VALUES (%s, %s)""")

sql["insert_prod"] = (
    """INSERT INTO Products """
    """(product_name, brands, code, """
    """categories, nutrition_grades, """
    """stores, url, added_timestamp) """
    """VALUES (%s, %s, %s, """
    """%s, %s, """
    """%s, %s, %s)""")

sql['prod_update'] = (
    """UPDATE Products """
    """SET substitute_id = %s, """
    """updated_timestamp = %s """
    """WHERE id = %s""")

# SQL Subs Menu
sql['displayByCat'] = (
    """SELECT * FROM Products LEFT JOIN Prod_in_Cat """
    """ON Products.id=Prod_in_Cat.product_id """
    """WHERE Prod_in_Cat.category_id=%s""")

sql['subst'] = sql['displayByCat'] + """ ORDER BY nutrition_grades"""

sql['prod'] = """SELECT * FROM Products WHERE id = %s"""

# SQL Disp Menu
sql['displayAll'] = (
    """SELECT * FROM Products WHERE substitute_id IS NOT NULL""")

sql['disp'] = sql['displayAll']
