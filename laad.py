import MySQLdb as mdb
import sys, getpass, parsingfasta as parse
from settings import guest

def create(tables):
    statements=[]
    for table in tables:
        columns = ""
        for column in tables[table]:
            columns += ", %s %s" % column
        statements.append("CREATE TABLE %s(%s)" % (table,columns[2:]))
    return statements

def insert(entry):
    text = ['TEXT','LONGTEXT']
    from settings import tables
    statements = []
    for table in tables:
        columns, values = "",""
        for column, type in tables[table]:
            if column in entry:
                columns += ", %s" % column
                values += (", \"%s\"" if type in text else ", %s") % entry[column]
        if columns:
            statements.append("INSERT INTO %s(%s) VALUES (%s);" % (table,columns[2:],values[2:]))
    return statements

def addEntries(entries, user = guest['username'], password = guest['password']):
    con = mdb.connect('localhost','laadguest','password', 'genomedb')
    with con:
        cur = con.cursor()
        for entry in entries:
            for command in insert(entry):
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
        sequences = cur.fetchall()
        #for row in rows: sequences.append(row)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    
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
