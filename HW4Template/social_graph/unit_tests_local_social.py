import sys
sys.path.append('..')
import social_graph.fan_comment_template as fct
import utils.utils as ut
import json
import py2neo
import pymysql

cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2017',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

fg = fct.FanGraph(auth=('neo4j','password'),
                              host="localhost",
                              port=7687,
                              secure=False)

ut.set_debug_mode(True)


def load_players():

    q = "SELECT playerID, nameLast, nameFirst FROM People where " + \
        "exists (select * from appearances where appearances.playerID = people.playerID and yearID >= 2017)"

    curs = cnx.cursor()
    curs.execute(q)

    r = curs.fetchone()
    cnt = 0
    while r is not None:
        print(r)
        cnt += 1
        r = curs.fetchone()
        if r is not None:
            p = fg.create_player(player_id=r['playerID'], last_name=r['nameLast'], first_name=r['nameFirst'])
            print("Created player = ", p)

    print("Loaded ", cnt, "records.")


def load_teams():

    q = "SELECT teamid, name from teams where yearid >= 2017"

    curs = cnx.cursor()
    curs.execute(q)

    r = curs.fetchone()
    cnt = 0
    while r is not None:
        print(r)
        cnt += 1
        r = curs.fetchone()
        if r is not None:
            p = fg.create_team(team_id=r['teamid'], team_name=r['name'])
            print("Created team = ", p)

    print("Loaded ", cnt, "records.")


def load_appearances():

    q = "SELECT distinct playerid, teamid, g_all as games from appearances where yearid >= 2017"

    curs = cnx.cursor()
    curs.execute(q)

    r = curs.fetchone()
    cnt = 0
    while r is not None:
        print(r)
        cnt += 1
        r = curs.fetchone()
        if r is not None:
            try:
                p = fg.create_appearance(team_id=r['teamid'], player_id=r['playerid'])
                print("Created appearances = ", p)
            except Exception as e:
                print("Could not create.")

    print("Loaded ", cnt, "records.")


def load_follows_fans():
    fg.create_fan(uni="js1", last_name="Smith", first_name="John")
    fg.create_fan(uni="ja1", last_name="Adams", first_name="John")
    fg.create_fan(uni="tj1", last_name="Jefferson", first_name="Thomas")
    fg.create_fan(uni="gw1", last_name="Washing", first_name="George")
    fg.create_fan(uni="jm1", last_name="Monroe", first_name="James")
    fg.create_fan(uni="al1", last_name="Lincoln", first_name="Abraham")

    fg.create_follows(follower="gw1", followed="js1")
    fg.create_follows(follower="tj1", followed="gw1")
    fg.create_follows(follower="ja1", followed="gw1")
    fg.create_follows(follower="jm1", followed="gw1")
    fg.create_follows(follower="tj1", followed="gw1")
    fg.create_follows(follower="al1", followed="jm1")


def create_supports():

    fg.create_supports("gw1", "WAS")
    fg.create_supports("ja1", "BOS")
    fg.create_supports("tj1", "WAS")
    fg.create_supports("jm1", "NYA")
    fg.create_supports("al1", "CHA")
    fg.create_supports("al1", "CHN")


def test_create_comment():
    t = fg.get_team('BOS')
    f = fg.get_fan('al1')
    p = fg.get_player('pedrodu01')
    c = "Awesome"
    pid = p['player_id']
    tid = t['team_id']
    fid = f['uni']
    # print(pid, tid, fid)
    c = fg.create_comment(fid, c, tid, pid)
    # print(c)


def test_create_sub_comment():
    # f50a9718-8df5-4bac-af24-f6c99749e8a5
    c = fg.get_comment("3e8b7c14-0cc6-458f-8625-3d439f0388fe")
    m = "Totally agree!"
    # f50a9718-8df5-4bac-af24-f6c99749e8a5
    r = fg.create_sub_comment('al1', "3e8b7c14-0cc6-458f-8625-3d439f0388fe", m)



if __name__ == "__main__":
    load_players()
    load_teams()
    load_appearances()
    load_follows_fans()
    create_supports()
    test_create_comment()
    test_create_sub_comment()
  






