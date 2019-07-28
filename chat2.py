import fbchat
from Levenshtein import jaro_winkler
import os
from quicksqlite import Connection
import getpass

class MsgDeleter:

    def __init__(self):
        self.DANGEROUS_WORDS=[]
        self.DANGEROUS_PEOPLE=[]
        self.login=''
        self.haslo=''
        self.client=None
        if os.path.isfile('base.db'):
            self.connection=Connection(path="base.db", auto_commit=True)
            if self.connection.select('keys','*'):
                self.DANGEROUS_WORDS.extend(list(self.connection.select('keys','*')))
            if self.connection.select('people', '*'):
                self.DANGEROUS_PEOPLE.extend(list(self.connection.select('people', '*')))
        else:
            self.connection=Connection(path="base.db", auto_commit=True)
            self.connection.create_table('keys',['word'], ['TEXT'])
            self.connection.create_table('people', ['name'], ['TEXT'])

    def __del__(self):
        self.connection.close()

    def addWord(self,word):
        self.DANGEROUS_WORDS.append(word)
        self.connection.insert('keys',[word])

    def addPerson(self,person):
        self.DANGEROUS_PEOPLE.append(person)
        self.connection.insert('people',[person])

    def zaloguj(self,name, passw):
        self.client = fbchat.Client(name, passw)

    def start(self):

        threads_ids = []

        threads = self.client.fetchThreadList()

        full_msgs = []
        for i in threads:
            if i.name in self.DANGEROUS_PEOPLE:
                a = self.client.fetchThreadMessages(i.uid)
                full_msgs.append(a)

        msgs_to_delete = []
        for i in range(len(full_msgs)):
            flag = False
            for j in range(len(full_msgs[i])):
                if full_msgs[i][j].text:
                    words = full_msgs[i][j].text.split(' ')
                    for l in words:
                        for m in self.DANGEROUS_WORDS:
                            if jaro_winkler(l, m) >= 0.75:
                                msgs_to_delete.append(full_msgs[i][j])
                                flag = True
                            if flag:
                                break
                        if flag:
                            break

        for i in msgs_to_delete:
            self.client.deleteMessages(i.uid)


    def printMenu(self):
        print('1 - zaloguj sie ')
        print('2 - dodaj slowo-klucz')
        print('3 - dodaj osobe ')
        print('4 - usun wiadomosci')



ob=MsgDeleter()

flag=False

while not flag:
    ob.printMenu()
    choice=int(input())
    if choice == 3:
        name=str(input('Podaj imie i nazwisko osoby z facebooka ktora chcesz dodac do filtrowania wiadomosci\n'))
        ob.addPerson(name)
    elif choice == 2:
        key=str(input('Podaj slowo klucz\n'))
        ob.addWord(key)
    elif choice == 1:
        email=str(input('Wpisz email do facebooka\n'))
        passw=str(getpass.getpass('Wpisz haslo do facebooka\n'))
        ob.zaloguj(email,passw)
    elif choice == 4:
        ob.start()
        flag=True
    else:
        print('nieprawidłowa liczba')



