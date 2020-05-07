#!/usr/bin/python3
# coding : utf-8

import os
import getpass
import mysql.connector as mysqlC
# from mysql.connector import errorcode

from src.models import config as cfg


class DB():
    """Manage DB"""
    def __init__(self):
        self.name = cfg.db["name"]
        self.user = cfg.db['connect']['user']
        self.sqlFileName = cfg.db["create_file_name"]
        self.sqlFilePath = cfg.db["create_file_path"]
        self.dictResult = False
        self.exist = False
        self.connect()

    def connect(self):
        try:
            self.cnx = mysqlC.connect(
                user=self.user,
                password=getpass.getpass())
        except mysqlC.error as e:
            if e.errno in cfg.db["error"].keys():
                print(cfg.db["error"][e.errno])
            else:
                print(cfg.db["Uerror"].format(e.msg))
            return
        self.cursor = self.cnx.cursor()
        self.cursor.execute(cfg.db["show"])
        databases = [elem[0] for elem in self.cursor.fetchall()]
        if self.name not in databases:
            self.create()
        self.cursor.execute("USE {}".format(self.name))

    def create(self):
        dirs = os.listdir(self.sqlFilePath)
        if self.sqlFileName not in dirs:
            print(self.sqlFileName, " not found")
            return
        path = os.path.join(self.sqlFilePath, self.sqlFileName)
        with open(path, "r") as fileA:
            queries = fileA.read().split(";")
        for query in queries:
            try:
                self.cursor.execute(query)
            except Exception as e:
                print(e)
                print(query)

    def getCursor(self):
        # result will always be returned as a dict
        if not self.dictResult:
            self.cursor.close()
            self.cursor = self.cnx.cursor(dictionary=True)
            self.dictResult = True
        return self.cursor

    def save(self):
        self.cnx.commit()

    def __del__(self):
        self.save()
        self.cursor.close()
        self.cnx.close()
