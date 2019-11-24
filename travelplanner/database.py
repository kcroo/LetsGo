from flask_mysqldb import MySQL

class Database():
    def __init__(self, app):
        self.db = MySQL(app)

    # run a single query with optional parameters
    def runQuery(self, query, params=None):
        cursor = self.db.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        self.db.connection.commit()
        return result

    # run multiple insert operations; takes list of queries (no parameters)
    def runMultipleQueries(self, queries):
        cursor = self.db.connection.cursor()

        for q in queries:
            print(q)
            cursor.execute(q)
            result = cursor.fetchall()

        cursor.close()
        self.db.connection.commit()
        return result