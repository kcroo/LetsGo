import os, secrets 

class Config(object):
    SECRET_KEY = secrets.token_hex(16)
    MYSQL_HOST = "oniddb.cws.oregonstate.edu"
    MYSQL_USER = "corraok-db"
    MYSQL_PASSWORD = "oY1sLTVf7C3Z26iE"
    MYSQL_DB = "corraok-db"
