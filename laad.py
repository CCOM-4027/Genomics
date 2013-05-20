import MySQLdb as mdb
import sys, getpass, parsingfasta as parse
from settings import default
from settings import databases
from getpass import getpass

def commands(commands,database,user,password=None):
    try:
        connection = mdb.connect('localhost',user,password)
        cursor = connection.cursor()
        #for statement in create(database):
        #    print statement
        #    cursor.execute(statement)
        for command in commands:
            print command
            cursor.execute(command)
        return cursor.fetchall()
    except mdb.Error,e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        if connection:
            connection.close()

def create(database):
    if type(database) is not dict and database in databases:
        statements =["CREATE DATABASE IF NOT EXISTS %s" % database,
                     "USE %s" % database,
                     "GRANT ALL ON %s.* TO %s@'localhost'" % (database,default['username']),]
        database = databases[database]
    else:
        statements=[]
    for table in database:
        columns = ""
        for column, datatype in database[table]:
            columns += ", %s %s" % (column,datatype)
        statements.append("CREATE TABLE IF NOT EXISTS %s(%s)" % (table,columns[2:]))
    return statements

def insert(entry,tables):
    text = ['TEXT','LONGTEXT']
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

def insertEntries(entries,database):
    statements = []
    for entry in entries:
        statements += insert(entry,databases[database])
    return statements

def dropDatabase(database):
    return ["Drop database %s" % database]

########################################

def addEntries(entries, user = default['username'], password = default['password']):
    con = mdb.connect('localhost','laadguest','password', 'genomedb')
    with con:
        cur = con.cursor()
        for entry in entries:
            for command in insert(entry):
                cur.execute(command)

def command(query, user=default['username']):
    sequences = []
    if user == default['username']:
        password = default['password']
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

def do(procedure, user=default['username'], password=default['password']):
    if user == default['username']:
        password = default['password']
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
