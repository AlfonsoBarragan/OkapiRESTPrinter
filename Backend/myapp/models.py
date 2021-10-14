#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import url_for
from . import db

orders_tab = db.Table('orders_tab',
    db.Column('order_id', db.String(64), db.ForeignKey('orders.idOrder')),
    db.Column('creation_id', db.String(64), db.ForeignKey('creations.idCreation')),
    db.Column('filament_id', db.String(64), db.ForeignKey('filaments.idFilament')),
    db.Column('printer_id', db.String(64), db.ForeignKey('printers.idPrinter'))
)

class Creation(db.Model):
    __tablename__   = 'creations'
    idCreation      = db.Column(db.String(64), primary_key=True)
    name            = db.Column(db.String(40), nullable=False)
    author          = db.Column(db.String(40), nullable=False)
    price           = db.Column(db.Integer)
    time            = db.Column(db.Integer)
    materialWasted  = db.Column(db.Integer)
    description     = db.Column(db.String(128), nullable=True)

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):        
        return dict([ (c, getattr(self, c)) for c in self.columns ])

class Filament(db.Model):
    __tablename__   = 'filaments'
    idFilament      = db.Column(db.String(64), primary_key=True)
    name            = db.Column(db.String(40), nullable=False)
    seller          = db.Column(db.String(40), nullable=False)
    link            = db.Column(db.String(256), nullable=False)
    price           = db.Column(db.Integer)
    weight          = db.Column(db.Integer)
    width           = db.Column(db.Float)

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):        
        return dict([ (c, getattr(self, c)) for c in self.columns ])

class Printer(db.Model):
    __tablename__   = 'printers'
    idPrinter       = db.Column(db.String(64), primary_key=True)
    name            = db.Column(db.String(40), nullable=False)
    consume         = db.Column(db.Integer)

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):        
        return dict([ (c, getattr(self, c)) for c in self.columns ])

class Order(db.Model):
    __tablename__   = 'orders'
    idOrder         = db.Column(db.String(64), primary_key=True)
    shippingPlace   = db.Column(db.String(64), nullable=False)
    customer        = db.Column(db.String(40), nullable=False)
    price           = db.Column(db.Float)
    duration        = db.Column(db.Integer)
    weight          = db.Column(db.Float)

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):        
        return dict([ (c, getattr(self, c)) for c in self.columns ])