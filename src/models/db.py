#!/usr/bin/python3
# coding : utf-8

import os
import getpass
import mysql.connector as mysqlC
# from mysql.connector import errorcode

from src.models import config as cfg


class DB():
    """This class connects or creates a MySQL database."""
    def __init__(self):
        """This method initializes the class and call self.connect()"""
        self.name = cfg.db["name"]
        self.user = cfg.db['connect']['user']
        self.sqlFileName = cfg.db["create_file_name"]
        self.sqlFilePath = cfg.db["create_file_path"]
        self.dictResult = False
        self.exist = False
        self.connect()

    def connect(self):
        """This method attempts a connection to mysql, check if db exist
        and use it
        """
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
        """This method is called by connect()
        and create database with a *.sql file
        """
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
            except mysqlC.error as e:
                print(e)
                print(query)

    def getCursor(self):
        """This method returns a cursor to execute queries"""
        # result will always be returned as a dict
        if not self.dictResult:
            self.cursor.close()
            self.cursor = self.cnx.cursor(dictionary=True)
            self.dictResult = True
        return self.cursor

    def save(self):
        """This method commits modification into database"""
        self.cnx.commit()

    def __del__(self):
        """This method saves, closes cursor and connection to DB
        when this object is removed
        """
        self.save()
        self.cursor.close()
        self.cnx.close()
