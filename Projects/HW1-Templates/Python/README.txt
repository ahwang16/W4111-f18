README.txt

Alyssa Hwang
ahh2143

Databases HW1

OVERVIEW
The implementation for CSVTable and RDBTable are written in 
separate Python files:
CSVTable.py, RDBTable.py
I chose to make a Python class for each and model RDBTable off the sample
CSVTable implementation.

RUNNING THE FILES
You should be able to run the test files from the command line.
To test CSVTable: python3 testsV2.py
To test RDBTable: python3 __________

The RDBTable class takes a dictionary connect_info as one of the parameters
to make a MySQL connection.
connect_info = {
	'host':,
	'user':
	'db':,
	'password':
}
where db is the database name (in this case, Lahman2017).
The full constructor:
__init__(self, table_name, table_file, db_table_name, key_columns, connect_info)
table_name: logical name for the data table


I removed the load and save methods from RDBTable because the SQL server should
take care of loading and updating the tables.

PACKAGE IMPORTS
csv, copy, sys, os, json, pymysql.cursors, operator.

ERROR HANDLING
I check for invalid keys, duplicate inserts, invalid removals
(removing something that doesn't exist or violates the relational database
constraints), and empty values for find operations.

***

CSVTable.py
I used Professor Ferguson's Python template for this class.
- CSVTable takes three parameters: table_name, table_file, key_columns
	table_name (string) is the name of the data table (eg: "people")
	table_file (string) is the name of the data table in memory
	  (eg: "people.csv")
	key_columns (list) is a list of strings (column names/fields)
	  that make up the primary key (eg: ['playerID'])
- The CSVTable class assumes that the CSV tables are in a subdirectory "Data" in the current directory. This can be changed in the hardcoded rel_path variable.
- Along with the three parameters to the constructor, CSVTable has an instance variable called load_data. This is a list of ordered dicts (initialized as empty) that handles loads and saves.
- __str__(self)
	The str dunder allows the user to pretty print the table from load_data
	The user must load the data at least once to print the data table
- load(self)
	This method opens the CSV table (given in the constructor) and writes each row to the list loaded_data as an ordered dict
	The fieldnames and columns are preserved
	The user should call load immediately after initializing a CSVTable:
		csvt = CSVTable('people', 'people.csv', ['playerID'])
		csvt.load()
	Users who make changes to the data (by inserting or deleting entries) should call save() before loading data again to avoid losing information
	The load method raises an error if the primary key is not part of the columns in the CSV to be loaded
- find_by_primary_key(self, string, fields)
	string (list): a list of ordered values that should match the preset primary_key. This class assumes that the elements in this string list correspond in order to the fields listed in key_columns
	fields (list): the columns that should be returned. If None, return all columns.
	This method calls find_by_template to find entries that match the primary key
	It raises an error if any element in string is None or empty
- find_by_template(self, t, fields=None)
	t (dictionary): a dictionary of keys and values that the rows must match
	fields (list, default None): a list of columns to include in the responses. If None, return all
	This method returns all rows that match a template t
	It raises an error if a key that is not in the CSV is searched
- save(self)
	Writes the ordered dicts in loaded_data back to the original CSV file
- insert(self, r)
	r (dictionary): key-value pairs	to be inserted into the CSV
	This method inserts a new row into the table
	This method does not save the new row in storage--the user must call save() to have a fully updated CSV
	This method raises an error if the primary key is not present, an invalid key is used, or the user tries to insert a duplicate primary key
- delete(self, t)
	










Top Ten Hitters
CSV:
RDB:


