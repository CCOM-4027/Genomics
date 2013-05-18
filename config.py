#make user test
import MySQLdb as mdb
import sys, getpass
from laad import do
from laad import create
from settings import guest
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

#Create database
def createDatabase(verbose = False):
    try:
        #Connect to SQL
        con = mdb.connect('localhost', 
                          'root', 
                          getpass.getpass("Please insert root password: "))
        cur = con.cursor()
        #Create the database
        from settings import database
        if verbose:
            print "Creating database %s..." % database
        cur.execute("CREATE DATABASE %s" % database)
        cur.execute("Use %s" % database)

        #Create tables
        if verbose:
            print "Creating tables..."
        from settings import tables2 as tables
        for statement in create(tables):
            cur.execute(statement)
        if verbose:
            print"Tables Created!"
        con.close()

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

#Create user
def createUserDB(sql, username=guest["username"], password=guest["password"]):
    if username == guest["username"]:
        password = guest["password"]
    else:
        password = getpass.getpass("Please, enter sql password for user %s:" % user)

    try:
        connection = mdb.connect('localhost', username, password, 'genomedb')
        cursor = connection.cursor()
        print "\nInsert new user name and password"
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
        sql.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s", (newUser, newPassword))
        sql.execute("GRANT ALL ON genomedb.* TO %s@'localhost'", newUser)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

def dropDatabase(sql):
    try:
        sql.execute("Drop database genomedb")
        print "Done!"
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

def dropUser(sql):
    try:
        print "Please indicate the user you which to delete"
	user = raw_input()
        sql.execute("Drop User %s@localhost",(user))
        print "User deleted"
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])


#Terminal Menu (User Interface)
def menu():
    stay = True
    print "\n\tWelcome to genome database test\nWARNING:Create database if not done already"
    while stay:
        print "\n\t----------------------------------------------------\nChoose:"
        print "\t\t1)Create database\n\t\t2)Create New User\n\t\t3)Drop Database\n\t\t4)Delete User"
        choose=raw_input("\nIf you wish to quit write '/q' else write number of Command:")
        if choose == "/q":
            stay = False
        elif choose == "1":
            createDatabase()
        elif choose == "2":
            do(createUserDB,'root')
        elif choose == "3":
            do(dropDatabase,'root')
        elif choose == "4":
            do(dropUser,'root')
    print "Bye"


        
