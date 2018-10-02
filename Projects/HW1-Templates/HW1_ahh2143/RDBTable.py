import csv, json, pymysql.cursors, os, operator

rel_path = os.path.realpath('./Data')

class RDBTable():
    
    data_dir = rel_path + "/"
    load_data = []
    
    def __init__(self, table_file, db_table_name, key_columns, connect_info):
        '''
        Constructor
        '''
        self.table_file = table_file
        self.db_table_name = db_table_name
        self.key_columns = key_columns
        self.cnx = pymysql.connect(host=connect_info['host'],
                                      user=connect_info['user'],
                                      password=connect_info['password'],
                                      db=connect_info['db'],
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
        
        
    def run_q(self, q, fetch=False):
        '''
        :param q: the query string to run
        :param fetch: True if this query produces a result and the function should perform and return fetchall()
        '''
        cursor = self.cnx.cursor()
        cursor.execute(q)
        if fetch:
            result = cursor.fetchall()
            return result
        
        
    def get_column_names(self):
        q = "show columns from " + self.table_file
        result = self.run_q(q, True)
        result = [r['Field'] for r in result]
        return list(result)
    
    
    def get_no_of_rows(self):
        q = "select count(*) as count from " + self.table_file
        result = self.run_q(q, True)
        result = result[0]['count']
        return result
    
    
    def get_key_columns(self):
        q = "show keys from " + self.table_file
        result = self.run_q(q, True)
        keys = [(r['Column_name'], r['Seq_in_index']) for r in result]
        keys = sorted(keys, key=operator.itemgetter(1))
        keys = [k[0] for k in keys]
        return keys
        
    
    def __str__(self):
        result = "Table name: {}, No of rows: {}, Key columns: {}"
        row_count = None
        columns = None
        key_names = None
        
        if self.table_file:
            row_count = self.get_no_of_rows()
            columns = self.get_column_names()
            key_names = self.get_key_columns()
        else:
            rows = "DERIVED"
            columns = "DERIVED"
            key_names = "DERIVED"
            
        if self.table_file is None:
            self.table_file = "DERIVED"
            
        result = result.format(self.table_file, row_count, key_names) + "\n"
        result += "Column names: " + str(columns)
        
        q_result = []
        if row_count != "DERIVED":
            q_result = self.find_by_template(None, None)
        
        for r in q_result:
            result += str(r) + "\n"
            
        return result
    
    
    def template_to_where(self, t):
        s = ""
        for (k, v) in t.items():
            if s!= "":
                s += " AND "
            s += k + "='" + str(v) + "'"
            
        if s != "":
            s = "WHERE " + s
            
        return s
    
    
    def find_by_primary_key(self, values, fields):
        t = {}
        for x in range(len(values)):
            t[self.key_columns[x]] = values[x]
        return self.find_by_template(t, fields)
    
    
    def find_by_template(self, t, fields):
        cursor = self.cnx.cursor()
        q = ""
        if t is None:
            q = "SELECT * FROM " + self.table_file
        else:
            w = self.template_to_where(t)
            if fields is None:
                q = "SELECT * FROM " + self.table_file + " " + w + ";"
            else:
                f = ", ".join(fields)
                q = "SELECT " + f + " FROM " + self.table_file + " " + w + ";"
            
        print("Query = ", q)
        try:
            cursor.execute(q)
            r = cursor.fetchall()
            return r
        except:
            raise ValueError("Invalid search")


    def insert(self, r):
        cursor = self.cnx.cursor()

        col = ", ".join(r.keys())
        val = []
        for k in r.keys():
            val.append("'" + str(r[k]) + "'")
        val = ", ".join(val)

        q = "INSERT INTO " + self.table_file + " (" + col + ") VALUES (" + val + ")"
        
        try:
            cursor.execute(q)
            self.cnx.commit()
        except pymysql.IntegrityError:
            print("Invalid insert")
            
        
        return None

        
    def delete(self, t):
        delete_this = []
        for (f, v) in t.items():
            delete_this.append(f + "='" + str(v) + "'")
        delete_this = " AND ".join(delete_this)
        
        cursor = self.cnx.cursor()
        q = "DELETE FROM " + self.table_file + " WHERE " + delete_this + ";"
        print("Query: " + q)

        try:
            cursor.execute(q)
            self.cnx.commit()
        except:
            print("Invalid delete")
        
        return None

    
    def ten_greatest_hitters(self):
        q = "SELECT \
                Batting.playerID, \
                (SELECT People.nameFirst FROM People WHERE People.playerID=Batting.playerID) as first_name, \
                (SELECT People.nameLast FROM People WHERE People.playerID=Batting.playerID) as last_name, \
                sum(Batting.h)/sum(batting.ab) as career_average, \
                sum(Batting.h) as career_hits, \
                sum(Batting.ab) as career_at_bats,\
                min(Batting.yearID) as first_year, \
                max(Batting.yearID) as last_year \
                FROM \
                Batting \
                GROUP BY \
                playerId \
                HAVING \
                career_at_bats > 200 AND last_year >= 1960 \
                ORDER BY \
                career_average DESC \
                LIMIT 10;"
        cursor = self.cnx.cursor()
        cursor.execute(q)
        r = cursor.fetchall()
        return r