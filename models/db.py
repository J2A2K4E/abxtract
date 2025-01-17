# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
from random import randint # To generate random number for unsub_key
import os

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# if request.global_settings.web2py_version < "2.15.5":
#     raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)



if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------

    db = DAL('mysql://william:ilovecs4242@localhost/main?set_encoding=utf8mb4', pool_size=10, migrate=False)

else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*']
# response.generic_patterns = [] 
# if request.is_local and not configuration.get('app.production'):
#     response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
response.static_version = '0.0.7'
STATIC_VERSION = '_0.0.7'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------



# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))
db.define_table(
    auth.settings.table_user_name,
    Field('username',length=32,unique=True,requires=[IS_LENGTH(minsize=4,maxsize=32),IS_NOT_IN_DB(db,'auth_user.username')]), # required
    Field('username_slug',length=255,unique=True,readable=False,writable=False,requires=[IS_SLUG(),IS_NOT_IN_DB(db,'auth_user.username_slug')],compute=lambda row: str(IS_SLUG()(row.username)[0])), # required
    Field('email',length=128,unique=True,requires=IS_EMAIL()), # required
    Field('password','password',length=512,requires =[IS_LENGTH(minsize=4),CRYPT()],readable=False),# required
    Field('registration_key',length=512,writable=False,readable=False,default=''), # required
    Field('reset_password_key',length=512,writable=False,readable=False,default=''), # required
    Field('registration_id',length=512,writable=False,readable=False, default=''), # required
    Field('created_on', 'datetime',default=request.now,writable=False,readable=False), # required
    Field('description',readable=False,writable=False,requires=IS_LENGTH(maxsize=50),default="New member"),
    Field('avatar', 'upload', readable=False, writable=False,
          uploadfolder=os.path.join(request.folder,'avatar'),
          requires=IS_EMPTY_OR(IS_IMAGE(extensions=('bmp','jpg','jpeg','png'),maxsize=(150,150),error_message='Image size must be smaller than 150px x 150px')),
          autodelete=True),
    Field('website',default='',readable=False,writable=False,requires=IS_EMPTY_OR(IS_URL())),
    Field('ethaddress',default='',readable=False,writable=False,requires=IS_LENGTH(maxsize=50)),
    Field('newsletter','boolean',readable=False,writable=False,default=True),
    Field('count_comment_publish','integer',readable=False,writable=False,default=0), # Number of root comments published
    Field('count_comment_vote','integer',readable=False,writable=False,default=0), # Number of upvotes received
    Field('count_follower','integer',readable=False,writable=False,default=0), # Number of followers
    Field('count_following','integer',readable=False,writable=False,default=0), # Number of users that user is following
    Field('count_new_reply','integer',readable=False,writable=False,default=0), # Number of new replies
    Field('unsub_key',readable=False,writable=False,default=''),
    Field('verif_key',readable=False,writable=False,default=''))

auth.define_tables()
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email),IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table


#Auth policy
auth.settings.create_user_groups = False # Cannot create user groups
auth.settings.register_verify_password = False # no need to verify password
auth.settings.registration_requires_verification = False #Require email verification to login next time
auth.settings.registration_requires_approval = False # No approval by admin required
auth.settings.login_after_registration = True # Stayed logged in after registering account
auth.settings.long_expiration = 3000000 # Stay logged in for one month
auth.settings.remember_me_form = False # Remove remember me checkbox

#Define auth tables
auth.define_tables()


# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------

from gluon.scheduler import Scheduler
scheduler = Scheduler(db)

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
