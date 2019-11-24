from flask_mysqldb import MySQL

class Database():
    def __init__(self, app):
        self.db = MySQL(app)

    def runQuery(self, query, params=None):
        cursor = self.db.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        self.db.connection.commit()
        return result