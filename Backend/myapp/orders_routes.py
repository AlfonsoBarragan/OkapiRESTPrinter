 
#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for

from myapp.models import Order, db
# from myapp.operations import calculate_cost

bp_orders=Blueprint("bp_orders", __name__)

def delOrder(idOrder):
    auxOrder = Order.query.filter_by(idOrder=idOrder)
    try:
        db.session.delete(auxOrder.first())
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":idOrder}), 200)

def getOrder(idOrder):
    try:        
        auxOrder = Order.query.filter_by(idOrder=str(idOrder))
        response = make_response(jsonify(auxOrder.first().toJSON), 200)
    except:
        abort(404)
    return response

@bp_orders.route('/<path:idOrder>', methods = ['DELETE','GET'])
def manager_order(idOrder):
    if request.method == 'DELETE':
        return delOrder(idOrder)
    elif request.method == 'GET':
        return getOrder(idOrder)

def getOrders():
    listOrders = []
    for itOrder in Order.query.all():
        listOrders.append(itOrder.toJSON)
    return make_response(jsonify({"orders":listOrders}), 200)

def addOrder():
    attr = ['shippingPlace', 'customer', 'price', 'duration', 'weight']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    shippingPlace   = request.json['shippingPlace']
    customer        = request.json['customer']
    price           = request.json['price']
    duration        = request.json['duration']
    weight          = request.json['weight']

    
    idOrder  = (base64.b64encode((shippingPlace + customer + price + duration + weight).encode())).decode('utf-8')
    newOrder = Order(
                    idOrder=str(idOrder),
                    shippingPlace=shippingPlace,
                    customer=customer,
                    price=price,
                    duration=duration,
                    weight=weight)
    try:
        db.session.add(newOrder)
        db.session.commit()
    except:
        abort(409)
    return make_response (jsonify({"created":idOrder}), 201)

@bp_orders.route('', methods = ['GET', 'POST'])
def manager_orders():
    if request.method == 'POST':
        return addOrder()
    elif request.method == 'GET':
        return getOrders()