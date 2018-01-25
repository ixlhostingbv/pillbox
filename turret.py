# -*- coding: utf-8 -*-
import os, sys
import bcrypt
from eve import Eve
from eve.auth import BasicAuth
from flask import current_app as app
from flask import config, request, render_template
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

# token based authentication with roles
class Authenticate(BasicAuth):
    
    def get_user_role(self):
                return g.get('roles')

    def set_user_role(self, role:
        g.role = role

    def check_auth(self, username, password, allowed_roles, resource, method):

        app.logger.debug('AUTH: resource: {} user: {} pass: {} method: {}'.format(resource,username,password,method))
        
        accounts = app.data.driver.db['tenants']
        lookup = {}
        lookup['tenantid'] = username
        if allowed_roles:
            lookup['role'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)
        if account:
             self.set_request_auth_value(account['tenantid'])
        return account and bcrypt.hashpw(str(password).encode('utf-8'), str(account['password']).encode('utf-8')) == account['password']
    
    def check_auth_token(self, token, allowed_roles, resource, method):

        app.logger.debug('AUTH: resource: {} token: {} method: {}'.format(resource, token, method))

        if resource == 'tenants' and app.config['SUPER_USER_TOKEN'] and token == app.config['SUPER_USER_TOKEN']:
            self.set_request_auth_value('superadmin')
            return True

        accounts = app.data.driver.db['tenants']
        lookup = {}
        lookup['tokens'] = token
        if allowed_roles:
            lookup['role'] = { '$in': allowed_roles }
        account = accounts.find_one(lookup)
        if account:
             self.set_request_auth_value(account['tenantid'])
        return account

    def authorized(self, allowed_roles, resource, method):
        """ Validates the the current request is allowed to pass through. """
        auth = request.authorization
        token = None

        if not auth and request.headers.get('Authorization'):
            token = request.headers.get('Authorization').strip()
            if token.lower().startswith(('token', 'bearer')):
                token = token.split(' ')[1]

        if auth:
            self.set_user_or_token(auth)
            return auth and self.check_auth(auth.username, auth.password, allowed_roles, resource, method)

        if token:
            self.set_user_or_token(token)
            return token and self.check_auth_token(token, allowed_roles, resource, method)


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
    if user_id != 'superadmin':
        lookup["tenantid"] = user_id
    if use

# Create a Flask Config object
config = config.Config(os.path.dirname(os.path.abspath(__file__)))
# Load settings.py config file
config.from_pyfile('settings.py')
# Load your local_settings.py config file
config.from_pyfile('local_settings.py')

app = Eve(settings=config, auth=Authenticate, template_folder=tmpl_dir)

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
