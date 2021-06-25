# -*- coding: utf-8 -*-
"""
Created on Sun May 30 03:09:38 2021

@author: romi

"""

from toMYSQL import insert
#import pandas as pd
import os
import glob
#import random
from datetime import datetime
import inspect
#from mysql.connector import connect as ct
#from mysql.connector import Error as er

#import datetime
# 

#%%
def FormatDateC (datelist):
    
    datesForm=[]
    dateFormat = "%d-%b-%Y"
    dateOutFormat = "%Y-%m-%d"
    
    for d in datelist:
        f=datetime.strptime(d,dateFormat)
        datesForm.append(f.strftime(dateOutFormat))
    return datesForm  

fecha2 = datetime.strptime('03-FEB-2010',"%d-%b-%Y")
#print(fecha2)


#%% A1 PARSER
currentFile = inspect.getframeinfo(inspect.currentframe()).filename 
path     = os.path.dirname(os.path.abspath(currentFile)) #pathof the current file
docs = glob.glob(os.path.join(path, "*_A1.log")) #get a list of the existing files inside the path

print(docs) #control line to verify the existing files in the path


dates = [] #isn't neccesary to format de date, is already in YYYY-MM-DD format
hours = []
helLevs = []
shieldTemps = []
filenames = []

# Open the file in read only mode
for d in docs:
    count=0
    measInDate=0
    date=0 #date being searched
    lastDateReg=0#last date registered
    flagReg=0 #indicates that Helium level and Shield Temp must be registered
    flagAP=0 #indicates if the values must be appended
    with open(d, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            count+=1
            if count==1: 
                date=line[0:10]   
                hour=line[11:19]
            if date!=lastDateReg:
                if flagReg:
                    helLev=line[8:13].strip() #trim whitespaces
                    shieldTemp=line[30:32]
                    flagReg=0
                    flagAP=1
                elif "HeliumLevel" in line: 
                    flagReg=1
            elif line[0]=="2": 
                date=line[0:10]
                hour=line[11:19]
                 
            if flagAP:
                dates.append(date)
                lastDateReg=date
                hours.append(hour)
                helLevs.append(helLev)
                shieldTemps.append(shieldTemp)
                f=os.path.basename(d) #file name
                filenames.append(f.replace('_A1.log',""))
                flagAP=0
          


#%%
''' 
MODELO DE LOS DATOS:

insert into modelo_A1  
        (id, fecha, hora, nivelHelio_porc, tempShield_K, idEquipo) 
VALUES  
		(1, '2021-03-31','23:55:00',85.2,4.05,9876),
        (1, '2021-03-31','23:55:00',85.2,4.05,9886);
'''
 

#%%

#QUEDAN DESCARTADOS, NO HACEN FALTA:
#df = pd.DataFrame(list(zip(dates, hours, helLevs, shieldTemps, filenames)), columns =['fecha','hora','nivelHelio_porc','tempShield_K','idEquipo'])       
#print(df)
#df.to_csv(r'E:\unir\apuntes\TFM doc\doc_mri\docs\DATA_A1.csv')    


#%% GENERA UN STRING QUE TIENE TODOS LOS COMANDOS DE INSERT JUNTOS
#'idEquipo','fecha','hora','nivelHelio_porc','tempBore_K','tempRecondensadorCabezaFria_K','tempRecondensadorShield_K','tempCabezaFria_K','presionMagneto_psi',

i = 0
a=""
b=''
for i in range(len(dates)): 
#for i in range(5): 
    
    if i < len(dates)-1:
        #print(i)
        #print(len(dates))
        #print(len(dates)-1)
        a= filenames[i],dates[i],hours[i],helLevs[i],shieldTemps[i]
        b+=str(a)+','    
        i+=1
        #print(i)
        
    else:
        a= filenames[i],dates[i],hours[i],helLevs[i],shieldTemps[i]
        b+=str(a)+';'  
        i+=1
        print(b)
print("modeloA1")
insert("modelo_A1","idEquipo, fecha, hora, nivelHelio_porc, tempBore_K",b)
