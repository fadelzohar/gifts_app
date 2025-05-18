from db_config import *

class DisplayEngineNoCondition(DbConnection):
    # protected
    _table = None
    def __init__(self,table) -> None:
        self._table = table
        DbConnection.__init__(self)


    def display(self) -> tuple:
        query = "SELECT * FROM {table}".format(table = self._table)    
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        return fetch

'''
column config attributes data type as
-- name
-- value
'''
class ColumnConfig:

    #protected
    _name = None
    _value = None

    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name


'''
table config attribute data type as 
-- name
'''
class Table:

    #protected
    _name = None

    def __init__(self,name):
        self._name = name

    @property
    def name(self):
        return self._name

class EngineConfigDb(DbConnection):

    #protected
    _table = None
    def __init__(self, table: Table):
        super().__init__()
        self._table = table




class Engine1Condition(EngineConfigDb):
    # protected
    _column = None
    _table = None
    # constructor inheritance and declaration
    def __init__(self, table: Table, column_1: ColumnConfig) -> None:
        super().__init__(table)
        self._column = column_1
        self._table = table


    def display(self) -> tuple:
        query = "SELECT * FROM '{table}' WHERE '{column}'='{value}'".format(
            table=self._table.name,
            column=self._column._name,
            value=self._column._value
        )
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        return fetch
    




class Engine2Condition(DisplayEngine):
    # protected 
    _column_2 = None
    _column_2_value = None
    _table = None
    # constructor inheritance from display engine class
    def __init__(self,table: Table,column_1: ColumnConfig column_2, column_2_value ) -> None:
        DisplayEngine.__init__(self,table, column_1, column_1_value )
        self._column_2 = column_2
        self._column_2_value = column_2_value
        self._table = table.name



    def display(self) -> tuple:
        query = "SELECT * FROM '{table}' WHERE '{column_1} = '{column_1_value} AND '{column_2}' = '{column_2_value}'".format(
            table = self._table,
            column_1 = self._column,
            column_1_value = self._column_value,
            column_2 = self._column_2,
            column_2_value = self._column_2_value
        )    
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        return fetch

    def update(self):
        query = "UPDATE 'table' SET 'table' "

class UpdateEngine1Condition(DisplayEngine):
    #protected
    _set_column = None
    _set_column_value = None
    def __int__(self,set_column: str, set_column_value: str,table,column_1, column_1_value, column_2, column_2_value ):
        super.__init__(table,column_1, column_1_value, column_2, column_2_value )
        self._set_column = set_column
        self._set_column_value = set_column_value


    def update(self) -> None:
        update_query = "UPDATE '{table}' SET '{set_column}'='{set_column_value}' WHERE '{column_1}'='{column_1_value}'".format(
            table=self._table, 
            set_culomn=self._set_culomn,
            set_culomn_value=self._set_culomn_value,
            culomn_1=self._culomn,
            culomn_1_value=self._culomn_value
        )     
        self._cursor.execute(update_query)
        connection.commit()
        connection.close()

class update_engine_2_changes():
