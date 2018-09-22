import csv          # Python package for reading and writing CSV files.
import copy         # Copy data structures. 

import sys,os,json

# You can change to wherever you want to place your CSV files.
rel_path = os.path.realpath('./Data')

class CSVTable():

    # Change to wherever you want to save the CSV files.
    data_dir = rel_path + "/"
    load_data = []

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


    def __str__(self):
        '''
        Pretty print the table and state.
        :return: String
        '''
        with open(self.data_dir + self.table_file, "r") as infile:
            pp = ""
            for line in infile:
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
                
                
    def find_by_primary_key(self, string, fields):
        # Input is a string of values.
        # Fields is a list defining which of the fields from the row/tuple you want.
        # Output is the single dictionary in the table that is the matching result, or null/None.
        if(len(string)!=len(self.key_columns)):
            raise ValueError("The length of search values doesn't match the length of the fields")
        print(string, self.key_columns)
        save = None
        result = None
        for row in self.load_data:
            count = 0
            for x in range(0, len(self.key_columns)):
                if row[self.key_columns[x]] != string[x]:
                    break
                if row[self.key_columns[x]] == string[x]:
                    count += 1
                if count == (len(self.key_columns) - 1):
                    save = row
            if save is not None:
                break
        
        if fields is None:
            return save
        
        if save is not None:
            result = {}
            for f in fields:
                result[f] = save[f]
        return result
    
    
    def find_by_template(self, t, fields=None):
        '''
        Return a table containing the rows matching the template and field selector.
        :param t: Template that the rows much match.
        :param fields: A list of columns to include in responses.
        :return: CSVTable containing the answer.
        '''
        return self.find_by_primary_key(t, fields)
    
    
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
        for line in self.load_data:
            count = 0
            for key in r.keys():
                if line[key] != r[key]:
                    break
                if line[key] == r[key]:
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
        while (delete_this):
            self.load_data.remove(delete_this)
            delete_this = self.find_by_template(t)
        
        return None