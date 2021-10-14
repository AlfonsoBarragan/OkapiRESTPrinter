 
#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for

from myapp.models import Filament, db

bp_filaments=Blueprint("bp_filaments", __name__)

def delFilament(idFilament):
    auxFilament = Filament.query.filter_by(idFilament=idFilament)
    try:
        db.session.delete(auxFilament.first())
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":idFilament}), 200)

def getFilament(idFilament):
    try:        
        auxFilament = Filament.query.filter_by(idFilament=str(idFilament))
        response = make_response(jsonify(auxFilament.first().toJSON), 200)
    except:
        abort(404)
    return response

@bp_filaments.route('/<path:idFilament>', methods = ['DELETE','GET'])
def manager_filament(idFilament):
    if request.method == 'DELETE':
        return delFilament(idFilament)
    elif request.method == 'GET':
        return getFilament(idFilament)

def getFilaments():
    listFilaments = []
    for itFilament in Filament.query.all():
        listFilaments.append(itFilament.toJSON)
    return make_response(jsonify({"filaments":listFilaments}), 200)

def addFilament():
    attr = ['name', 'seller', 'link', 'price', 'weight', 'width']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    
    name    = request.json['name']
    seller = request.json['seller']
    link = request.json['link']
    price = request.json['price']
    weight = request.json['weight']
    width = request.json['width']  

    idFilament  = (base64.b64encode((name + seller + link + price + weight + width).encode())).decode('utf-8')
    newFilament = Filament(
                    idFilament=str(idFilament),
                    name=name,
                    seller=seller,
                    link=link,
                    price=price,
                    weight=weight,
                    width=width)
    try:
        db.session.add(newFilament)
        db.session.commit()
    except:
        abort(409)
    return make_response (jsonify({"created":idFilament}), 201)

@bp_filaments.route('', methods = ['GET', 'POST'])
def manager_filaments():
    if request.method == 'POST':
        return addFilament()
    elif request.method == 'GET':
        return getFilaments()