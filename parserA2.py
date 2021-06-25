# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 19:17:46 2021

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

#%% parse a2
currentFile = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(currentFile))
#print(path)
docs = glob.glob(os.path.join(path, "*_A2.log")) #get a list of the existing files inside the path
#rint(docs) #control line to verify the existing files in the path


dates = []
hours = []
helLevs = []#niveles de helio
pressures = []#presiones
boreTemps = []#temperatura de bore
linkTemps = []#temperature de link
cHTemps=[]#coldhead temperature
pHAP=[]#Preassure heater average power
filenames = []
posibles=['Helium Probe1','Link1 Temperature','Bore 1 Temperature','Magnet Pressure','Cold Head Temperature:','Pressure Heater Average Power:','Link 1 Temperature','Bore1 Temperature']

datesForm=[]
dateFormat = "%d.%m.%y"
dateOutFormat = "%Y-%m-%d"

fechassinhelio = []

# Open the file in read only mode
for d in docs:
    count=0
    measInDate=0
    date=0 #date being searched
    lastDate=0 #last date registered
    flagP=0
    flagBT=0
    flagLT=0
    flagCHT=0
    flagPHAP=0
    
    with open(d, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            count+=1
            if "supervisory test time:" in line: 
                date=line[28:36]
                hour=line[37:45]
            if "monitoring values:" in line: 
                date=line[24:32]
                hour=line[33:41]
            if lastDate==0:lastDate=date    #just for the first date
            if(date==lastDate): 
                #search for posible keywords in the line and save the match
                match = next((x for x in posibles if x in line), False)
                if match:#if there is a match, save according to which it is
                    if match==posibles[0] and not measInDate:
                        helLev=line[30:34].strip()
                        measInDate=1
                    elif (match==posibles[1] or match==posibles[6]) and not flagLT :
                        linkTemp=line[28:33].strip()
                        flagLT=1
                    elif (match==posibles[2] or match==posibles[7])and not flagBT:
                        boreTemp=line[28:32].strip()
                        flagBT=1
                    elif match==posibles[3] and not flagP:
                        pressure=line[26:30].strip()
                        flagP=1
                    elif match==posibles[4] and not flagCHT:
                        cHTemp=line[32:36].strip()
                        flagCHT=1
                    elif match==posibles[5] and not flagPHAP:
                        pHApow=line[40:44].strip()
                        flagPHAP=1
            else:#if the date has changed and there is a Helium measurement,register all values 
                if measInDate:
                    hours.append(hour)
                    dates.append(lastDate)
                    helLevs.append(helLev)
                    f=os.path.basename(d) #file name
                    filenames.append(f.replace('_A2.log',""))
                    #add zero if there wasn't that particular measurement
                    if not flagLT:linkTemp=0
                    linkTemps.append(linkTemp)
                    if not flagBT:boreTemp=0
                    boreTemps.append(boreTemp)
                    if not flagP:pressure=0
                    pressures.append(pressure)
                    if not flagCHT:cHTemp=0
                    cHTemps.append(cHTemp)
                    if not flagPHAP: pHApow=0
                    pHAP.append(pHApow)
                #reset flags
                lastDate=date
                measInDate=0
                flagP=0
                flagBT=0
                flagLT=0
                flagCHT=0
                flagPHAP=0
                
        if measInDate:#register values for last day
            hours.append(hour)
            dates.append(lastDate)
            f=os.path.basename(d) #file name
            filenames.append(f.replace('_A2.log',""))
            helLevs.append(helLev)
            if not flagLT:linkTemp=0
            linkTemps.append(linkTemp)
            if not flagBT:boreTemp=0
            boreTemps.append(boreTemp)
            if not flagP:pressure=0
            pressures.append(pressure)
            if not flagCHT:cHTemp=0
            cHTemps.append(cHTemp)
            if not flagPHAP: pHApow=0
            pHAP.append(pHApow)

for d in dates:
    f=datetime.strptime(d,dateFormat)
    datesForm.append(f.strftime(dateOutFormat))
           
df = pd.DataFrame(list(zip(datesForm, hours, helLevs, pressures, boreTemps, linkTemps,cHTemps,pHAP, filenames)), columns =['fecha','hora','nivelHelio_porc','presionMagneto_psiA','tempBore_K','tempLink_K','tempCabezaFria_K','pressHeaterAvgPower_W','idEquipo'])       
print(df)
#df.to_csv(r'E:\unir\apuntes\TFM doc\doc_mri\docs\DATA_A22.csv')      

#%% fields: idEquipo,fecha, hora, nivelHelio_porc, tempBore_K, presionMagneto_psiA, tempLink_K, tempCabezaFria_K, pressHeaterAvgPower_W

i = 0
a=""
b=''
for i in range(len(dates)): 
#for i in range(5): 
    
    if i < len(dates)-1:
        #print(i)
        #print(len(dates))
        #print(len(dates)-1)
        a= filenames[i],datesForm[i],hours[i],helLevs[i],boreTemps[i],pressures[i],linkTemps[i],cHTemps[i],pHAP[i]
        b+=str(a)+','    
        i+=1
        #print(i)
        
    else:
        a= filenames[i],datesForm[i],hours[i],helLevs[i],boreTemps[i],pressures[i],linkTemps[i],cHTemps[i],pHAP[i]
        b+=str(a)+';'  
        i+=1
print("modelo_A2")
print(b)

#