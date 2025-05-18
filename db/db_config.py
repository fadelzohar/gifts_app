import pymysql

connection = pymysql.connect(host='localhost', user='root', password='', database='festival')


class DbConnection:
    # protected
    _conn = None
    _cursor = None

    def __init__(self):
        #self._cursor = pymysql.connect(host='localhost',user='root',password='',database='festival2').cursor()

        self._cursor = connection.cursor()

    def test_conn(self):
        if self._cursor:
            return "okk"

#ob = DbConnection()
#ob.test_conn()