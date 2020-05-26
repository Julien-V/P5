#!/usr/bin/python3
# coding : utf-8

import os
import getpass
import mysql.connector as mysql_c
# from mysql.connector import errorcode

import config as cfg


class DB:
    """This class connects or creates a MySQL database."""
    def __init__(self):
        """This method initializes the class and call self.connect()"""
        self.name = cfg.db["name"]
        self.user = cfg.db['connect']['user']
        self.sql_filename = cfg.db["create_file_name"]
        self.sql_filepath = cfg.db["create_file_path"]
        self.dict_result = False
        self.exist = False
        self.connect()

    def connect(self):
        """This method attempts a connection to mysql, check if db exist
        and use it
        """
        try:
            self.cnx = mysql_c.connect(
                user=self.user,
                password=getpass.getpass())
        except mysql_c.error as e:
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
        # parameter insertion doesn't seem to work with database name
        self.cursor.execute("USE {}".format(self.name))

    def create(self):
        """This method is called by connect()
        and create database with a *.sql file
        """
        dirs = os.listdir(self.sql_filepath)
        if self.sql_filename not in dirs:
            print(self.sql_filename, " not found")
            return
        path = os.path.join(self.sql_filepath, self.sql_filename)
        with open(path, "r") as file_a:
            queries = file_a.read().split(";")
        for query in queries:
            try:
                self.cursor.execute(query)
            except mysql_c.error as e:
                print(e)
                print(query)

    def get_cursor(self):
        """This method returns a cursor to execute queries"""
        # result will always be returned as a dict
        if not self.dict_result:
            self.cursor.close()
            self.cursor = self.cnx.cursor(dictionary=True)
            self.dict_result = True
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
