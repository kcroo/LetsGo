import os, secrets 

class Config(object):
    SECRET_KEY = secrets.token_hex(16)
    MYSQL_HOST = "your_host_here"
    MYSQL_USER = "your_username_here"
    MYSQL_PASSWORD = "your_password_here"
    MYSQL_DB = "your_database_here"
