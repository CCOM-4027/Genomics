#make user test
import MySQLdb as mdb
import sys, getpass
from laad import do
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
def createDatabase():
    from settings import tables
    password=getpass.getpass("Please insert root password: ")
    try:
        #Connection
        con = mdb.connect('localhost', 'root', password)
        cur = con.cursor()
        cur.execute("CREATE DATABASE genomedb")

        #Table creation
        cur.execute("Use genomedb")
        for table in tables:
            cur.execute(table)
        print"Tables Created!"
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        if con:
            con.close()

#Create user
def createUserDB(sql):

    try:
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
        sql.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s", (newUser, newPassword))
        sql.execute("GRANT ALL ON genomedb.* TO %s@'localhost'", newUser)

	print"Done!"


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
