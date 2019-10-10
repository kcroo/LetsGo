#############################################################################
# Author: Kirsten Corrao
# Date: 10/1/2019
# Class: CS340
# Sources:
#   https://github.com/knightsamar/CS340_starter_flask_app
#   https://www.youtube.com/watch?v=Z1RJmh_OqeA
#   https://flask.palletsprojects.com/en/1.0.x/
##############################################################################

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

# start flask app
app = Flask(__name__)

# log in info for database (can put in own file later)
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_corraok"
app.config["MYSQL_PASSWORD"] = "1298"
app.config["MYSQL_DB"] = "cs340_corraok"

db = MySQL(app)

# index route
@app.route('/')
def index():
    return render_template("index.html", result="Hello, world!!!")

if __name__ == "__main__":
    app.run(debug=True)