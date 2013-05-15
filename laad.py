import MySQLdb as mdb
from parsingfasta import SeqEntry
import sys
import getpass

def Gdataentry(sequences):
    """
    print "Give desired username and password"
    user=raw_input("User:")
    password = getpass.getpass()
    """
    try:
        #Connecting
        con = mdb.connect('localhost', 'guest', 'password', 'genomedb')
        cur = con.cursor()
        #Adding
        for seq in sequences:
            cur.execute("INSERT INTO Sequences(seqID, seqHash) VALUES (%s, %s)", (seq.id, seq.hash))

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:
        if con:
            con.close()

def query(query, user='laadguest'):
    if user == 'laadguest':
        password = 'password'
    else:
        password = getpass.getpass("Please, enter sql password for user %s:" % user)

   sequences = []
   try:
       con = mdb.connect('localhost', user, password, 'genomedb')
       cur = con.cursor(mdb.cursors.DictCursor)
       cur.execute(query)
       rows = cur.fetchall()
       for row in rows:
           sequences.append(SeqEntry(row["seqID"],row["seqHash"]))
   except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
       
   finally:
       if con:
	       con.close()
   return sequences
