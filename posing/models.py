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
    admin = Role(name="Admin")
    employee = Role(name="Employee")
    # add roles
    session.add_all([admin, employee])
    user1 = User(name="derp1", 
                 fullname="one, derp", 
                 password="bleep", 
                 role=[admin])
    user2 = User(name="derp2", 
                 fullname="two, derp",
                 password="blerp", 
                 role=[employee])
    #add users
    session.add_all([user1, user2])
    tinned = StockCategory(name="Tinned Consumable")
    herb = StockCategory(name="Dried Herb")
    sauce = StockCategory(name="Sauce")
    fresh = StockCategory(name="Fresh Produce")
    meat = StockCategory(name="Meat/Poultry")
    # add stock catagories
    session.add_all([tinned, herb, sauce, fresh, meat])
    tin_tomato = Stock(name="Tinned Tomatoes", category=tinned)
    tin_peach = Stock(name="Tinned Peach", category=tinned)
    oregano = Stock(name="Oregano", category=herb)
    parsley = Stock(name="Parsley", category=herb)
    mixed_herb = Stock(name="Mixed Herbs", category=herb)
    sauce_tom = Stock(name="Tomato Sauce", category=sauce)
    sauce_mayo = Stock(name="Mayonaise", category=sauce)
    cabbage = Stock(name="Cabbage", category=fresh)
    spinach = Stock(name="Spinach", category=fresh)
    tomato = Stock(name="Tomato", category=fresh)
    steak = Stock(name="Steak", category=meat)
    # add stock
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
    steak_veg = Item(name="Steak and Veg", 
                     unit_price=11.50, 
                     stock=[steak, 
                            spinach, 
                            tomato])
    steak_napoli = Item(name="Steak Napoli", 
                        unit_price=13, 
                        stock=[steak,
                               tin_tomato,
                               oregano,
                               parsley])
    # add items
    session.add_all([steak_veg, steak_napoli])
    order1 = Order(customer="Billy Jean", 
                   items=[steak_veg, 
                          steak_napoli])
    # add order
    session.add(order1)
    sale1 = Sale(order=order1, operator=user2)
    # add sale
    session.add(sale1)
    # commit to db
    session.commit()
    
    for row in session.query(User).all():
        print(row)
    
    for row in session.query(Role).all():
        print(row)

    for row in session.query(Stock).all():
            print(row)    

    for row in session.query(Item).all():
            print(row)

    for row in session.query(Order).all():
            print(row)
            
    for row in session.query(Sale).all():
            print(row)            
            
#=================================
# User models

user_role_assoc = Table("user_role", 
                        Base.metadata,
                        Column("user_id", 
                               Integer, 
                               ForeignKey("users.id")),
                        Column("role_id", 
                               Integer, 
                               ForeignKey("roles.id")))

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    role = relationship("Role", secondary=user_role_assoc, backref='users')

    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (self.name,
                                                     self.fullname)

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    def __repr__(self):
        return "<Role(name='%s')>" % self.name

#=================================
# stock models
    
item_stock_assoc = Table("item_stock", 
                         Base.metadata,
                         Column("stock_id", 
                                Integer, 
                                ForeignKey("stock.id")),
                         Column("item_id", 
                                Integer, 
                                ForeignKey("items.id")))    

class Stock(Base):
    __tablename__ = "stock"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("stock_categories.id"))
    category = relationship("StockCategory")
    
    def __repr__(self):
        return "<Stock(name='%s', category=%s)>" % (self.name, 
                                                    self.category)
    
    
class StockCategory(Base):
    __tablename__ = "stock_categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    def __repr__(self):
        return "<StockCategory(name='%s')>" % self.name
    
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    unit_price = Column(Float)
    quantity = Column(Integer)
    stock = relationship("Stock", secondary=item_stock_assoc)
    
    def __repr__(self):
        return "<Item(name='%s')>" % self.name


#=================================
# orders and sales    

order_item_assoc = Table("order_items", 
                         Base.metadata,
                         Column("order_id", 
                                Integer, 
                                ForeignKey("orders.id")),
                         Column("item_id", 
                                Integer, 
                                ForeignKey("items.id")))

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True)
    date = Date()
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order")
    operator_id = Column(Integer, ForeignKey("users.id"))
    operator = relationship("User")
    
    def __repr__(self):
        return "<Sale(date='%s', order=%s)>" % (self.date, 
                                                self.order)
    
    
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer = Column(String)
    #sale_id = Column(Integer, ForeignKey("sales.id"))
    items = relationship("Item", secondary=order_item_assoc)
    
    def __repr__(self):
        return "<Order(customer='%s')>" % self.customer

    
if __name__ == "__main__":
    refresh_models()
    add_test_data()
    print(Base)