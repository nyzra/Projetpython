import os
import pickle

class User:
    def __init__(self,name,lastname,age,yearStudy,fieldStudy,city,interest=[],folow=[],folowed=[]):
        self.firstname=name
        self.lastname=lastname
        self.age=age
        self.yearStudy=yearStudy
        self.fieldStudy=fieldStudy
        self.city=city
        self.interest=interest
        self.folow=folow
        self.folowed=folowed
    def __repr__(self):
        output=f"firstname: {self.firstname}\nlastname: {self.lastname}\nage: {self.age}\nYear of study: {self.yearStudy}\nField of study: {self.fieldStudy}\nCity: {self.city}\n"
        output+="Interest :\n"
        for i in self.interest:
            output+= f"{i}\n"
        output+= "Folow :\n"
        for i in self.folow:
            output+= f"{i}\n"
        output+= "Folowed by :"
        for i in self.folowed:
            output+= f"{i}\n"
        return output
    def addFolow(self,name,lastname):
        self.folow.append(f"{name}_{lastname}")
    def addfolowed(self,name,lastname):
        self.folowed.append(f"{name}_{lastname}")


database={}



    
def AddUser(database):
    name=input("Enter the name of the user").lower()
    lastname=input("Enter the lastname of the user").lower()

    if f"{name}_{lastname}" in database.keys():
        print("the user alrdeay exist")
        return

    age=int(input("Enter the age of the user"))
    yearStudy=int(input("Enter the year of study of the user"))
    fieldStudy=input("Enter the field of study of the user")
    nbinterest=int(input("how many interest does he have?"))
    interest=[]
    for i in range(nbinterest):
        interest.append(input("Enter the interest of the user"))
    city=input("Enter the city of the user")  
    database[f"{name}_{lastname}"]=User(name,lastname,age,yearStudy,fieldStudy,city,interest)
    saveDatabase(database)


def saveDatabase(database):
    for key in database.keys():
        pickle.dump(database[key], open(f"Users/"+key, "wb"))


def loadDatabase(database):
    for file_name in os.listdir("Users"):
        chemin = os.path.join("Users", file_name)
        key = file_name.lower()
        database[key]=pickle.load(open(chemin,"rb"))

def getByName(database,firstname):
    correspondant=[]
    for key in database.keys():
        if firstname in key:
            correspondant.append(database[key])
    if len(correspondant)==0:
        print(f"there is no user named {firstname}")
        return 0, False
    if len(correspondant)>1:
        print(f"there are many users named {firstname}")
        lastname=input("Whar is his last name")
        for usr in correspondant:
            if usr.lastname==lastname:
                return usr,True
    else:
        return correspondant[0],True

def searchByName(database):
    firstname=str(input("What is his first name :"))
    usr,find=getByName(database,firstname)
    if find:
        print(usr)
        return usr

def searchUser(database):
    print("How do you want to search for a user\n1.name\n2.field\n3.year of study\n4.areas of interest\n5.Quit")
    choice=int(input("Your choice :"))
    if choice==1:
        searchByName(database)
    elif choice==2:
        return
    elif choice==3: 
        return
    elif choice==4:
        return
    elif choice==5:
        return

def AddFolow(database):
    name1=str(input("Who do you want to add folow"))
    usr1,find1=getByName(database,name1)
    if not find1:
        return
    name2=str(input("Who do you want to folow"))
    usr2,find2=getByName(database,name2)
    if not find2:
        return
    usr1.addFolow(usr2.firstname,usr2.lastname)
    usr2.addFolower(usr1.firstname,usr1.lastname)

def DelteUser(database):
    firstname=str(input("what is the name of the user you want to delete :"))
    usr,find =getByName(database,firstname)
    if not find:
        return
    del database[f"{usr.firstname}_{usr.lastname}"]
    os.remove(f"Users/{usr.firstname}_{usr.lastname}")

def updateUser():
    return

def modificationUsers(database):
    print("What do you want to do?\n1. Insert a user\n2.delete an user\n3.Update an users_n4. Quit")
    choice=int(input("Your choice :"))
    if choice==1:
        AddUser(database)
    elif choice==2:
        DelteUser(database)
    elif choice==3: 
        updateUser()
    elif choice==4:
        return

def apllication(database):
    loadDatabase(database)
    active=True
    while active:
        print("what do you want to do?")
        print("1.Insertion, deletion and updating users.\n2.Adding followers to a user’s followers list.\n3.Display all the followers of a certain user.\n4.Search for users\n5.Propose a list of user suggestions for a certain user to follow\n6.Quit")
        choice=int(input("what is our choice :"))
        if choice ==1:
            modificationUsers(database)
        elif choice ==2:
            return
        elif choice ==3:
            return
        elif choice ==4:
            searchUser(database)
        elif choice ==5:
            return
        elif choice ==6:
            active=False
    saveDatabase(database)
apllication(database)