 
#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy


# Por defecto el root es $PREFIX/var/myapp-instance
app=Flask(__name__, instance_relative_config=False, static_folder="static/")
app.config.from_pyfile('../instance/development.cfg')

db = SQLAlchemy(app)

from myapp.creations_printed_routes import bp_creations
from myapp.printers_routes import bp_printers
from myapp.filaments_routes import bp_filaments
from myapp.orders_routes import bp_orders

@app.route('/')
def root():
    return app.send_static_file('index.html')


app.register_blueprint(bp_creations, url_prefix="/creations_printed")
app.register_blueprint(bp_printers, url_prefix="/printers")
app.register_blueprint(bp_filaments, url_prefix="/filaments")
app.register_blueprint(bp_orders, url_prefix="/orders")

db.init_app(app)
with app.app_context():
    db.create_all()

# Este podría ir en otro Blueprint
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)
