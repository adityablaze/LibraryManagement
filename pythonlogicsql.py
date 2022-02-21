import mysql.connector
import datetime
from tabulate import tabulate

#this is updated
#sql connectivity
User = input("Enter your mysql username: ")
passwd = input("Enter your mysql password: ")
Host = "localhost"
datcon = mysql.connector.connect(host=Host, user=User, password=passwd) #connector object                                                                           
if datcon.is_connected():
     print("mysql connectivity successful")
else:
     print("mysql connection unsuccessful")
cursor = datcon.cursor()  #cursor object

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
query="create table if not exists memberlist \
(memid varchar(6) PRIMARY KEY,\
phoneno varchar(11) UNIQUE,\
mname varchar(50) NOT NULL,\
maddress varchar(60));"
cursor.execute(query)
query="create table if not exists borrowhis \
     (borrowid varchar(6) PRIMARY KEY, \
     memid varchar(6), \
     mname varchar(50), \
     mphone char(13), \
     bookid varchar(6), \
     bookname varchar(44), \
     doi date, \
     dor date \
     );"
cursor.execute(query)


# mainmenu__________________________________________________________________________________________________________  
def MainMenu():    
     l = [(1,"Add Books",8,"Add Members",12,"Borrow a book"),(2,"Search & Update Book Detail",9,"Display all members",13,"Display Borrow history"),(3,"Display all books",10,"Delete Member",14,"Return a Books"),(4,"Search & Delete Book",11,'Search & Display Member',15,"Borrow history stats"),(5,"Search & Display Books",'-','-',16,'Borrow history of a member'),(6,"Library Stats"),(7,"EXIT")]
     T = tabulate(l,headers=['Sno.','LIBRARY MANAGEMENT MAIN MENU','Sno.','Member functions','Sno.','Borrow functions'], tablefmt='fancy_grid')
     print(T)
     choice = int(input("write the corresponding Sno. for function you want to do : "))
     if choice == 1:
          addbooks()
     elif choice == 2:
          updatedetail()
     elif choice == 3:
          displaybooks()
     elif choice == 4:
          deletebook()
     elif choice == 5:
          search()
     elif choice == 6:
          libstats()
     elif choice == 7:
          closecon()
     elif choice == 8:
          addmembers()
          ldmenu()
     elif choice == 9:
          displaymembers()
     elif choice == 10:
          deletemember()
     elif choice == 11:
          searchmembers()
          ldmenu()
     elif choice == 12:
          borrowbook()
          ldmenu()
     elif choice == 13:
          displayborrow()
     elif choice == 14:
          returnbook()
          ldmenu()
     elif choice == 15:
          borrowhistats()
     elif choice == 16:
          borhofmember()
          ldmenu()

          
#closing connection____________________________________________________________________________
def closecon():
     datcon.close()
     print("Connection closed")

def borhofmember():
     searchmembers()
     id=input("please enter the MemberID to check its borrowhistory : ")
     query="select * from borrowhis where memid='{}'"
     headb=['BorrowID','MemberID','Member Name','Phone no.','BookID','Book name','DateofIssue','DateofReturn']
     cursor.execute(query.format(id))
     data=cursor.fetchall()
     if data==[]:
          print("No records found with that memberID !")
          return
     print(tabulate(data,headers=headb,tablefmt='psql'))
     input("Press Enter to display the borrow count -")
     query="select memid,mname,mphone,count(*) from borrowhis where memid='{}' group by mphone"
     cursor.execute(query.format(id))
     data=cursor.fetchall()
     print(tabulate(data,headers=['MemberID','Member Name','Phone no.','Borrow count'],tablefmt='psql'))
     return

#searching in members___________________________________________________________________________
def searchmembers():
     l=[(1,"MemberID"),(2,"Member Name"),(3,"phone number")]
     print(tabulate(l,headers=['Sno.','search attribute'],tablefmt='psql'))
     I=int(input("Enter the sno. to search with : "))
     headm=["MemberID","Phone Number","Member Name","Address"]
     if I==1:
          membid=input("Enter the MemberID to search : ")
          query="select * from memberlist where memid='{}'"
          cursor.execute(query.format(membid))
          data=cursor.fetchall()
          if data==[]:
               print("No Members found with that ID--")
               return
          print(tabulate(data,headers=headm,tablefmt='psql'))
          return
     elif I==2:
          memname=input("Enter the name (or first few letters) of member to search : ")
          query="select * from memberlist where mname like '{}'"
          memname=memname+'%'
          cursor.execute(query.format(memname))
          data=cursor.fetchall()
          if data==[]:
               print("No Members found !")
               return
          print(tabulate(data,headers=headm,tablefmt='psql'))
          return
     elif I==3:
          phno=input("Enter phone number to search : ")
          query="select * from memberlist where phoneno like '{}'"
          cursor.execute(query.format(phno))
          data=cursor.fetchall()
          if data==[]:
               print("No Members found !")
               return
          print(tabulate(data,headers=headm,tablefmt='psql'))
          return


def borrowhistats():
     l=[(1,'Display non returned borrow history'),(2,'Display borrow count of each member'),(3,'Display Borrow history of a member')]
     print(tabulate(l,headers=['sno.','Stats to display'],tablefmt='simple'))
     I=int(input("\nEnter the choice to display : "))
     headb=['BorrowID','MemberID','Member Name','Phone no.','BookID','Book name','DateofIssue','DateofReturn']
     if I==1:
          query="select * from borrowhis where dor='0000-0-0'"
          cursor.execute(query)
          data=cursor.fetchall()
          print(tabulate(data,headers=headb,tablefmt='psql'))
          ldmenu()
     elif I==2:
          query="select memid,mname,count(*) from borrowhis group by mname order by memid"
          cursor.execute(query)
          data=cursor.fetchall()
          head1=['MemberID','Member Name','Borrow count']
          print(tabulate(data,headers=head1,tablefmt='psql'))
          ldmenu()
     elif I==3:
          borhofmember()
          ldmenu()


#returing a book _____________________________________________________________________________
def returnbook():
     l=[("1.BorrowID","2.MemberID")]
     print(tabulate(l,tablefmt='simple'))
     I = int(input("enter the no. to search in borrow history : "))
     if I==1:
          borid=input("Enter The borrowID : ")
          query="select * from borrowhis where borrowid='{}'"
          cursor.execute(query.format(borid))
     elif I==2:
          membid=input("Enter the memberID : ")
          query="select * from borrowhis where memid='{}'"
          cursor.execute(query.format(membid))
     data=cursor.fetchall()
     if data==[]:
          print("no records found !")
          return
     headb=['BorrowID','MemberID','Member Name','Phone No.','BookID','Book name','DateofIssue','DateofReturn']
     print(tabulate(data,headers=headb,tablefmt='psql'))
     borid=input("please enter BorrowID again : ")
     query="update borrowhis set dor=curdate() where borrowid='{}'"
     cursor.execute(query.format(borid))
     datcon.commit()
     print("Book return data updated in borrow history successfully")
     return


#Borrowing a book______________________________________________________________________________
def borrowbook():
     try:
          borid=boridgen()
          phno=input("Please enter your phone number : ")
          memid=checkmember(phno)
          if memid==None:
               print("Please try borrowing again --")
               return
          mname=getname(memid)
          lst=borrowbooksrch()
          if lst==None:
               return
          bookid=lst[0]
          boname=lst[1]
          query="insert into borrowhis values('{}','{}','{}','{}','{}','{}',curdate(),'{}');"
          cursor.execute(query.format(borid,memid,mname,phno,bookid,boname,'0000-0-0'))
          datcon.commit()
          print("Borrow History Added Successfully !")
          return

     except Exception as e:
          print(e)
          print("some problem occured !")
          print("please make sure to enter details properly ")
          return


#checks member existence _____________________________________________________________________
def checkmember(phno):
     query="select memid from memberlist where phoneno='{}'"
     cursor.execute(query.format(phno))
     data = cursor.fetchall()
     if data==[]:
          print("Looks like you are not aldready a member!")
          print("Please enter all the details so that we can add you as a member")
          addmembers()
          return
     else:
          memid=data[0][0]
          return memid
def getname(memid):#___________________________________________________________________________
     query="select mname from memberlist where memid='{}'"
     cursor.execute(query.format(memid))
     data=cursor.fetchall()
     mname=data[0][0]
     return mname


#searching book feature for borrow function____________________________________________________
def borrowbooksrch():
     bname=input("Enter the book name (or first few letters) of the book to borrow : ")
     query="select * from booklist where bookname like '{}'"
     bnames=bname+'%'
     cursor.execute(query.format(bnames))
     data = cursor.fetchall()
     if data==[]:
          print("There are no books of that name !")
          return
     else:
          head=['BookID','Book Name','Author','Publisher','Edition','Cost','Category']
          print(tabulate(data,headers=head,tablefmt='psql'))
          boid=input("Enter the bookID to borrow : ")
          query="select bookid,bookname from booklist where bookid='{}'"
          cursor.execute(query.format(boid))
          data2=cursor.fetchall()
          if data2==[]:
               print("Please Enter bookid properly\n press enter --")
               input("")
               return
          else:
               retlist=['boid','bname']
               retlist[0]=data2[0][0]
               retlist[1]=data2[0][1]
               return retlist

#Display borrow history________________________________________________________________________
def displayborrow():
     query="select * from borrowhis"
     cursor.execute(query)
     data=cursor.fetchall()
     print(tabulate(data,headers=['BorrowID','MemberID','Member Name','Phone no.','BookID','Book name','DateofIssue','DateofReturn'],tablefmt='psql'))
     ldmenu()

#Adding Members________________________________________________________________________________
def addmembers():
     try :
          mname=input("Enter Member name : ")
          mphone=input("Enter phone number(10) : ")
          mid=midgen()
          addr=input("Enter you address(60) : ")
          query="insert into memberlist values('{}','{}','{}','{}')"
          cursor.execute(query.format(mid,mphone,mname,addr))
          datcon.commit()
          print("member added successfully !")
          return

     except Exception as e:
          #print(e)
          print("some problem occured !") 
          print("please make sure to enter details properly ")
          return


# Diplay all members__________________________________________________________________________
def displaymembers():
     headm=["MemberID","Phone Number","Member Name","Address"]
     query="select * from memberlist"
     cursor.execute(query)
     data=cursor.fetchall()
     if data==[]:
          print("There are currently no members !")
          ldmenu()
     else:
          T=tabulate(data,headers=headm,tablefmt='psql')
          print(T)
          ldmenu()


#Delete Member________________________________________________________________________________
def deletemember():
     headm=["MemberID","Phone Number","Member Name","Address"]
     print("You can search Member to delete using following --")
     T=[("1.Phone number","2.Member name","3.MemberID")]
     print(tabulate(T,tablefmt='simple'))
     ch=int(input("Enter your choice to search : "))
     if ch==1:
          phno=input("Enter the phone number : ")
          query="select * from memberlist where phoneno like '{}'"
          phnumb=phno+'%'
          cursor.execute(query.format(phnumb))
          data = cursor.fetchall()
          if data==[]:
               print("No members found !")
               ldmenu()
          else:
               print(tabulate(data,headers=headm,tablefmt='psql'))
               print("These records match your search")
               mid=input("Enter the memberID to delete : ")
               deletememberid(mid)
               ldmenu()
     elif ch==2:
          memname=input("Enter the member name : ")
          query="select * from memberlist where mname like '{}'"
          membname=memname+'%'
          cursor.execute(query.format(membname))
          data=cursor.fetchall()
          if data==[]:
               print("No members found !")
               ldmenu()
          else:
               print(tabulate(data,headers=headm,tablefmt='psql'))
               print("These records match your search")
               mid=input("Enter the memberID to delete : ")
               deletememberid(mid)
               ldmenu()
     elif ch==3:
          mid=input("Enter memberID : ")
          deletememberid(mid)
          ldmenu()


#for deletemember_____________________________________________________________________________
def deletememberid(id):
     query="select * from memberlist where memid='{}'"
     cursor.execute(query.format(id))
     data=cursor.fetchall()
     if data==[]:
          print("No member with that id !")
          return
     query="delete from memberlist where memid='{}'"
     cursor.execute(query.format(id))
     print("member deleted successfully !")
     datcon.commit()


# returns uinque member id based on previous id_______________________________________________ 
def midgen():
     query="select * from memberlist order by memid desc limit 1"
     cursor.execute(query)
     data=cursor.fetchall()
     if data==[]:
          return "m1"
     lastid=data[0][0]
     lid=""
     for i in range(1,len(lastid)):
          lid=lid+lastid[i]
     lidint=int(lid)
     lastboid="m"+str(lidint+1)
     return lastboid
# returns unique borrow id_____________________________________________________________________
def boridgen():
     query="select * from borrowhis order by borrowid desc limit 1"
     cursor.execute(query)
     data=cursor.fetchall()
     if data==[]:
          return "B1"
     lastid=data[0][0]
     lid=""
     for i in range(1,len(lastid)):
          lid=lid+lastid[i]
     lidint=int(lid)
     lastboid="B"+str(lidint+1)
     return lastboid
#adding books__________________________________________________________________________________     
def addbooks(): 
     try:
          while True:
               boid=boidgen()
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

#returns a unique book id based on previous book id _________________________________________
def boidgen():
     query="select * from booklist order by bookid desc limit 1"
     cursor.execute(query)
     data=cursor.fetchall()
     if data==[]:
          return "b1"
     lastid=data[0][0]
     lid=""
     for i in range(1,len(lastid)):
          lid=lid+lastid[i]
     lidint=int(lid)
     lastboid="b"+str(lidint+1)
     return lastboid

     
#display all books ____________________________________________________________________________
def displaybooks(): # funtion to display all books
     cursor.execute("select * from booklist")
     head=['BookID','Book Name','Author','Publication','Edition','Cost','Category']
     data = cursor.fetchall()
     if data==[]:
          print("There are currently no books")
     else:
          print(tabulate(data,headers=head,tablefmt='psql'))
          ldmenu()


#display library stats______________________________________________________________________________
def libstats():
     l=[(1,'Total no. of books in library'),(2,'Number of books in each Category'),(3,'Number of books of each Publisher'),(4,'Number of books of an Author'),(5,'Total cost of books')]
     print(tabulate(l,headers=['Sno.','Stats to display'],tablefmt='simple'))
     I=int(input("Enter the sno. for stats to see : "))
     if I==1:
          query="select count(*) as 'Number of books in library' from booklist"
          cursor.execute(query)
          data=cursor.fetchall()
          T = tabulate(data,headers=['Total number of books in library'],tablefmt='psql')
          print(T)
          ch=input("Do you want to check more stats (y/n) : ")
          if ch in 'Yy':
               libstats()
          else:
               ldmenu()
     elif I==2:
          query="select category,count(*) from booklist group by category order by count(*) desc"
          cursor.execute(query)
          data=cursor.fetchall()
          T = tabulate(data,headers=['Category','Number of books'],tablefmt='psql')
          print(T)
          ch=input("Do you want to check more stats (y/n) : ")
          if ch in 'Yy':
               libstats()
          else:
               ldmenu()
     elif I==3:
          query="select publisher,count(*) from booklist group by publisher order by count(*) desc"
          cursor.execute(query)
          data=cursor.fetchall()
          T = tabulate(data,headers=['Publisher','No. of books'],tablefmt='psql')
          print(T)
          ch=input("Do you want to check more stats (y/n) : ")
          if ch in 'Yy':
               libstats()
          else:
               ldmenu()
     elif I==4:
          query="select author,count(*) from booklist group by author order by count(*) desc"
          cursor.execute(query)
          data=cursor.fetchall()
          T = tabulate(data,headers=['Author','No. of books'],tablefmt='psql')
          print(T)
          ch=input("Do you want to check more stats (y/n) : ")
          if ch in 'Yy':
               libstats()
          else:
               ldmenu()
     elif I==5:
          query="select count(*),sum(cost) from booklist"
          cursor.execute(query)
          data=cursor.fetchall()
          T=tabulate(data,headers=['No. of books','Total Cost of all books'],tablefmt='psql')
          print(T)
          ch=input("Do you want to check more stats (y/n) : ")
          if ch in 'Yy':
               libstats()
          else:
               ldmenu()


#searching__________________________________________________________________________________________
def search():
     print("\nYou can search a book using the following -\n")
     print(tabulate([('1.BookID','2.Book Name','3.Author','4.Category','5.Publisher')]))
     I = int(input("\nEnter the sno. using which you want to search : "))
     if I==1:
          bookid=input("Enter BookID to search :")
          searchst('bookid',bookid)
          ldmenu()
     elif I==2:
          boname=input("Enter the Bookname or first few letters : ")
          searchst('bookname',boname)
          ldmenu()
     elif I==3:
          auth=input("Enter the Author name or first few letters : ")
          searchst('author',auth)
          ldmenu()
     elif I==4:
          categ=input("Enter the Category name or first few letters : ")
          searchst('category',categ)
          ldmenu()
     elif I==5:
          publ=input("Enter the Publisher name or first few letters : ")
          searchst('publisher',publ)
          ldmenu()
     
def searchst(srchattr,stuser):
     ch=input("do you want to sort the records (y/n) : ")
     if ch in 'yY':
          print("\nWhat do you want to sort about -")
          print(tabulate([('1.BookID','2.Book Name','3.Author','4.Cost','5.Publisher','6.Edition','7.Category')]))
          C=int(input("Enter your Choice to sort about : "))
          if C==1:
               query="select * from booklist where "+srchattr+" like '{}' order by bookid"
          elif C==2:
               query="select * from booklist where "+srchattr+" like '{}' order by bookname"
          elif C==3:
               query="select * from booklist where "+srchattr+" like '{}' order by author"
          elif C==4:
               query="select * from booklist where "+srchattr+" like '{}' order by cost"
          elif C==5:
               query="select * from booklist where "+srchattr+" like '{}' order by publisher"
          elif C==6:
               query="select * from booklist where "+srchattr+" like '{}' order by edition"
          elif C==7:
               query="select * from booklist where "+srchattr+" like '{}' order by category"

     elif ch in 'Nn':
          query="select * from booklist where "+srchattr+" like '{}'"

     searchstr=stuser+'%'
     cursor.execute(query.format(searchstr))
     data=cursor.fetchall()
     if data==[]:
          print("No records match your search !")
          return
     head=['BookID','Book Name','Author','Publisher','Edition','Cost','Category']
     print(tabulate(data,headers=head,tablefmt='psql'))
     print("\nThese records match your search ---")


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
          return
     head=['BookID','Book Name','Author','Publication','Edition','Cost','Category']
     print(tabulate(data,headers=head,tablefmt='psql'))
     ch=input("Are you sure to delete this record (y/n) : ")
     if ch in 'Nn':
          return
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
