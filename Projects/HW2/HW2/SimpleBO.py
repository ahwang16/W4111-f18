import pymysql
import json

cnx = pymysql.connect(host='127.0.0.1',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

### HELPER METHODS ###
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


def find_primary_key(table):
    q = "show index from {t} where key_name='PRIMARY'".format(t=table)
    print(q)

    key_col = run_q(q, None, True)

    d = []
    for k in key_col:
        d.append({"COLUMN_NAME":k['Column_name']})

    print(d)

    return d


def find_foreign_key(table):
    q = "SELECT i.TABLE_NAME, i.CONSTRAINT_TYPE, i.CONSTRAINT_NAME, k.REFERENCED_TABLE_NAME, k.REFERENCED_COLUMN_NAME " \
        "FROM information_schema.TABLE_CONSTRAINTS i LEFT JOIN information_schema.KEY_COLUMN_USAGE k ON i.CONSTRAINT_NAME = k.CONSTRAINT_NAME " \
        "WHERE i.CONSTRAINT_TYPE = 'FOREIGN KEY' AND i.TABLE_SCHEMA = DATABASE() AND i.TABLE_NAME = '" + table + "'"
    
    return run_q(q, None, True)


###END HELPER METHODS ###


### BASE RESOURCE (COLLECTION) ###
def insert_primary_key(table, primary_key, r):
    pk = primary_key.split("_")
    key_col = find_primary_key(table)

    for x in range(len(key_col)):
        r[key_col[x]["COLUMN_NAME"]] = pk[x]

    return insert(table, r)


def insert(table, r):
    print(r)
    col = ", ".join(r.keys())
    val = []
    for k in r.keys():
        val.append("'" + str(r[k]) + "'")
    val = ", ".join(val)

    q = "INSERT INTO " + table + " (" + col + ") VALUES (" + val + ")"


    result = run_q(q, None, True)
    return result


### END BASE RESOURCE (COLLECTION) ###


### SPECIFIC RESOURCE (COLLECTION ELEMENT) ###
def find_by_template(table, template, fields=None, limit=None, offset=None):
    wc = template_to_where_clause(template)

    if fields is None:
        q = "select * from " + table + " " + wc
    else:
        q = "select " + fields[0] + " from " + table + " " + wc
    if limit:
        q += " limit {}".format(limit)
    if offset:
        q += " offset {}".format(offset)


    result = run_q(q, None, True)
    return result


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

    for x in range(len(pk)):
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


### END SPECIFIC RESOURCE (COLLECTION ELEMENT) ###


### DEPENDENT RESOURCE/RELATED RESOURCES ###
# /api/<resource>/<primary_key>/<related_resource>[query_expression][fields_expression]
# /api/batting/willite01_BOS_1960_1/people?fields=nameLast,nameFirst,playerID,birthCity,throws
def find_related_resource(resource, primary_key, related_resource, template, fields, limit=None, offset=None):
    pk = primary_key.split("_")
    key_col = find_primary_key(resource)
    print(key_col)

    f = ""
    if fields is not None:
        for field in fields:
            f += field
    else:
        f = "*"

    q = "SELECT " + f + " FROM " + resource + " WHERE "

    for x in range(len(pk)):
        q += key_col[x]["COLUMN_NAME"] + " = " + "'" + pk[x] + "'" + " AND "

    q = q[:-5]

    if limit:
        q += " limit {}".format(limit)
    if offset:
        q += " offset {}".format(offset)

    return run_q(q, None, True)


def find_related_resource2(resource, primary_key, related_resource, template, fields, limit=None, offset=None):
    # primary key values and column names
    pk = primary_key.split("_")
    key_col = find_primary_key(related_resource)

    # list of dicts of info about resource/related_resource, including foreign key
    for_key = find_foreign_key(related_resource)
    print("foreign key",for_key)
    fk = []

    # iterate through each resource to other_resource relationship for find foreign key
    for f in for_key:
        if(f['REFERENCED_TABLE_NAME'].lower() == resource.lower()):
            fk.append(f['REFERENCED_COLUMN_NAME'])

    # get primary key values from resource
    pkd = {}
    for x in range(len(pk)):
        pkd[key_col[x]['COLUMN_NAME'].lower()] = pk[x]
        print(pk[x])

    # foreign key from primary key (might have multiple columns)
    search = {}
    print("fk", fk)
    for f in fk:
        search[f] = [pkd[f]]

    print('search', search)
    
    wc = template_to_where_clause(search)

    f = ""
    if fields is not None:
        for field in fields:
            f += field
    else:
        f = "*"

    q = "SELECT " + f + " FROM " + related_resource + " " + wc
    
    if limit:
        q += " limit {}".format(limit=limit)
    if offset:
        q += " offset {}".format(offset=offset)

    return run_q(q, None, True)


def insert_related_resource(resource, primary_key, related_resource, template, fields):
    pk = primary_key.split("_")
    key_col = find_primary_key(resource)

    for x in range(len(key_col)):
        template[key_col[x]["COLUMN_NAME"]] = pk[x]

    return insert(related_resource, template)


### END DEPENDENT RESOURCE/RELATED RESOURCE ###


### CUSTOM QUERIES ###
def get_teammates(playerid):
    # find all the times this player played
    q = "SELECT playerID,teamID,yearID from appearances {}".format(template_to_where_clause({'playerID':[playerid]}))
    seen = run_q(q, None, True)

    # find all the players on the same team in the same year
    all_players = []
    for player in seen:
        q = "SELECT playerID, teamID, yearID from appearances {}".format(template_to_where_clause({'teamID':[player['teamID']], 'yearID':[player['yearID']]}))
        all_players.append(run_q(q, None, True))

    result = {}
    for player in all_players:
        for d in player:
            p = d['playerID']

            if p not in result.keys():
                result[p] = {'firstYear':d['yearID'], 'lastYear':d['yearID'], 'seasons':1}
            else:
                result[p]['lastYear'] = d['yearID']
                result[p]['seasons'] += 1

    sorted_players = sorted(result)
    final = {}
    for s in sorted_players:
        final[s] = result[s]

    return final


def get_career_stats(playerid):
    # SQL queries
    playerid = [playerid]
    select = "a.playerid, a.teamid, a.yearid, c.g_all, b.hits, b.ABs, a.Assists, a.Errors"
    assists = "playerid, teamid, yearid, cast(sum(A) as SIGNED) as Assists"
    errors = "cast(sum(E) as SIGNED) as Errors"
    fielding = template_to_where_clause({'fielding.playerid':playerid})
    group1 = "group by playerid, teamid, yearid"
    join1 = "join (select playerid, teamid, yearid, cast(sum(AB) as SIGNED) as ABs, cast(sum(H) as SIGNED) as hits from batting"
    join2 = "join (select playerid, teamid, yearid, g_all from appearances {}".format(template_to_where_clause({'appearances.playerid':playerid}))
    batting = template_to_where_clause({'batting.playerid':playerid})
    final = "on a.playerid=b.playerid and a.yearid=b.yearid and a.teamid=b.teamid and a.playerid=c.playerid and a.yearid=c.yearid and a.teamid=c.teamid"

    q = "select {select} from (select {assists}, {errors} from fielding {fielding} {group1}) as a {join1} {batting} {group1}) as b {join2} {group1}) as c {final}".format(select=select, assists=assists, errors=errors, fielding=fielding, group1=group1, join1=join1, batting=batting, join2=join2, final=final)

    return run_q(q, None, True)


def get_roster(args, limit, offset):
    team = args['teamid'][0]
    year = args['yearid'][0]

    select = "b.nameLast, b.nameFirst, a.playerid, a.teamid, a.yearid, a.g_all, c.hits, d.assists, d.errors"
    app = "select playerid, teamid, yearid, g_all from appearances {} group by playerID".format(template_to_where_clause({'appearances.teamid':[team], 'appearances.yearid':[year]}))
    joinb = "select playerid, nameLast, nameFirst from people group by playerID"
    joinc = "select playerid, yearid, cast(sum(AB) as SIGNED) as ABs, cast(sum(H) as SIGNED) as hits from batting {} group by playerID".format(template_to_where_clause({'batting.teamid':[team], 'batting.yearid':[year]}))
    joind = "select playerid, yearid, cast(sum(A) as SIGNED) as assists, sum(E) as errors from fielding {} group by playerID".format(template_to_where_clause({'fielding.teamid':[team], 'fielding.yearid':[year]}))
    final = "on a.playerid=b.playerid and a.playerid=c.playerid and a.playerid=d.playerid"

    q = "SELECT {select} from ({app}) as a JOIN ({joinb}) as b JOIN ({joinc}) as c JOIN ({joind}) as d {final}".format(select=select, app=app, joinb=joinb, joinc=joinc, joind=joind, final=final)

    if limit:
        q += " limit {}".format(limit)
    if offset:
        q += " offset {}".format(offset)

    print(q)
    return run_q(q, None, True)




