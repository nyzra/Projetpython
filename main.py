import os
import pickle

class User:
    #definition of the User class which defines the type that will be stored in the database dictionnary
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
        self.key=f"{name}_{lastname}"
    #this defines the structure of a user with all their information
    def __repr__(self):
        output="/////////////////////////////////////////////////////////\n"
        output+=f"firstname: {self.firstname}\nlastname: {self.lastname}\nage: {self.age}\nYear of study: {self.yearStudy}\nField of study: {self.fieldStudy}\nCity: {self.city}\n"
        output+="Interest :\n"
        for i in self.interest:
            output+= f"{i}\n"
        output+= "Follow :\n"
        for i in self.folow:
            output+= f"{i}\n"
        output+= "Followed by :\n"
        for i in self.folowed:
            output+= f"{i}\n"
        output+="/////////////////////////////////////////////////////////\n"
        return output
    #defines the way of printing a User class object
    def addFolow(self,usr):
        self.folow.append(usr.key)
    #function that adds a follow to a user's following list
    def addFolower(self,usr):
        self.folowed.append(usr.key)
    #function that adds a follower to a user's follower list


database={}
#initialisation of the database dictionnary before loading the users stored in the memory using loadDatabase


    
def AddUser(database):
    #function to add a user in the dictionnary using saveDatabase
    name=input("Enter the name of the user : ").lower()
    lastname=input("Enter the lastname of the user : ").lower()

    if f"{name}_{lastname}" in database.keys():
        print("the user already exists")
        return

    age=int(input("Enter the age of the user : "))
    yearStudy=int(input("Enter the year of study of the user : "))
    fieldStudy=input("Enter the field of study of the user : ")
    nbinterest=int(input("how many interests does he have? : "))
    interest=[]
    for i in range(nbinterest):
        interest.append(input("Enter the interest of the user : "))
    city=input("Enter the city of the user : ")  
    database[f"{name}_{lastname}"]=User(name,lastname,age,yearStudy,fieldStudy,city,interest)
    saveDatabase(database,database[f"{name}_{lastname}"])


def saveDatabase(database,user):
    #function to save a new user as a file in the 'Users' directory
    pickle.dump(user, open("Users/"+user.key, "wb"))


def loadDatabase(database):
    #function used at the beginning of each execution to load all the users stored in the 'Users' directory to put them in the database dictionnary
    for file_name in os.listdir("Users"):
        chemin = os.path.join("Users", file_name)
        key = file_name.lower()
        database[key]=pickle.load(open(chemin,"rb"))

def getByName(database,firstname):
    #function to retrieve a user with his name
    correspondant=[]
    for key,usr in database.items():
        if firstname == usr.firstname:
            correspondant.append(usr)
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

def getByField(database,field):
    #function to retrieve a user (or more) with his field
    correspondant=[]
    for key,usr in database.items():
        if field == usr.fieldStudy:
            correspondant.append(usr)
        return correspondant, False
    else:
        return correspondant,True

def getByInterest(database,interest):
    #function to retrieve a user (or more) with his interest
    correspondant=[]
    for key,usr in database.items():
        if interest in usr.interest:
            correspondant.append(usr)
    if len(correspondant)==0:
        print(f"there is no user interested in {interest}")
        return correspondant, False
    else:
        return correspondant,True

def getByYear(database,year):    
    #function to retrieve a user (or more) with his year of study
    correspondant=[]
    for key,usr in database.items():
        if year == usr.yearStudy:
            correspondant.append(usr)
    if len(correspondant)==0:
        print(f"there is no user studying since {year}")
        return correspondant, False
    else:
        return correspondant,True

def searchByName(database):
    #function to search for a user using his name
    firstname=str(input("What is his first name :"))
    usr,find=getByName(database,firstname)
    if find:
        print(usr)

def searchByField(database):
    #function to search for a user (or more) using his field
    field=str(input("What is his field name :"))
    usrs,find=getByField(database,field)
    for usr in usrs:
        print(usr)

def searchByYear(database):
    #function to search for a user (or more) using his year of study
    year=int(input("What is his year of study :"))
    usrs,find=getByYear(database,year)
    for usr in usrs:
        print(usr)

def searchByInterest(database):
    #function to search for a user (or more) using his interest
    interest=str(input("What is his interest :"))
    usrs,find=getByInterest(database,interest)
    for usr in usrs:
        print(usr)

def searchUser(database):
    #function to search for a user using a certain parameter that is chosen
    print("How do you want to search for a user\n1.name\n2.field\n3.year of study\n4.areas of interest\n5.Quit")
    choice=int(input("Your choice :"))
    if choice==1:
        searchByName(database)
    elif choice==2:
        searchByField(database)
    elif choice==3: 
        searchByYear(database)
    elif choice==4:
        searchByInterest(database)
    elif choice==5:
        return

def AddFolow(database):
    #function to add a follower/following link between two users 
    name1=str(input("Who do you want to add folow : "))
    usr1,find1=getByName(database,name1)
    if not find1:
        print("the User could not be found")
        return
    name2=str(input("Who do you want to folow : "))
    usr2,find2=getByName(database,name2)
    if not find2:
        return
    usr1.addFolow(usr2)
    usr2.addFolower(usr1)
    saveDatabase(database,usr1)
    saveDatabase(database,usr2)

def DelteUser(database):
    #function to delete a user (deletion of the user and all his iterances in follower and following lists of other users)
    firstname=str(input("what is the name of the user you want to delete : "))
    delusr,find =getByName(database,firstname)
    if not find:
        return
    del database[delusr.key]
    for key,usr in database.items():
        if delusr.key in usr.folow:
            usr.folow.remove(delusr.key)
        if delusr.key in usr.folowed:
            usr.folowed.remove(delusr.key)
    
    os.remove(f"Users/{delusr.key}")

def updateUser():
    #function to update a user, changing the field of your choice
    name=str(input("Which user do you want to update : "))
    usr,find=getByName(database,name)
    if not find:
        print("the User could not be found")
        return
    if find:
        print(usr)
        print("What do you want to change :\n1.name\n2.field\n3.year of study\n4.areas of interest\n5.Age\n6.City\n7.Quit")
        choice=int(input("Your choice :"))
        if choice==1:
            usr.name=input("Enter the new name of the user : ").lower()
            usr.lastname=input("Enter the new lastname of the user : ").lower()
        elif choice==2:
            usr.fieldStudy=input("Enter the new field of study of the user : ")
        elif choice==3: 
            usr.yearStudy=int(input("Enter the new year of study of the user : "))
        elif choice==4:
            nbinterest=int(input("how many new interests does he have? : "))
            for i in range(nbinterest):
                usr.interest.append(input("Enter the interest of the user : "))
        elif choice==5:
            usr.age=int(input("Enter the age of the user : "))
        elif choice==6:
            usr.city=input("Enter the city of the user : ")     
        elif choice==7:
            return
        saveDatabase(database,usr)

def modificationUsers(database):
    #function to choose whether you want to  add, update or delete a user
    print("What do you want to do?\n1. Insert a user\n2.delete an user\n3.Update an users\n4. Quit")
    choice=int(input("Your choice :"))
    if choice==1:
        AddUser(database)
    elif choice==2:
        DelteUser(database)
    elif choice==3: 
        updateUser()
    elif choice==4:
        return

def displayFolowers(database):
    #function to display the followers of a certain user
    firstname=str(input("who do you want to display followers :"))
    usr,find=getByName(database,firstname)
    if find:
        print(f"{usr.firstname} {usr.lastname} is folowed by:")
        for folower in usr.folowed:
            print(folower)

def userSuggestions(database):
    #function to display 5 following suggestions for a user using (by choice) their mutual connections or their mutual interests
    firstname=str(input("who do you want to have follow suggestions for :"))
    usr,find=getByName(database,firstname)
    if not find:
        print("the User could not be found")
        return
    else:
        following=[]
        followers=[]
        for folower in usr.folowed:
            followers.append(folower)
        for folowed in usr.folow:
            following.append(folowed)
        results=[]
        print("On what do you want your suggestions to be based on?\n1. Mutual Interests\n2. Mutual Connections\n3. Both")
        choice=int(input("Your choice :"))
        for key ,usrs in database.items():
            if key not in following:            
                correspondant=0
                if choice == 1 or choice == 3:
                    for interest in usr.interest:
                        if interest in usrs.interest:
                            correspondant+=1
                if choice == 2 or choice == 3:
                    for folower in followers:
                        for folows in usrs.folowed:
                            if key == folows:
                                correspondant+=1
            results.append([key,correspondant])
        for i in range(len(results)):
            for j in range(0, len(results)-i-1):
                if results[j][1] > results[j+1][1] :
                    results[j], results[j+1] = results[j+1], results[j]
        for k in range(5):
            print(results[k][0])

def apllication(database):
    #the main function that loads the database dictionnary using loadDatabase and runs until the execution is terminated, it calls all the pther functions and is mainly the main user interface
    loadDatabase(database)
    active=True
    while active:
        print("what do you want to do?")
        print("1.Insertion, deletion and updating users.\n2.Adding followers to a user’s followers list.\n3.Display all the followers of a certain user.\n4.Search for users\n5.Propose a list of user suggestions for a certain user to follow\n6.Quit")
        choice=int(input("what is our choice :"))
        if choice ==1:
            modificationUsers(database)
        elif choice ==2:
            AddFolow(database)
        elif choice ==3:
            displayFolowers(database)
        elif choice ==4:
            searchUser(database)
        elif choice ==5:
            userSuggestions(database)
        elif choice ==6:
            active=False

apllication(database)