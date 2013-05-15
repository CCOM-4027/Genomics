import MySQLdb as mdb
from parsingfasta import seqEntry
import sys
import getpass

#generateCommands:sequence->string,tuple

def addseqs(sequences):
    def aux(sql):
        try:
        #Connecting
            for sequence in sequences:
                for command in sequence.commands():
                    print command
                    sql.execute(command, sequence.data)         
                    
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])

    return aux

def query(query, user='laadguest'):
    sequences = []
    if user == 'laadguest':
        password = 'password'
    else:
        password = getpass.getpass("Please, enter sql password for user %s:" % user)
    try:
        con = mdb.connect('localhost', user, password, 'genomedb')
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        print rows
        for row in rows:
            sequences.append(seqEntry(row["seqID"],row["seqHash"]))

    finally:
        if con:
            con.close()
    return sequences

def do(procedure,user='laadguest',password='password',database='genomedb'):
    if user == 'laadguest':
        password = 'password'
    else:
        password = getpass.getpass("Please, enter sql password for user %s:" % user)
    
    try:
        connection = mdb.connect('localhost', user, password, 'genomedb')
        cursor = connection.cursor(mdb.cursors.DictCursor)
        result = procedure(cursor)
        connection.close()
        return result

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
