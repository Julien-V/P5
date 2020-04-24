#!/usr/bin/python3
# coding : utf-8


class Product():
    def __init__(self):
        self.spec = dict()

    def addSpec(self, args):
        # args (dict) given by controller
        for arg in args.keys():
            self.spec[arg] = args[arg]
