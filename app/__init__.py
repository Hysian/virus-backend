#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/23
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    
    cache.init_app(app)
    
    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()
    return app
