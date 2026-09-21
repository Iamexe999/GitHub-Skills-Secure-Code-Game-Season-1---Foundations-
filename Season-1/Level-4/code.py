'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import sqlite3
import os
import re
import math
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"])
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class Connect(object):

    # helper function creating database with the connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            # creates a dummy database inside the folder of this challenge
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            # checks if tables already exist, which will happen when re-running code
            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()

            # if tables do not exist, create them and insert dummy data
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')

                # inserts dummy data to the 'stocks' table, representing average price on date
                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

class DB_CRUD_ops:
    def _connect(self):
        Create()
        return sqlite3.connect(os.path.join(os.path.dirname(__file__), 'level-4.db'))

    def get_stock_info(self, stock_symbol):
        # Display text preserves the exercise UI; it is NEVER executed as SQL.
        display = "SELECT * FROM stocks WHERE symbol = '{0}'".format(stock_symbol)
        res = "[METHOD EXECUTED] get_stock_info\n[QUERY] " + display + "\n"
        if any(char in stock_symbol for char in ";%&^!#-'"):
            return res + "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
        con = self._connect()
        try:
            for row in con.execute("SELECT * FROM stocks WHERE symbol = ?", (stock_symbol,)):
                res += "[RESULT] " + str(row)
            return res
        finally:
            con.close()

    def get_stock_price(self, stock_symbol):
        display = "SELECT price FROM stocks WHERE symbol = '" + stock_symbol + "'"
        res = "[METHOD EXECUTED] get_stock_price\n[QUERY] " + display + "\n"
        con = self._connect()
        try:
            for row in con.execute("SELECT price FROM stocks WHERE symbol = ?", (stock_symbol,)):
                res += "[RESULT] " + str(row) + "\n"
            return res
        finally:
            con.close()

    def update_stock_price(self, stock_symbol, price):
        if not isinstance(price, float) or not math.isfinite(price) or price < 0:
            raise ValueError("ERROR: stock price must be a finite nonnegative float")
        display = "UPDATE stocks SET price = '%d' WHERE symbol = '%s'" % (price, stock_symbol)
        con = self._connect()
        try:
            con.execute("UPDATE stocks SET price = ? WHERE symbol = ?", (price, stock_symbol))
            con.commit()
            return "[METHOD EXECUTED] update_stock_price\n[QUERY] " + display + "\n"
        finally:
            con.close()

    @staticmethod
    def _read_requests(query):
        # Compatibility with the two original read-only examples, not arbitrary SQL.
        # Parse the ENTIRE request before executing any fixed statement.
        requests = []
        for part in query.split(';'):
            if not part.strip():
                continue
            match = re.fullmatch(
                r"SELECT (price|\*) FROM stocks WHERE symbol = '([A-Za-z0-9.]+)'",
                part.strip(), re.IGNORECASE)
            if match is None:
                raise ValueError("Only stock-price and stock-info lookups are supported")
            requests.append((part, match[1].lower(), match[2]))
        return requests

    @staticmethod
    def _read_rows(con, column, symbol):
        if column == 'price':
            return con.execute("SELECT price FROM stocks WHERE symbol = ?", (symbol,)).fetchall()
        return con.execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,)).fetchall()

    def exec_multi_query(self, query):
        requests = self._read_requests(query)
        con = self._connect()
        try:
            res = "[METHOD EXECUTED] exec_multi_query\n"
            for original, column, symbol in requests:
                res += "[QUERY]" + original + "\n"
                for row in self._read_rows(con, column, symbol):
                    res += "[RESULT] " + str(row) + " "
            return res
        finally:
            con.close()

    def exec_user_script(self, query):
        requests = self._read_requests(query)
        con = self._connect()
        try:
            res = "[METHOD EXECUTED] exec_user_script\n[QUERY] " + query + "\n"
            for _, column, symbol in requests:
                for row in self._read_rows(con, column, symbol):
                    res += "[RESULT] " + str(row)
            return res
        finally:
            con.close()
