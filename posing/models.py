#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Posing - db.py
--------------

This is the database models for the ORM
"""

from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

from sqlalchemy import create_engine
db_path = 'sqlite:///:memory:'
engine = create_engine(dp_path, echo=True)

#=================================
# User models

user_role_assoc = Table("user_role", Base.metadata,
                        Column("users", Integer, ForeignKey("users.id")),
                        Column("roles", Integer, ForeignKey("roles.id")))

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    roles = relationship("Role", secondary="user_role_assoc", backref='users')
    

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


# class UserRoleAssoc(Base):
    # __tablename__ = "user_role_assoc"
    
    # user_id = Column(Integer, ForeignKey("users.id"))
    # role_id = Column(Integer, ForeignKey("roles.id"))
        

#=================================
# stock models
    
item_stock_assoc = Table("item_stock", Base.metadata,
                         Column("stock", Integer, ForeignKey("stock.id")),
                         Column("item", Integer, ForeignKey("items.id")))    

class Stock(Base):
    __tablename__ = "stock"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    
class StockCatagory(Base):
    __tablename__ = "stock_catagories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    stock = relationship("Stock", backref=backref("catagory"))
    
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    stock = relationship("Stock", secondary="item_stock_assoc")
    

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True)
    