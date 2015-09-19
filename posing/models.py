#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Posing - db.py
--------------

This is the database models for the ORM
"""

from sqlalchemy import ForeignKey, Table, Column, Integer, Float, String, Date
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime

import config
Config = config.parse_config()

Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine(Config["general"]["db_path"], echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def refresh_models():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def add_test_data():
    
    user1 = User(name="derp1", fullname="one, derp", password="bleep")
    user2 = User(name="derp2", fullname="two, derp", password="blerp")
    session.add_all([user1, user2])
    
    tinned = StockCatagory("Tinned Consumable")
    herb = StockCatagory("Dried Herb")
    sauce = StockCatagory("Sauce")
    fresh = StockCatagory("Fresh Produce")
    meat = StockCatagory("Meat/Poultry")
    session.add_all([tinned, herb, sauce, fresh, meat])

    tin_tomato = Stock("Tinned Tomatoes", tinned)
    tin_peach = Stock("Tinned Peach", tinned)
    oregano = Stock("Oregano", herb)
    parsley = Stock("Parsley", herb)
    mixed_herb = Stock("Mixed Herbs", herb)
    sauce_tom = Stock("Tomato Sauce", sauce)
    sauce_mayo = Stock("Mayonaise", sauce)
    cabbage = Stock("Cabbage", fresh)
    spinach = Stock("Spinach", fresh)
    tomato = Stock("Tomato", fresh)
    steak = Stock("Steak", meat)
    session.add_all([tin_tomato,
                     tin_peach,
                     oregano,
                     parsley,
                     mixed_herb,
                     sauce_tom,
                     sauce_mayo,
                     cabbage,
                     spinach,
                     tomato,
                     steak])
    
    steak_veg = Item("Steak and Veg", 11.50, [steak, spinach, tomato])
    session.add(steak_veg)
    
    order1 = Order("Billy Jean", [steak_veg])
    session.add(order1)
    
    sale1 = Sale()
    sale1.operator = user1  
    sale1.order = order1
    session.add(sale1)
    
    session.commit()

    


#=================================
# User models

user_role_assoc = Table("user_role", Base.metadata,
                        Column("user_id", Integer, ForeignKey("users.id")),
                        Column("role_id", Integer, ForeignKey("roles.id")))

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    role = relationship("Role", secondary=user_role_assoc, backref='users')
        

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    def __init__(self, name, desc=""):
        self.name = name
        self.description = desc

# class UserRoleAssoc(Base):
    # __tablename__ = "user_role_assoc"
    
    # user_id = Column(Integer, ForeignKey("users.id"))
    # role_id = Column(Integer, ForeignKey("roles.id"))
        

#=================================
# stock models
    
item_stock_assoc = Table("item_stock", Base.metadata,
                         Column("stock_id", Integer, ForeignKey("stock.id")),
                         Column("item_id", Integer, ForeignKey("items.id")))    

class Stock(Base):
    __tablename__ = "stock"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    catagory = ForeignKey("stock_catagories.id")
    
    def __init__(self, name, catagory, desc=""):
        self.name = name
        self.description = desc
    
    
class StockCatagory(Base):
    __tablename__ = "stock_catagories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    def __init__(self, name, desc=""):
        self.name = name
        self.description = desc
        
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    unit_price = Column(Float)
    quantity = Column(Integer)
    stock = relationship("Stock", secondary=item_stock_assoc)
    
    def __init__(self, name, price, stock, quantity=1, desc=""):
        self.name = name
        self.unit_price = price
        self.stock = stock
        self.quantity = quantity
        self.description = desc
        


#=================================
# orders and sales    

# order_item_assoc = Table("order_items", Base.metadata,
                         # Column("order_id", Integer, ForeignKey("orders.id")),
                         # Column("item_id", Integer, ForeignKey("items.id")))

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True)
    date = Date()
    order = ForeignKey("Order.id")
    operator = ForeignKey("User.id")
    
    def __init__(self):
        self.date = datetime.datetime.now()
        
    
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer = Column(String)
    sale_id = ForeignKey("sales.id")
    items = relationship("OrderItems")
    
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items


class OrderItems(Base):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    order = relationship("Order")
    quantity = Column(Integer)
    
if __name__ == "__main__":
    refresh_models()
    add_test_data()
    print(Base)