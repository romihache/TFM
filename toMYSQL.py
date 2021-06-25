# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 19:15:59 2021

@author: romi
"""


from mysql.connector import connect as ct
from mysql.connector import Error as er



def main():
    #print("validation 1")

    def insert(tabla,campos, valores):
        try:
            with ct(
                 # temporary, the credencials will be in another file
                 host="127.0.0.1",
                 port = "33306",
                 user="root",
                 password="mariadb-pass",
                 database="resonadores"
                 ) as connection:
                with connection.cursor() as cursor:
                     sql = "INSERT INTO {0} {1} VALUES {2}".format(tabla,campos,valores)
                     #print(sql) #check what's inserting
                     #print("validation 2") #check if it is entering this loop
                     cursor.execute(sql)
                     connection.commit() #saves the changes
                     connection.close()
        # Show error if connection fails
        except er as e:
            print("No se pudo conectar a la base de datos, Error =====>  ")
            print(e)


if __name__ == '__main__':
     main()
#%%
#from toMYSQL import insert
#insert("mitabla","superquery")


