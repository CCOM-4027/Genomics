#make user test
import MySQLdb as mdb
import sys
import getpass
"""
Function definitions:
	1)createDatabase()
		Precondition: MYSQL installed
		Postcondition: Database created, Tables created
	2)createUserDB()
		Precondition: Database and Tables have been created
		Postcondition: New user in the database with acces to tables
    3)dropDatabase()
        Precondition: Database has been created
		Postcondition: Database Droped
    4)dropUser()
        Precondition: Users have been created
        Postcondition: Specified user droped
 """
tables = ["CREATE TABLE Sequences(seqID TEXT, seqHash TEXT)", "CREATE TABLE Reeds(sampleID INT, seqHash TEXT)", "CREATE TABLE Assembled(Assembler TEXT, sampleID TEXT, seqID TEXT, seqHash TEXT)", "CREATE TABLE Align(aligner TEXT, sourceID TEXT, targetID TEXT, targetHash TEXT)" ]

#Create database
def createDatabase(tables):
    #Connecting as root
    print"\nThis will create tables automatically\n\nPlease insert root password"
    password=getpass.getpass()

    try:
        #Connection
        con = mdb.connect('localhost', 'root', password)
        cur = con.cursor()
        #Database creation
        cur.execute("CREATE DATABASE genomedb")

        #Table creation
        cur.execute("Use genomedb")
        #cur.execute("CREATE TABLE Reads(sample_ID INT)")
        for table in tables:
            cur.execute(table)
        print"Tables Created!"

        cur.execute("CREATE USER 'laadguest'@'localhost' IDENTIFIED BY 'password'")
        cur.execute("GRANT ALL ON genomedb.* TO 'laadguest'@'localhost'")

        print "Created guest user"

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:
        if con:
            con.close()

#Create user
def createUserDB():

    #Connecting as root
    print"\nPlease insert root password"
    password=getpass.getpass()
    try:
        #Connection
        con = mdb.connect('localhost', 'root', password);
	cur = con.cursor()
        #New user
        print"\nInsert new user name and password"
	newUser=raw_input("Username:")

	passError=True
	while passError:
           newPassword=raw_input("Password:")
           checkPass=raw_input("Retype Password:")
           if checkPass!=newPassword:
               print "Error try again"
           else:
               passError = False

        #mysql execution
        cur.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s", (newUser, newPassword))
        cur.execute("GRANT ALL ON genomedb.* TO %s@'localhost'", newUser)

	print"Done!"


    except mdb.Error, e:
  
        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:    
        
        if con:    
            con.close()

def dropDatabase():
    #Connecting as root
    print"\nThis will delete the database completely\n\nPlease insert root password"
    password=getpass.getpass()

    try:
        #Connection
        con = mdb.connect('localhost', 'root',
        password);
        cur = con.cursor()
        #Database Drop
        cur.execute("Drop database genomedb")
	print "Done!"

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:

        if con:
            con.close()

def dropUser():
    #Connecting as root
    print"\nThis will delete the specified user\n\nPlease insert root password"
    password=getpass.getpass()
    try:
        #Connection
        con = mdb.connect('localhost', 'root',
        password);
        cur = con.cursor()
        #User Drop()
        print "Please indicate the user you which to delete"
	user = raw_input()
        cur.execute("Drop User %s@localhost",(user))
        print "User deleted"

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        if con:
            con.close()

def tableManagement():

    try:
        #Connection
        con = mdb.connect('localhost', 'laadguest', 'password', 'genomedb')
        cur = con.cursor()
        #showing tables
        cur.execute("show tables;")
        rows = cur.fetchall()

        for row in rows:
            print row
    
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

    finally:
        if con:
            con.close()



#Terminal Menu (User Interface)
stay = True
print "\n\tWelcome to genome database test\nWARNING:Create database if not done already"

while stay:
    print "\n\t----------------------------------------------------\nChoose:"
    print "\t\t1)Create database\n\t\t2)Create New User\n\t\t3)Drop Database\n\t\t4)Delete User\n\t\t5)Show tables"
    choose=raw_input("\nIf you wish to quit write '/q' else write number of Command:")
    if choose == "/q":
        stay = False
    elif choose == "1":
	   createDatabase(tables)
    elif choose == "2":
	   createUserDB()
    elif choose == "3":
	   dropDatabase()
    elif choose == "4":
        dropUser()
    elif choose == "5":
        tableManagement()


print "Bye"
