 
#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for

from myapp.models import Creation, db
# from myapp.operations import calculate_cost

bp_creations=Blueprint("bp_creations", __name__)

def delCreation(idCreation):
    auxCreation = Creation.query.filter_by(idCreation=idCreation)
    try:
        db.session.delete(auxCreation.first())
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":idCreation}), 200)

def getCreation(idCreation):
    try:        
        auxCreation = Creation.query.filter_by(idCreation=str(idCreation))
        response = make_response(jsonify(auxCreation.first().toJSON), 200)
    except:
        abort(404)
    return response

@bp_creations.route('/<path:idCreation>', methods = ['DELETE','GET'])
def manager_creation(idCreation):
    if request.method == 'DELETE':
        return delCreation(idCreation)
    elif request.method == 'GET':
        return getCreation(idCreation)

def getCreations():
    listCreations = []
    for itCreation in Creation.query.all():
        listCreations.append(itCreation.toJSON)
    return make_response(jsonify({"creations":listCreations}), 200)

def addCreation():
    attr = ['name', 'author', 'time', 'materialWasted', 'description']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    name                = request.json['name']
    author              = request.json['author']
    price               = request.json['price']
    time                = request.json['time']
    materialWasted      = request.json['materialWasted']
    description         = request.json['description']
    
    idCreation  = (base64.b64encode((name + author + price + time + materialWasted).encode())).decode('utf-8')
    newCreation = Creation(
                    idCreation=str(idCreation),
                    name=name,
                    author=author,
                    price=price,
                    time=time,
                    materialWasted=materialWasted,
                    description=description)
    try:
        db.session.add(newCreation)
        db.session.commit()
    except:
        abort(409)
    return make_response (jsonify({"created":idCreation}), 201)

@bp_creations.route('', methods = ['GET', 'POST'])
def manager_creations():
    if request.method == 'POST':
        return addCreation()
    elif request.method == 'GET':
        return getCreations()