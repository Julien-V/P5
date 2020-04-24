#!/usr/bin/python3
# coding : utf-8

import os
import mysql.connector as mysqlC
# from mysql.connector import errorcode

import config as cfg


class DB():
    """Manage DB"""
    def __init__(self):
        self.name = cfg.db["name"]
        self.sqlFileName = cfg.db["create_file_name"]
        self.connect()

    def connect(self):
        try:
            self.cnx = mysqlC.connect(**cfg.db["connect"])
        except mysqlC.error as e:
            if e.errno in cfg.db["error"].keys():
                print(cfg.db["error"][e.errno])
            else:
                print(cfg.db["Uerror"].format(e.msg))
            return
        self.cursor = mysqlC.cursor()
        self.cursor.execute(cfg.db["show"])
        databases = [elem[0] for elem in self.cursor.fetchall()]
        if self.name in databases:
            self.cursor.execute("USE {}".format(self.name))
        else:
            self.create()

    def create(self):
        # Where are we ?
        dirs = os.listdir()
        if self.sqlFileName not in dirs:
            print(self.sqlFileName, " not found")
            return
        with open(self.sqlFileName, "r") as fileA:
            queries = fileA.read().split(";")
        for query in queries:
            self.cursor.execute(query)

    def executeQuery(self, query):
        try:
            self.cursor.execute(query)
            for row in self.cursor:
                print(row)
        except mysqlC.error as e:
            print(e)
