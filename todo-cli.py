#-----------------------------------------------------------------------------------------------------

###Author: Omio
###Project: TODO CLI APPLICATION
###Date: 09/October/2019
###Version: 1.0.0

#-----------------------------------------------------------------------------------------------------


import mysql.connector
from getpass import getpass
from termcolor import colored
import sys
import time

#-----------------------------------------------------------------------------------------------------
def loging_out():
    print(colored(">>Logging out",'red',attrs=['bold']), sep=' ',end='',flush=True) 
    for i in range(5):
        print(colored(".",'red',attrs=['bold']),sep=' ',end='',flush=True)
        time.sleep(0.70)
    print("\n")

def show_menu():
    #print('\n')
    print(colored('>>Select Any Option: ','green',attrs=['bold']))
    print(colored("        1.See Tasks    2.Add Tasks    3.Logout",'green',attrs=['bold']))

def show_menu_task():
    print(colored('>>Select Any Command: ','green',attrs=['bold']))
    print(colored("        [DN]Mark as Done    [RM]Remove Tasks    [B]Back",'green',attrs=['bold']))

def add_task(username,task,mycursor):
  sql = "INSERT INTO tasks (owner,task) VALUES (%s,%s)"
  val = (username,task)
  mycursor.execute(sql,val)
  mydb.commit()

def strike(text):
    return "".join([u'\u0336{}'.format(c) for c in text])

def view_tasks(username,mycursor):
    sql = "SELECT task,status FROM tasks WHERE owner='"+username+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mydb.commit()
    index=1
    for data in myresult:
        if(data[1]):
            print("        "+colored(str(index)+"."+strike(data[0]),'yellow',attrs=['bold']))
        else:
            print("        "+colored(str(index)+"."+data[0],'yellow',attrs=['bold']))
        index+=1


def option(command):
  number = ""
  for char in command:
    if char>= '1' and char<= '9':
      number = number + char
    if char=='*':
        return char
    if len(number)>0 and (char==' ' or char>='a' and char<='z'):
      break

  return int(number)-1


def delete_task(username,index,mycursor):
    if index == '*':
        sql = "DELETE FROM tasks WHERE owner='"+username+"'"
    else:
        sql_fetch = "SELECT task_id FROM tasks WHERE owner='"+username+"'"
        mycursor.execute(sql_fetch)
        myresult = mycursor.fetchall()
        mydb.commit()
        task_id = (myresult[index])[0]
        sql = "DELETE FROM tasks WHERE task_id='"+str(task_id)+"'"
    mycursor.execute(sql)
    mydb.commit()


def mark_task(username,index,mycursor):
    if index=='*':
        sql_update = "UPDATE tasks SET status='1' WHERE owner='"+username+"'"
    else:
        sql_fetch = "SELECT task_id FROM tasks WHERE owner='"+username+"'"
        mycursor.execute(sql_fetch)
        myresult = mycursor.fetchall()
        mydb.commit()
        task_id = (myresult[index])[0]
        sql_update = "UPDATE tasks SET status='1' WHERE task_id='"+str(task_id)+"'"
    mycursor.execute(sql_update)
    mydb.commit()
#-----------------------------------------------------------------------------------------------------
mydb = mysql.connector.connect(
  host="remotemysql.com",
  user="t3efuyDEcc",
  passwd="zlo0Tr0Swm",
  database="t3efuyDEcc"
) #global
mycursor = mydb.cursor()

#-----------------------------------------------------------------------------------------------------

username = str(input(colored(">>Username: ",'green',attrs=['bold'])))
password = str(getpass(colored(">>Password: ",'green',attrs=['bold'])))
mycursor.execute("SELECT * FROM users WHERE uName='" +username+ "' AND pass='"+password+"'")
myresult = mycursor.fetchall()
if myresult == []:
        print(colored("Username and Password do not match!",'red',attrs=['bold']))
else:
    while True:
        show_menu()
        select = int(input(colored('>>','green',attrs=['bold'])))
        if select==1:
                    while True:
                        view_tasks(username,mycursor)
                        show_menu_task()
                        command = (str(input(colored('>>','green',attrs=['bold']))).strip()).lower()
                        if "dn" in command:
                            index_dn = option(command)
                            mark_task(username,index_dn,mycursor)
                            print(colored(">>Task has been marked!",'red',attrs=['bold']))
                        elif "rm" in command:
                            index_del = option(command)
                            delete_task(username,index_del,mycursor)
                            print(colored(">>Task has been removed!",'red',attrs=['bold']))
                        elif "b" in command:
                            break
                        else:
                            print(colored(">>Invalid Command!",'red',attrs=['bold']))


        elif select==2:
                    task = input(colored(">>Task Description: ",'green',attrs=['bold']))
                    add_task(username,task,mycursor)
                    print(colored(">>Task added to the list!",'red',attrs=['bold']))
        elif select==3:
                    loging_out()
                    break
        else:
                print(colored(">>Invalid Option!",'red',attrs=['bold']))




#-----------------------------------------------------------------------------------------------------