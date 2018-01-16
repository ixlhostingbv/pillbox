# -*- coding: utf-8 -*-
import os

MONGO_HOST = os.environ.get('MONGO_HOST', '127.0.0.1')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'pillbox')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'changemepass')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'pillbox')
SUPER_USER_TOKEN = os.environ.get('SUPER_USER_TOKEN', 'changemetoken')
REMOTE_ADDR_HEADER = 'X-Real-IP'


RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

ALLOWED_ROLES = ['admin']

URL_PREFIX = 'api'

tenants = {
    'item_title': 'tenants',
    'pagination': False,
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'tenantid'
    },
    'allowed_roles': ['user','admin'],
    'schema': {
        'tenantid': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'companyname': {
            'type': 'string',
        },
        'companynumber': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'emailaddress': {
            'type': 'string',
            'required': True,
        },
        'secondemailaddress': {
            'type': 'string',
        },
        'identifier': {
            'type': 'string',
        },
        'sex': {
            'type': 'string',
        },
        'initials': {
            'type': 'string',
        },
        'surname': {
            'type': 'string',
        },
        'username': {
            'type': 'string',
        },
        'address': {
            'type': 'string',
        },
        'city': {
            'type': 'string',
        },
        'country': {
            'type': 'string',
        },
        'website': {
            'type': 'string',
        },
        'zipcode': {
            'type': 'string',
        },
        'password': {
            'type': 'string',
        },
        'mobilenumber': {
            'type': 'string',
        },
        'phonenumber': {
            'type': 'string',
        },
        'legalform': {
            'type': 'string',
        },
        'password': {
            'type': 'string',
        },
    },
}

operators = {
    'item_title': 'operators',
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['user','admin'],
    'schema': {
        'name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 64,
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'tokens': {
            'type': 'list',
        },
        'role': {
            'type': 'string',
	        'allowed': ['admin', 'user', 'viewer'],
            'default': 'viewer'
        }
    },
}

logs = {

    'item_title': 'logs',
    'schema': {
        'host': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'hosts',
                'embeddable': True
            }
        },
        'tags': {
            'type': 'list',
        },
        'description': {
            'type': 'string',
        },
        '_remote_addr': {
            'type': 'string',
        },
    },
}
        
hosts = {
    'item_title': 'hosts',
    'pagination': False,
    'additional_lookup': {
        'url': 'regex("[\w\.]+")',
        'field': 'name'
    },
    'versioning': True,
    'allowed_roles': ['user','admin'],
    'schema': {
        'name': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'alias': {
            'type': 'list',
        },
        'tenant': {
            'type': 'string',
            'data_relation': {
                'resource': 'tenants',
                'field': 'tenantid',
                'embeddable': True
            }
        },
        'groups': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'data_relation': {
                    'resource': 'groups',
                    'field': 'name',
                    'embeddable': True
                }
            }
        },
        'vars': {
            'type': 'dict',
            'allow_unknown': True,
            'schema': {
                'parent': {
                  'type': 'string',
                  'data_relation': {
                    'resource': 'hosts',
                    'field': 'name',
                  }
                }
            }
        }
    },
}

groups = {
    'item_title': 'groups',
    'pagination': False,
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'name'
    },
    'allowed_roles': ['user','admin'],
    'schema': {
        'name': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'vars': {
            'type': 'dict',
            'allow_unknown': True,
        },
        'children': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'data_relation': {
                    'resource': 'groups',
                    'field': 'name',
                    'embeddable': True
                }
            }
        },
    }
}

secrets = {
    'item_title': 'secrets',
    'versioning': True,
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['user','admin'],
    'schema': {
        'name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 128,
            'required': True,
            'unique': True,
        },
        'store': {
            'type': 'string',
        },
        'category': {
            'type': 'string',
            'default': 'default',
        },
    }
}

kb = {
    'item_title': 'knowledgebase',
    'versioning': True,
    'schema': {
        'name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 128,
            'required': True,
            'unique': True,
        },
        'store': {
            'type': 'string',
        },
        'parent': {
          'type': 'string',
          'data_relation': {
            'resource': 'kb',
            'field': 'name',
          }
        },
    }
}

DOMAIN = {
    'tenants': tenants,
    'operators': operators,
    'logs': logs,
    'groups': groups,
    'hosts': hosts,
    'secrets': secrets,
    'kb': kb,
}

for resource in DOMAIN:
    DOMAIN[resource]['schema']['_created_by'] = {'type': 'string'}
    DOMAIN[resource]['schema']['_modified_by'] = {'type': 'string'}
    DOMAIN[resource]['schema']['_remote_addr'] = {'type': 'string'}

SWAGGER_INFO = {
    'title': 'Turret ansible inventory API',
    'version': '0.3',
    'description': 'Pillbox our Swiss army knife api',
    'termsOfService': 'Use of this api and the content is at your own risk',
    'contact': {
        'name': 'Vincent van Gelder',
        'url': 'http://www.ixlhosting.nl'
    },
    'license': {
        'name': 'APACHE',
        'url': 'https://github.com/pyeve/eve-swagger/blob/master/LICENSE',
    }
}

SWAGGER_HOST = 'pillbox.example.com'
