import mysql.connector
import datetime
from tabulate import tabulate

#this is updated
#sql connectivity
User = input("Enter your mysql username: ")
passwd = input("Enter your mysql password: ")
Host = "localhost"
datcon = mysql.connector.connect(host=Host, user=User, password=passwd) #connector object
cursor = datcon.cursor()                                                #cursor object                               
if datcon.is_connected():
     print("mysql connectivity successful")
else:
     print("mysql connection unsuccessful")


#database and tables creation
database = "librarymanagement"
cursor.execute("create database if not exists {}".format(database,))
print("--Database_Created--")
cursor.execute("use "+database)
query="create table if not exists booklist \
(bookid varchar(6) PRIMARY KEY,\
Bookname varchar(44) NOT NULL,\
Author varchar(50),\
Publisher varchar(50),\
Edition int,\
Cost int,\
Category varchar(50));"
cursor.execute(query)  #table creation query

# mainmenu__________________________________________________________________________________________________________  
def MainMenu():    
     l = [(1,"Add Books"),(2,"Search & Update Book Detail"),(3,"Display all books"),(4,"Search & Delete Book"),(5,"EXIT")]
     T = tabulate(l,headers=['Sno.','LIBRARY MANAGEMENT MAIN MENU'], tablefmt='fancy_grid')
     print(T)
     choice = int(input("write the corresponding serial number for function you want to perform: "))
     if choice == 1:
          addbooks()
     elif choice == 2:
          updatedetail()
     elif choice == 3:
          displaybooks()
     elif choice == 4:
          deletebook()
     elif choice == 5:
          closecon()

          
#closing connection____________________________________________________________________________
def closecon():
     print("Connection closed")
     datcon.close()

  
#adding books__________________________________________________________________________________     
def addbooks(): 
     try:
          while True:
               boid=input("Enter bookid(eg:b0001):")
               boname=input("Enter Book name: ")
               auth=input("Enter Author name: ")
               publ=input("Enter Publisher name: ")
               edn=int(input("Enter edition: "))
               cost=int(input("Enter cost of book: "))
               cat=input("Enter category of book: ")
               query="insert into booklist values('{}','{}','{}','{}',{},{},'{}')"
               cursor.execute(query.format(boid,boname,auth,publ,edn,cost,cat))
               datcon.commit()
               print("\nrecord added successfully ! \n")
               ch=input("Do you want to add more books (y/n):")
               if ch in 'nN':
                    break
          ldmenu()
     except Exception as e:
          #print(e)
          print("some problem occured!")
          print("\nplease make sure bookid needs to be unique ")
          ldmenu()

          
#display all books ____________________________________________________________________________
def displaybooks(): # funtion to display all books
     cursor.execute("select * from booklist")
     head=['BookID','Book Name','Author','Publication','Edition','Cost','Category']
     print(tabulate(cursor,headers=head,tablefmt='psql'))
     input("press enter to load main menu......")
     MainMenu()

     
#delete book_______________________________________________________________________________________
def deletebook():
     print("\nYou can search a book to delete using following -\n")
     print(tabulate([('1.BookID','2.Book Name','3.Author','4.Category','5.Publisher')]))
     I = int(input("\nEnter the sno. using which you want to search the book -"))
     if I==1:
          bookid=input("Enter BookID :")
          deleteid(bookid)
          ldmenu()
     elif I==2:
          boname=input("Enter book name or first few letters :")
          strdelete('bookname',boname)
          ldmenu()
     elif I==3:
          auth=input("Enter Author name or first few letters :")
          strdelete('author',auth)
          ldmenu()
     elif I==4:
          categ=input("Enter Category name or first few letters :")
          strdelete('category',categ)
          ldmenu()
     elif I==5:
          pub=input("Enter publisher name or first few letters :")
          strdelete('publisher',pub)
          ldmenu()


#delete search______________________________________________________________________________________          
def strdelete(srchattrbt,stuser):
     query="select * from booklist where "+srchattrbt+" like '{}'"
     head=['BookID','Book Name','Author','Publisher','Edition','Cost','Category']
     srchst=stuser+'%'
     cursor.execute(query.format(srchst))
     data = cursor.fetchall()
     if data == []:
          print("No Records found!")
          return
     print(tabulate(data,headers=head,tablefmt='psql'))
     print("\nThese records match your search ---")
     bookid=input("Enter BookID to delete :")
     deleteid(bookid)


#delete with an id ___________________________________________________________________________________ 
def deleteid(bookid):
     query="select * from booklist where bookid='{}'"
     cursor.execute(query.format(bookid))
     data=cursor.fetchall()
     if data==[]:
          print("No records where found! ")
          input("press enter")
          return
     head=['BookID','Book Name','Author','Publication','Edition','Cost','Category']
     print(tabulate(data,headers=head,tablefmt='psql'))
     query="delete from booklist where bookid='{}'"
     cursor.execute(query.format(bookid))
     print("record deleted successfully!")
     datcon.commit()

       
#update details of a book(s)____________________________________
def updatedetail():
     print("\nYou can search a book to update using following parameters -\n")
     print(tabulate([('1.BookID','2.Book Name','3.Author','4.Category','5.Publisher')]))
     I = int(input("\nEnter the sno. of the parameter you want to search a book to update -"))
     if I==1:
          bookid=input("Enter BookID -")
          updatechoices(bookid)           
          ldmenu()
     elif I==2:
          bookn=input("Enter Full name or First few letters -")
          strupdate('bookname',bookn)
          ldmenu()
     elif I==3:
          auth=input("Enter the Author name or first few letters of name -")
          strupdate('author',auth)
          ldmenu()
     elif I==4:
          categ=input("Enter the Category to search (first few letters will also work) :")
          strupdate('category',categ)
          ldmenu()
     elif I==5:
          pub=input("Enter the publisher to search or first few letters :")
          strupdate('publisher',pub)
          ldmenu()

     
#Used in updatedetails___________________________________________
def strupdate(srchattrbt,stuser):
     query="select * from booklist where "+srchattrbt+" like '{}'"
     head=['BookID','Book Name','Author','Publisher','Edition','Cost','Category']
     srchst=stuser+'%'
     cursor.execute(query.format(srchst))
     data = cursor.fetchall()
     if data == []:
          print("No records were found----")
          return
     print(tabulate(data,headers=head,tablefmt='psql'))
     print("These records match your search")
     bookid=input("\nEnter the BookID of the book to change details of -")
     updatechoices(bookid)

     
#searches using integers________________________________________________
def intupdate(srchattrbt,intuser):
     query="select * from booklist where "+srchattrbt+"={}"
     head=['BookID','Book Name','Author','Publisher','Edition','Cost','Category']
     cursor.execute(query.format(intuser))
     data = cursor.fetchall()
     if data == []:
          print("No records were found----")
          return
     print(tabulate(data,headers=head,tablefmt='psql'))
     print("These records match your search")

     
#used in update details funcion_________________________________________
def updatechoices(bookid):
     head=['BookID','Book Name','Author','Publisher','Edition','Cost','Category']
     query="select * from booklist where bookid='{}'"
     cursor.execute(query.format(bookid))
     data = cursor.fetchall()
     if data == []:
          print("No records were found----")
          return
     print(tabulate(data,headers=head,tablefmt='psql'))     
     print("What do you want to update")
     L = [(1,'Book Name'),(2,'Author'),(3,'Publisher'),(4,'Edition'),(5,'Cost'),(6,'Category')]
     T = tabulate(L,headers=['sno.','details to change -'],tablefmt='fancy_grid')
     print(T)
     I2=int(input("enter sno. of detail you want to update :"))
     if I2 == 1:
          name=input("Enter the new book name you want :")
          query="update booklist set bookname='{}' where bookid='{}'"
          cursor.execute(query.format(name,bookid))
          datcon.commit()
          print("name changed successfully!")
          return
     elif I2 == 2:
          auth=input("Enter the new name of Author :")
          query="update booklist set author='{}' where bookid='{}'"
          cursor.execute(query.format(auth,bookid))
          datcon.commit()
          print("Author changed succsessfully")
          return
     elif I2 == 3:
          publ=input("Enter the new name of Publisher:")
          query="update booklist set publisher='{}' where bookid='{}'"
          cursor.execute(query.format(publ,bookid))
          datcon.commit()
          return
     elif I2 == 4:
          editn=int(input("Enter the Edition to change to :"))
          query="update booklist set edition={} where bookid='{}'"
          cursor.execute(query.format(editn,bookid))
          datcon.commit()
          return
     elif I2 == 5:
          cost=int(input("Enter the new cost :"))
          query="update booklist set cost={} where bookid='{}'"
          cursor.execute(query.format(cost,bookid))
          datcon.commit()
          print("cost changed successfully!")
          return
     elif I2 == 6:
          categ=input("Enter the category to change to :")
          query="update booklist set category='{}' where bookid='{}'"
          cursor.execute(query.format(categ,bookid))
          datcon.commit()
          print("changed successfully")
          return
     
  
#loadingmenu____________________
def ldmenu():
     input("\nPress Enter to load menu----")
     MainMenu()

     
#main______________________________
MainMenu()

