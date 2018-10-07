import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""

    if t is None:
        return s

    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s;

    return s


def insert_primary_key(table, primary_key, r):
    pk = primary_key.split("_")
    print("pk: ", pk)
    key_col = find_primary_key(table)

    for x in range(len(key_col)):
        r[key_col[x]["COLUMN_NAME"]] = [pk[x]]

    return insert(table, r)


def insert(table, r):
    col = ", ".join(r.keys())
    val = []
    for k in r.keys():
        val.append("'" + str(r[k][0]) + "'")
    val = ", ".join(val)

    q = "INSERT INTO " + table + " (" + col + ") VALUES (" + val + ")"
    print(q)


    result = run_q(q, None, True)
    return result


def find_by_template(table, template, fields=None):
    wc = template_to_where_clause(template)

    if fields is None:
        q = "select * from " + table + " " + wc
    else:
        q = "select " + fields[0] + " from " + table + " " + wc
    result = run_q(q, None, True)
    return result


def find_primary_key(table):
    q = "SELECT column_name FROM information_schema.columns WHERE table_name='" + table + "' AND COLUMN_KEY='PRI'"
    key_col = run_q(q, None, True)

    return key_col


def find_by_primary_key(table, primary_key, fields):
    f = ""
    if fields is not None:
        for field in fields:
            f += field
    else:
        f = "*"

    q = "SELECT " + f + " FROM " + table + " WHERE "

    pk = primary_key.split("_")
    key_col = find_primary_key(table)

    for x in range(len(key_col)):
        q += key_col[x]["COLUMN_NAME"] + " = " + "'" + pk[x] + "'" + " AND "

    q = q[:-5]

    return run_q(q, None, True)


def delete(table, primary_key):
    delete_this = []

    pk = primary_key.split("_")
    key_col = find_primary_key(table)

    for x in range(len(key_col)):
        delete_this.append(key_col[x]["COLUMN_NAME"] + "='" + str(pk[x]) + "'")
    
    delete_this = " AND ".join(delete_this)

    q = "DELETE FROM " + table + " WHERE " + delete_this + ";"

    return run_q(q, None, True)






