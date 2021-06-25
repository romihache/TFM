# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 21:15:44 2021

@author: romi
"""

#%%
import pandas as pd
import os
import glob
#import random
from datetime import datetime
import inspect
#import datetime
#

#%%

#path = (r'E:\unir\apuntes\TFM doc\doc_mri\docs') #store the name of the path
path = os.getcwd()
print(path)



def FormatDateC (datelist):
    
    datesForm=[]
    dateFormat = "%d-%b-%Y"
    dateOutFormat = "%Y-%m-%d"
    
    for d in datelist:
        f=datetime.strptime(d,dateFormat)
        datesForm.append(f.strftime(dateOutFormat))
    return datesForm  

fecha2 = datetime.strptime('03-FEB-2010',"%d-%b-%Y")

#%% PARSE INGENIA FILES (CLOSED MRI) 
currentFile = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(currentFile))
docs = glob.glob(os.path.join(path, "*C3.txt")) #get a list of the existing files inside the path

print(docs) #control line to verify the existing files in the path


dates = []
hours = []
helLevs = []
pressures = []
filenames = []


fechassinhelio = []

# Open the file in read only mode
for d in docs:
    count=0
    measInDate=0
    date=0
    flagP=0
    with open(d, 'r') as read_obj:
        
        # Read all lines in the file one by one
        
        for line in read_obj:
            count += 1
            if(count>3):
                #If the date changes, check which measures to register
                if (date!=line[0 : 11] and date!=0): 
                    #If there's a Helium measurement then check if there is pressure or add it
                    if(measInDate==0) : fechassinhelio.append(date)
                    if(measInDate!=0): 
                        if flagP==0: pressures.append("0")
                        measInDate=0
                        flagP=0
                        dates.append(date) 
                        hours.append(hour)  #
                        f=os.path.basename(d) #file name
                        filenames.append(f.replace('_C3.txt',"")) #keep just the number
 
                date = line[0 : 11] 
                #print(date)
    
                # For each line, check if it contains the string
                if (measInDate==0 and "Helium level"  in line): 
                        
                        #parse data and append to lists
                        
                        measInDate=1 #set measurement flag
                     
                          #extract the helium level
                        helLev = line[65: 70] 
                        hour = line[12 :20]
                        #register helium level
                        helLevs.append(helLev)  
                          
 
                if (flagP==0 and "Magnet pres. level"  in line):
                        #parse data and append to lists
                        flagP=1 #Magnet pressure registered
                        pressures.append(line[69: 71])
                        
                        
        if(measInDate!=0): 
            dates.append(date) 
            hours.append(hour) 
            f=os.path.basename(d) #file name
            filenames.append(f.replace('_C3.txt',"")) #keep just the number
 
datesForm=  FormatDateC(dates)             


#create df from lists and then export to cs             
df = pd.DataFrame(list(zip(datesForm, hours, helLevs, pressures, filenames)), columns =['fecha','hora','nivelHelio_porc','presionMagneto_hPa','idEquipo'])       
#print(df)
df.to_csv(r'E:\unir\apuntes\TFM doc\doc_mri\docs\DATA_C3b.csv')


#%% 
#idEquipo,fecha, hora, nivelHelio_porc
i = 0
a=""
b=''
for i in range(len(dates)): 
#for i in range(5): 
    
    if i < len(dates)-1:
        #print(i)
        #print(len(dates))
        #print(len(dates)-1)
        a= filenames[i],datesForm[i],hours[i],helLevs[i],pressures[i]
        b+=str(a)+','    
        i+=1
        #print(i)
        
    else:
        a= filenames[i],datesForm[i],hours[i],helLevs[i],pressures[i]
        b+=str(a)+';'  
        i+=1

print("modelo_C3")
print(b)


