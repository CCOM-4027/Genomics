import MySQLdb as mdb
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

    
def Gquery(query):

    """ 
    print "Give desired username and password"
    user=raw_input("User:")
    password = getpass.getpass()
    """
    SeqEntry sequences

    try:
        #Connecting
        con = mdb.connect('localhost', 'guest', 'password', 'genomedb')
        cur = con.cursor()
        #Query
        #print "Please insert desired query"
        #query=raw_input("Query:"")

        cur.execute(query)
        rows=cur.fetchall()
        for row in rows:
            if seqID in query:
                for seq in sequences:
                    seq.id = row
            elif seqHash in query:
                for seq in sequences:
                    seq.hash = row

       except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:
        if con:
            con.close()

    return sequences

        