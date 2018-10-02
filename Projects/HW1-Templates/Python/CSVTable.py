import csv          # Python package for reading and writing CSV files.
import copy         # Copy data structures. 

import sys,os,json

# You can change to wherever you want to place your CSV files.
rel_path = os.path.realpath('./Data')

class CSVTable():

    # Change to wherever you want to save the CSV files.
    data_dir = rel_path + "/"
    

    def __init__(self, table_name, table_file, key_columns):
        '''
        Constructor
        :param table_name: Logical names for the data table.
        :param table_file: File name of CSV file to read/write.
        :param key_columns: List of column names the form the primary key.

        '''
        self.table_name = table_name
        self.table_file = table_file
        self.key_columns = key_columns
        self.load_data = []


    def __str__(self):
        '''
        Pretty print the table
        :return: String
        '''
        pp = ""
        for line in self.load_data:
            for word in line.split(","):
                pp += word + "\t"
            pp += "\n"
        
        return pp 


    def load(self):
        '''
        Load information from CSV file.
        :return: None
        '''
        with open(self.data_dir + self.table_file, "r") as infile:
            reader = csv.DictReader(infile, delimiter=",", quotechar='"')
            for row in reader:
                self.load_data.append(row)
            for field in self.key_columns:
                if field not in reader.fieldnames:
                    raise ValueError(field + "primary key not a subset of data table fields")
                
    
    def find_by_primary_key(self, string, fields):
        # Input is a string of values.
        # Fields is a list defining which of the fields from the row/tuple you want.
        # Output is the single dictionary in the table that is the matching result, or null/None.
        
        t = {}
        
        count = 0
        for s in string:
            if s is None or s == "":
                raise KeyError("Invalid value")
            t[self.key_columns[count]] = s
            count += 1
            
        return self.find_by_template(t, fields)
    
    
    def find_by_template(self, t, fields=None):
        '''
        Return a table containing the rows matching the template and field selector.
        :param t: Template that the rows much match.
        :param fields: A list of columns to include in responses.
        :return: CSVTable containing the answer.
        '''
        save = []
        result = []
        
        for row in self.load_data:
            count = 0
            for field in t.keys():
                if field not in row.keys():
                    raise ValueError("Invalid key")
                if row[field] != t[field]:
                    break
                if row[field] == t[field]:
                    count += 1
                if count == (len(t.keys())):
                    save.append(row)

        if fields is None:
            return save

        r = {}
        for s in save:
            for f in fields:
                r[f] = s[f]
            result.append(r)
            r = {}
        
        return result    
    
    def save(self):
        '''
        Write updated CSV back to the original file location.
        :return: None
        '''
        with open(self.data_dir + self.table_file, "r") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

        with open(self.data_dir + self.table_file, "w") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.load_data:
                writer.writerow(row)
                
        return None
        
        
    def insert(self, r):
        '''
        Insert a new row into the table.
        :param r: New row.
        :return: None. Table state is updated.
        '''

        # Check for primary key
        for k in self.key_columns:
            if k not in r.keys():
                raise ValueError("Missing primary key")

        for k in r.keys():
            if k not in self.load_data[1].keys():
                raise ValueError("Invalid field")

        for x in range(len(self.load_data)):
            count = 0
            for key in r.keys():
                if self.load_data[x][key] != r[key]:
                    break
                if self.load_data[x][key] == r[key]:
                    count += 1
                if count == (len(r.keys()) - 1):
                    raise ValueError("Duplicate primary key")
                
        self.load_data.append(r)
        return None
    
    
    def delete(self, t):
        '''
        Delete all tuples matching the template.
        :param t: Template
        :return: None. Table is updated.
        '''
        delete_this = self.find_by_template(t)
        if delete_this is None:
            raise ValueError("Template not found")
        count = 0
        while (delete_this):
            self.load_data.remove(delete_this.pop())
        
        return None










