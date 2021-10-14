 
#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for

from myapp.models import Printer, db
# from myapp.operations import calculate_cost

bp_printers=Blueprint("bp_printers", __name__)

def delPrinter(idPrinter):
    auxPrinter = Printer.query.filter_by(idPrinter=idPrinter)
    try:
        db.session.delete(auxPrinter.first())
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":idPrinter}), 200)

def getPrinter(idPrinter):
    try:        
        auxPrinter = Printer.query.filter_by(idPrinter=str(idPrinter))
        response = make_response(jsonify(auxPrinter.first().toJSON), 200)
    except:
        abort(404)
    return response

@bp_printers.route('/<path:idPrinter>', methods = ['DELETE','GET'])
def manager_printer(idPrinter):
    if request.method == 'DELETE':
        return delPrinter(idPrinter)
    elif request.method == 'GET':
        return getPrinter(idPrinter)

def getPrinters():
    listPrinters = []
    for itPrinter in Printer.query.all():
        listPrinters.append(itPrinter.toJSON)
    return make_response(jsonify({"printers":listPrinters}), 200)

def addPrinter():
    attr = ['name', 'consume']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    
    name    = request.json['name']
    consume = request.json['consume']
    
    idPrinter  = (base64.b64encode((name + consume).encode())).decode('utf-8')
    newPrinter = Printer(
                    idPrinter=str(idPrinter),
                    name=name,
                    consume=consume)
    try:
        db.session.add(newPrinter)
        db.session.commit()
    except:
        abort(409)
    return make_response (jsonify({"created":idPrinter}), 201)

@bp_printers.route('', methods = ['GET', 'POST'])
def manager_printers():
    if request.method == 'POST':
        return addPrinter()
    elif request.method == 'GET':
        return getPrinters()