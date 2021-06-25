# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 03:09:38 2021

@author: romi

"""


import pandas as pd
import os
import glob
#import random
from datetime import datetime
import inspect

#%%  OBTENER EL PATH EN QUE SE ESTÁ EJECUTANDO EL ARCHIVO





#%% funcion que formatea las fechas para el formato C de log
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

#%% PARSE B1 FILES (CLOSED MRI)
currentFile = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(currentFile))
#print(path)

docs = glob.glob(os.path.join(path, "*_B1.txt")) #get a list of the existing files inside the path
#print(docs) #control line to verify the existing files in the path


decimals = 3
dateFormat = "%d-%b-%y"
dateOutFormat = "%Y-%m-%d"
dates=[]
count=0#para identificar el último archivo

'''
#listas para enviar a BBDD
helLevs=[]
boreTemps=[]
reconTemps=[]
reconSITemps=[]
cHTemps=[]
pressures=[]
'''
file=open(os.path.join('stringB1.txt'),'w')


str4MySQL='' #string para enviar a BBDD
for d in docs:
    count+=1
    datesForm=[]#reseteo las fechas formateadas al inicio del documento
    hours=[]
    filenames=[]
    df = pd.read_csv(d, sep = ',', header=0, skipinitialspace = True) 
    
    df.iloc[:,0].str.strip()
    df.iloc[:,1].str.strip()
    df=df.iloc[:,[0,1,2,5,6,7,8,9]]
    #tomo solo el valor que midio a las 00
    df = df[df['Time'] =='00:00']
    df['Time']='00:00:00'
    
    #tomo solo 2 o 3 decimales
    df = df.round({"HeLvl":2,"Shield":decimals, "ReconRuO":decimals, "ReconSi410":decimals, "ColdheadRuO":decimals, "HePress":decimals})
    
    #convierto a string para que luego pueda pasarlo como un solo string a la BBDD

    i=2
    while i<8:
        df.iloc[:,i]=df.iloc[:,i].apply(str)
        i+=1
    
        
    dates=df['Date'].tolist()
    
    n= os.path.basename(d) #tomo el nombre del archivo para el idEquipo
    for a in dates:
        #para cada fecha doy el formato YYYY-MM-DD y guardo el idEquipo 
        f=datetime.strptime(a,dateFormat)
        datesForm.append(f.strftime(dateOutFormat))
        filenames.append(n.replace('_B1.txt',""))
        
    df['Date']=datesForm
    df.insert(0, 'IdEquipo',filenames)   
    
    '''
    #convierto la informacion a listas para pasar a la BBDD
    helLevs.extend(df['HeLvl'].tolist())
    boreTemps.extend(df['Shield'].tolist())
    reconTemps.extend(df['ReconRuO'].tolist())
    reconSITemps.extend(df['ReconSi410'].tolist())
    cHTemps.extend(df['ColdheadRuO'].tolist())
    pressures.extend(df['HePress'].tolist())

    
    #creo una lista con tuplos de informacion 
    listas=list(zip(filenames,datesForm,hours,helLevs,boreTemps,reconTemps,reconSITemps,cHTemps,pressures))
    
    str4MySQL = str(listas)[1:len(str(listas))-1]+';'      '''
    #guardo el string de cada equipo en el archivo separados con ',' y con ';' al final
    str4MySQL=str(df.to_records(index=False)).replace('\n',',')[1:-1]
    file.write(str4MySQL)
    if count==len(docs): file.write(';')
    else: file.write(',')
    
    
    #df2=df2.append(df)#agrego la informacion de este nuevo equipo al listado general
 
file.close()
#convierto la informacion en un solo string que se pasa a la BBDD
#str4MySQL=str(df2.to_records(index=False)).replace('\n',',')[1:-1]+";"
#print(str4MySQL)


#%%
f=open(os.path.join('stringB1.txt'),'w')
f.write(str4MySQL)
f.close()