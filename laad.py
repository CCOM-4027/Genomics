import MySQLdb as mdb
import sys, getpass, parsingfasta as parse
from settings import guest

def addEntries(entries, user = 'laadguest'):
    con = mdb.connect('localhost','laadguest','password', 'genomedb')
    with con:
        cur = con.cursor()
        for entry in entries:
            for command in parse.insert(entry):
                cur.execute(command)

def command(query, user=guest['username']):
    sequences = []
    if user == guest['username']:
        password = guest['password']
    else:
        password = getpass.getpass("Please, enter sql password for user %s:" % user)
    try:
        con = mdb.connect('localhost', user, password, 'genomedb')
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            sequences.append(row)
    finally:
        if con:
            con.close()
    return sequences

def do(procedure, user=guest['username'], password=guest['password']):
    if user == guest['username']:
        password = guest['password']
    else:
        password = getpass.getpass("Please, enter sql password for user %s:" % user)
    
    try:
        connection = mdb.connect('localhost', user, password, 'genomedb')
        cursor = connection.cursor()
        result = procedure(cursor)
        connection.close()
        return result

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
