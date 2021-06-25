# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 20:19:41 2021

@author: romi
"""


#import pandas as pd
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
print(fecha2)


#%% PARSE C1 FILES (OPEN MRI) 
currentFile = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(currentFile))
#print(path)
docs = glob.glob(os.path.join(path, "*C1.txt")) #get a list of the existing files inside the path

print(docs) #control line to verify the existing files in the path


dates = []
hours = []
upHelLevs = []
loHelLevs = []
pressures = []
filenames = []




# Open the file in read only mode
for d in docs:
    with open(d, 'r') as read_obj:
        
        # Read all lines in the file one by one
        count=0
        measInDate=0
        date=0
        flagP=0
        hour=0
        for line in read_obj:
            count += 1
            if(count>3):
                
                if (date!=line[0 : 11] and date!=0): #If the day changes and I don't have the necesary measures, reset flags
                    if flagP==0 and measInDate>0: pressures.append("0")
                    
                    if(measInDate!=0): 
                        measInDate=0
                        flagP=0
                        dates.append(date) 
                        hours.append(hour) 
                        f=os.path.basename(d) #file name
                        filenames.append(f.replace('_C1.txt',"")) #keep just the number
                    
                
                
                date = line[0 : 11].strip() 
    
                # For each line, check if it contains the string
                if (measInDate<2 and "helium level"  in line): 
                        
                        #parse data and append to lists
                        
                        measInDate+=1 #add 1 measurement count
                     
                          #extract the helium level
                        helLev = line[77: 82].strip() 
                        hour = line[12 :20].strip()
                        #set value depending of which magnet the measure is
                        if "Upper" in line: upHelLevs.append(helLev)  
                        else: loHelLevs.append(helLev)  
                        
                        
    
                if (flagP==0 and "Magnet pres. level"  in line):
                        #parse data and append to lists
                        flagP=1 #Magnet pressure registered
                        pressures.append(line[69: 71].strip())
                        
                        
        if(measInDate!=0): 
            dates.append(date) 
            hours.append(hour) 
            f=os.path.basename(d) #file name
            filenames.append(f.replace('_C1.txt',"")) #keep just the number

datesForm=  FormatDateC(dates) 
              

#create df from lists and then export to csV             
#df = pd.DataFrame(list(zip(datesForm, hours, upHelLevs, loHelLevs, pressures, filenames)), columns =['fecha','hora','nivelHelioSup_porc','nivelHelioInf_porc','presionMagneto_hPa','idEquipo'])          
#df.to_csv(r'E:\unir\apuntes\TFM doc\doc_mri\docs\DATA_C1.csv')   
#print(df)

#%%
#idEquipo,fecha, hora, nivelHelioSup_porc, nivelHelioInf_porc, presionMagneto_hPa, tempLink_K, tempCabezaFria_K, pressHeaterAvgPower_W
i = 0
a=""
b=''
for i in range(len(dates)): 
#for i in range(5): 
    
    if i < len(dates)-1:
        print(i)
        print(len(dates))
        print(len(dates)-1)
        a= filenames[i],datesForm[i],hours[i],upHelLevs[i],loHelLevs[i],pressures[i]
        b+=str(a)+','    
        i+=1
        print(i)
        
    else:
        a= filenames[i],datesForm[i],hours[i],upHelLevs[i],loHelLevs[i],pressures[i]
        b+=str(a)+';'  
        i+=1
print(a)
print(b)

#