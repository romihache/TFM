# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 21:04:29 2021

@author: romi
"""


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
#path = os.getcwd()
#print(path)



def FormatDateC (datelist):
    
    datesForm=[]
    dateFormat = "%d-%b-%Y"
    dateOutFormat = "%Y-%m-%d"
    
    for d in datelist:
        f=datetime.strptime(d,dateFormat)
        datesForm.append(f.strftime(dateOutFormat))
    return datesForm  

fecha2 = datetime.strptime('03-FEB-2010',"%d-%b-%Y")
print(fecha2)

#%% PARSE C2 FILES (CLOSED MRI)
currentFile = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(currentFile))
#print(path)

docs = glob.glob(os.path.join(path, "*C2.txt")) #get a list of the existing files inside the path

#print(docs) #control line to verify the existing files in the path



dates = []
hours = []
helLevs = []
filenames = []

# Open the file in read only mode
for d in docs:
    count=0
    refDate=""
    with open(d, 'r') as read_obj:
        
        # Read all lines in the file one by one
        
        for line in read_obj:
            count += 1
            date = line[0 : 11] 
    
            if count == 4: refDate=date #first line with date, take that date as reference
            
            # For each line, check if it contains the string
            if (refDate != date and "Helium level [%]"  in line): 
                    
                    #parse data and append to lists
                    refDate=date                
                    hour = line[12 :20] 
                    helLev = line[65: 70]
                    dates.append(date)
                    hours.append(hour)
                    helLevs.append(helLev)
                    f=os.path.basename(d) #file name
                    filenames.append(f.replace('_C2.txt',"")) #keep just the number

datesForm=  FormatDateC(dates)  
#create df from lists and then export to csv
df = pd.DataFrame(list(zip(datesForm, hours, helLevs,filenames)), columns =['fecha','hora','nivelHelio_porc','idEquipo'])
df.to_csv(r'E:\unir\apuntes\TFM doc\doc_mri\docs\DATA_C2.csv')   
print(df)

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
        a= filenames[i],datesForm[i],hours[i],helLevs[i]
        b+=str(a)+','    
        i+=1
        #print(i)
        
    else:
        a= filenames[i],datesForm[i],hours[i],helLevs[i]
        b+=str(a)+';'  
        i+=1
print(b)
