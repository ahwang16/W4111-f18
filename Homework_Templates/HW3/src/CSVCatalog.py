import pymysql
import csv
import logging


def run_q(q, args, cnx, fetch=False, commit=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    if commit:
        cnx.commit()
    return result


class ColumnDefinition:
    """
    Represents a column definition in the CSV Catalog.
    """

    # Allowed types for a column.
    column_types = ("text", "number")

    def __init__(self, column_name, column_type="text", not_null=False):
        """

        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types.
        :param not_null: True or False
        """
        # check for invalid column name
        if column_name is None:
            raise ValueError("Column name cannot be None")
        self.column_name = column_name

        # check for invalid column type
        if column_type not in column_types:
            raise ValueError("Column cannot be of type {}".format(column_type))
        self.column_type = column_type

        # check for valid not_null
        if not isinstance(not_null, bool):
            raise ValueError("Not null must be either True or False")
        self.not_null = not_null

    
    def __str__(self):
        return "Column name: {}, type: {}, not_null: {}".format(self.column_name, self.column_type, self.not_null)

    def to_json(self):
        """

        :return: A JSON object, not a string, representing the column and its properties.
        """
        return {
            "column_name":self.column_name,
            "column_type":self.column_type,
            "not_null":self.not_null
        }

        return result


class IndexDefinition:
    """
    Represents the definition of an index.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, index_name, index_type, column_names):
        """

        :param index_name: Name for index. Must be unique name for table.
        :param index_type: Valid index type.
        """
        self.index_name = index_name # check for uniqueness? TODO

        self.index_type = index_type
        if self.index_type not in index_types:
            raise ValueError("Invalid index type: {}".format(self.index_type))

        if len(column_names) == 0:
            raise ValueError("Invalid number of columns")

        self.column_names = column_names


    def to_json(self):
        result = {
            "index_name":self.index_name,
            "type":self.index_type,
            "columns":self.column_names
        }

        return result


class TableDefinition:
    """
    Represents the definition of a table in the CSVCatalog.
    """

    def __init__(self, t_name=None, csv_f=None, column_definitions=None, index_definitions=None, cnx=None, load=False):
        """

        :param t_name: Name of the table.
        :param csv_f: Full path to a CSV file holding the data.
        :param column_definitions: List of column definitions to use from file. Cannot contain invalid column name.
            May be just a subset of the columns.
        :param index_definitions: List of index definitions. Column names must be valid.
        :param cnx: Database connection to use. If None, create a default connection.
        """
        self.cnx = cnx
        self.table_name = t_name
        self.columns = []
        self.indexes = []


        if not load:
            if self.table_name is None or csv_f is None:
                raise ValueError("Invalid name")

            if not self.__is_file__(csv_f):
                raise ValueError("File must exist")

            self.file_name = csv_f

            self.__save_core_definition__()

            if column_definitions is not None:
                for c in column_definitions:
                    self.add_column_definition(c)

            if index_definitions is not None:
                for idx in index_definitions:
                    self.define_index(idx)

        else:
            self.__load_core_definition__()
            self.__load_columns__()
            self.__load_indexes__()


        ### COLUMN DEFINITIONS ###
        # self.column_definitions = column_definitions
        # self.index_definitions = index_definitions


        if cnx is None:
            self.cnx = pymysql.connect(host="localhost", port=3306, dbuser="dbuser", password="dbuser", database="csvdatatable", cursorclass=pymysql.cursors.DictCursor)

    
    def __is_file__(self, fn):
        try:
            with open(fn, "r") as a_file:
                return True
        except:
            return False


    def __load_columns__(self):
        q = "select * from csvtablecolumns where table_name={}".format(self.table_name)
        result = run_q(q, None, self.cnx, fetch=True, commit=True)
        for r in result:
            new_cd = ColumnDefinition(r['column_name'], r['type'], r['not_null']==1)
            self.columns.append(new_cd)
    

    def __save_core_definition__(self):
        # q = "insert into csvtables values({}, {})".format(self.table_name, self.file_name)
        # result = run_q(q, None, self.cnx, fetch=False, commit=True)
        q = "insert into csvtables values(%s, %s)"
        result = run_q(q, (self.table_name, self.file_name), self.cnx, fetch=False, commit=True)


    def __load_core_definition__(self):
        q = "select * from csvtables where name='{}'".format(self.table_name)
        result = run_q(sq, None, self.cnx, fetch=True, commit=True)
        self.file_name = result[0]['path']


    def __str__(self):
        return json.dumps(self.to_json())


    @classmethod
    def load_table_definition(cls, cnx, table_name):
        """

        :param cnx: Connection to use to load definition.
        :param table_name: Name of table to load.
        :return: Table and all sub-data. Read from the database tables holding catalog information.
        """
        pass

    def __load_column_definition__(self, c):
        q = "select * from csvtablecolumns where table_name='{}'".format(self.table_name)
        result = run_q(q, None, self.cnx, fetch=True)
    

    def __save_column_definition__(self, c):
        q = "insert into csvtablecolumns values({}, {}, {}, {})".format(self.table_name, c.column_name, c.column_type, c.not_null)
        result = run_q(q, None, self.cnx, fetch=False, commit=True)
        self.columns.append(c)


    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        self.__save_column_definition(c)
        self.columns.append(c)


    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """
        pass

    def to_json(self):
        """

        :return: A JSON representation of the table and its elements.
        """
        result = {
            "table_name":self.table_name,
            "file_name":self.file_name,
        }

        result['columns'] = []
        for c in self.columns:
            result['columns'].append(c.to_json())

        result['indexes'] = []
        for idx in self.indexes:
            result['indexes'].append(idx.to_json())

        return result



    def define_primary_key(self, columns):
        """
        Define (or replace) primary key definition.
        :param columns: List of column values in order.
        :return:
        """
        pass


    def __save_index_definition__(self, i_name, cols, k):
        q = "insert into csvindexes (table_name, column_name, kind, key_column_order, index_name) values(%s, %s, %s, %s, %s)"
        for i in range(len(cols)):
            v = (self.table_name, cols[i], k, str(i), i_name)
            result = run_q(q, v, self.cnx, fetch=False, commit=True)


    def define_index(self, index_name, columns, kind="index"):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        self.__save_index_definition__(index_name, columns, kind)
        if self.indexes is None:
            self.indexes = []
        new_idx = IndexDefinition(index_name, kind, columns)
        self.indexes.append(new_idx)

    def drop_index(self, index_name):
        """
        Remove an index.
        :param index_name: Name of index to remove.
        :return:
        """
        pass

    def get_index_selectivity(self, index_name):
        """

        :param index_name: Do not implement for now. Will cover in class.
        :return:
        """
        pass

    def describe_table(self):
        """
        Simply wraps to_json()
        :return: JSON representation.
        """
        return self.to_json()


class CSVCatalog:

    def __init__(self, dbhost="localhost", dbport=3306,
                 dbname="csvdatatable", dbuser="dbuser", dbpw="dbuser", debug_mode=None):
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpw = dbpw
        self.debug_mode = debug_mode
        self.cnx = pymysql.connect(host=dbhost, port=dbport, user=dbuser, password=dbpw, database=dbname, cursorclass=pymysql.cursors.DictCursor, charset="utf8mb4")


    def __str__(self):
        return "Host: {}, port: {}, dbname: {}, dbuser: {}, dbpw: {}, debug mode: {}".format(self.dbhost, self.dbport, self.dbname, self.dbuser, self.dbpw, self.debug_mode)


    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        # __init__(self, t_name=None, csv_f=None, column_definitions=None, index_definitions=None, cnx=None)
        table = TableDefinition(table_name, file_name, column_definitions, primary_key_columns, self.cnx)
        return table


    def drop_table(self, table_name):
        pass

    def get_table(self, table_name):
        """
        Returns a previously created table.
        :param table_name: Name of the table.
        :return:
        """
        result = TableDefinition(table_name)














