#!/usr/bin/python
#!-*- coding:utf-8 -*-

"""
Posing - cherrypy.py
--------------------
Represents the web server - currently just POC

"""


import os

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
print(sys.path)
from posing import models

import cherrypy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('web/templates'))
current_dir = os.path.dirname(os.path.abspath(__file__))

session = models.Session()

class App(object):
    
    @cherrypy.expose
    def index(self):
        page = env.get_template("base.html")
        return page.render(title="test")
    
    @cherrypy.expose
    def viewSales(self):
        sales = session.query(models.Sale).all()
        page = env.get_template("sales.html")
        return page.render(title="Sales!", sales=sales)
    
    
def run():
    cherrypy.quickstart(App(), '/', config="config.ini")
    
    
if __name__ == "__main__":
    run()
    