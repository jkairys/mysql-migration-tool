import mysql.connector
import logging
logger = logging.getLogger("migrate.database")


class Database:
    _connection = None
    _connected = False

    def __init__(self, host="localhost", port=3306, username=None, password=None):
        try:
            self._connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                passwd=password,
            )
            self._connected = True
        except Exception as e:
            logger.exception("Unable to connect to database")
            self._connected = False

    def cursor(self):
        return self._connection.cursor()

    def database(self):
        return self._connection

    def execute(self, sql, bvs=None):
        cursor = self._connection.cursor()
        try:
            ret = cursor.execute(sql, bvs)
        except Exception as e:
            logger.error(f"Error executing sql '{sql}' using bind variables {bvs}")
            raise e

    def query(self, sql, bvs=None):
        cursor = self._connection.cursor()
        try:
            ret = cursor.execute(sql, bvs)
        except Exception as e:
            logger.error(f"Error running query '{sql}' using bind variables {bvs}")
            raise e

        keys = [d[0] for d in cursor.description]
        rows = cursor.fetchall()

        result = list()
        for r in rows:
            row = dict(zip(keys, r))
            result.append(row)

        return result

    def commit(self):
        self._connection.commit()

    def connected(self):
        return self._connected
