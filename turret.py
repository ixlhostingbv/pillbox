# -*- coding: utf-8 -*-
import os, sys
import bcrypt
from eve import Eve
from eve_auth_jwt import JWTAuth
from flask import current_app as app
from flask import config, request, render_template, g
from eve_swagger import swagger, add_documentation
import tools
import logging

# set template directory
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# set log handler
handler = logging.FileHandler('pillbox.log')
# log formatter
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(filename)s:%(lineno)d] -- ip: %(clientip)s, '
    'url: %(url)s, method:%(method)s'))

# hook functions

# store ip and user 
def store_creator(resource, docs):
    ip = request.headers.get(app.config['REMOTE_ADDR_HEADER'], request.remote_addr)
    user_id = app.auth.get_request_auth_value()

    for doc in docs:
        doc['_created_by'] = user_id
        doc['_modified_by'] = user_id
        doc['_remote_addr'] = ip
        
def store_modifier(resource, doc):
    ip = request.headers.get(app.config['REMOTE_ADDR_HEADER'], request.remote_addr)
    user_id = app.auth.get_request_auth_value()

    doc['_modified_by'] = user_id
    doc['_remote_addr'] = ip

def restrict_user_superadmin(request, lookup):
    
    user_id = app.auth.get_request_auth_value()
    role = app.auth.get_user_role()
    #elif role != 'admin':
    #    lookup['role'] = {'$in': role}
    if user_id != 'superadmin':
        lookup["tenantid"] = user_id

# Create a Flask Config object
config = config.Config(os.path.dirname(os.path.abspath(__file__)))
# Load settings.py config file
config.from_pyfile('settings.py')
# Load your local_settings.py config file
config.from_pyfile('local_settings.py')

app = Eve(settings=config, auth=JWTAuth, template_folder=tmpl_dir)

# set log level and add handler
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

# hooks
app.on_insert += store_creator
app.on_replace += store_modifier
app.on_pre_GET_tenants += restrict_user_superadmin

app.register_blueprint(swagger)

app.register_blueprint(tools.bp, url_prefix='/tools')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
