# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:52:02 2021

@author: romi
"""
import pandas as pd
import os
import glob
import random
from datetime import datetime
import inspect
#import datetime
#import math


#%%
#path = (r'E:\unir\apuntes\TFM doc\doc_mri\docs') #store the name of the path
path = os.getcwd()
print(path)

currentFile = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(currentFile))
docs = glob.glob(os.path.join(path, "*C3.txt")) #get a list of the existing files inside the path

#%% Randomize  A1 (CLOSED MRI) 
#Helium level, Shield Temperature


#abro el archivo que uso de base
doc =  open(glob.glob(os.path.join(path, '2224_A1.log')), 'r')

#lista de nombres que van a tener los logs.
#newNames=['3999','1','1578','2634','2887','1642','1581','1752','1584','2161',
#'2224','1657']
newNames=['3999','1','1578','2634','2887','1642','1581']

titles=[] #linea de los titulos de cada medicion
separators=[] #linea de separador
helLevs = [] #linea de datos de mediciones
values=[]#valores 
count=0


for line in doc: #save standard log entry
    values=line.split() 
    #dependiendo del numero de linea, la informacion que guardo
    if count==0: dates=values 
    if count==1: titles=line
    if count==2: helLevs=values
    if count==3: separators=line
    if count==5:break;    
       
    count+=1 #lo voy a hacer solo 4 veces

for n in newNames: #para cada archivo nuevo reseteo contador de day, mes 
    f=open(os.path.join(path,n+'_A1.log'),'w')    #creo el archivo con el nombre correcto
     
    count=0 
    date=datetime.datetime(2021,4,1,9,45)
    while count<61: #creo 61 mediciones
        #genero mediciones randomizadas para helio y temperatura
       # helLevs[0]=str(random.randint(35,70)+random.randint(1,9)/10)
        #helLevs[0]=str(35.8)#critico
        helLevs[0]=str(75.3)#normal
        #helLevs[0]=str(45.4)#importante
        helLevs[2]=str(67.9)
       
        

        
  #comienzo a escribir el archivo con el formato del original     
        f.write(str(date))
        f.write("\n")
        f.write(titles)
        i=0#lo uso como contador de posicion de caracteres para luego usar el parseo bien.
        while i<8:#posicion de inicio de la medicion de helio
            f.write(" ")
            i+=1
        f.write(helLevs[0])
        f.write(" ")
        f.write(helLevs[1])
        i+=len(helLevs[0])+len(helLevs[1])+1#agrego el largo de lo que escribi al contador d eposicion
        while i<29:#posicion de inicio de la medicion de temperatura
            f.write(" ")
            i+=1
        f.write(" "+helLevs[2])
        f.write("\n")      
        f.write(separators)
        
        count+=1
        date+=datetime.timedelta(days=1)
    f.close()
     
    
    
  #%% Randomize A2 (CLOSED MRI)
#Helium level, Shield Temperature


#abro el archivo que uso de base
doc =  open(glob.glob(os.path.join(path, '1608_A2.log')), 'r')

#lista de nombres que van a tener los logs.
#newNames=['3999','1','1578','2634','2887','1642','1581','1752','1584','2161','2224','1657']
#newNames=['2','3','1582','1583','1608','1656','2160','2162','1573','1767','3042','2763','3099','3274']
newNames=['2','3']
datesSup = [] #linea de fecha y hora supervisor
datesMon=[] #linea de fecha y hora monitoring
posibles=['Helium Probe1','Link1 Temperature','Bore 1 Temperature','Magnet Pressure','Cold Head Temperature:','Pressure Heater Average Power:','Link 1 Temperature','Bore1 Temperature']

helLevs = [] #linea de datos de mediciones
values=[]#valores 
count=0

dateFormat="%d.%m.%y"

for line in doc: #save standard log entry 
    #dependiendo del numero de linea, la informacion que guardo
    count+=1
    if 17<count<56:     
        datesMon.append(line)
    if 55<count<63: 
        datesSup.append(line)
    if count==63: break #63 lineas iniciales estandar
    
    
    
for n in newNames:
    f=open(os.path.join(path,n+'_A2.log'),'w')    #creo el archivo con el nombre correcto
    
    count=0
    date=datetime.datetime(2021,4,1)
    while count<61:    
        for d in datesMon:
            w=d#si no entro a ningun IF entonces copio la celda igual
            if"---> monitoring values:" in d:#le cambio la fecha a monitoring
                w=d.replace(d[24:32],date.strftime(dateFormat))          
            match = next((x for x in posibles if x in d), False)
            if match:#if there is a match, save according to which it is
                if match==posibles[0]:#Helio
                    #w=d.replace(d[30:34],str(35.4))#critico
                   #w=d.replace(d[30:34],str(45.6))#importante
                    w=d.replace(d[30:34],str(70.3))#normal
        
                    #w=d.replace(d[30:34],str(random.randint(35,70)+random.randint(1,9)/10))
        
                elif (match==posibles[1] or match==posibles[6]):#link temperature
                  w=d.replace(d[28:32],str(50.7))#bien
                  #w=d.replace(d[28:32],str(60.2))#mal
                  
                # w=d.replace(d[28:32],str(random.randint(30,70)+random.randint(1,9)/10))
                elif (match==posibles[2] or match==posibles[7]):#Bore temperature
                    w=d.replace(d[28:32],str(50.2))#bien
                    #w=d.replace(d[28:32],str(65.6))#mal
                    #w=d.replace(d[28:32],str(random.randint(30,70)+random.randint(1,9)/10))
                    
                elif match==posibles[3]:#Magnet pressure
                    w=d.replace(d[26:30],str(15.3))#bien
                    #w=d.replace(d[26:30],str(16.4))#mal
                    #w=d.replace(d[26:30],str(random.randint(30,70)+random.randint(1,9)/10))
                
                elif match==posibles[4]:#coldhead temp
                    w=d.replace(d[32:36],str(41.1)) #bien 
                    #w=d.replace(d[32:36],str(50.4))#mal
                    #w=d.replace(d[32:36],str(random.randint(37,55)+random.randint(1,9)/10))                  
                
                elif match==posibles[5]:#PHAP
                    w=d.replace(d[40:44],str(0.00))
                    #w=d.replace(d[40:44],str(random.randint(0,5)+random.randint(1,9)/10))
           
            f.write(w)    
  
        for d in datesSup:
            w=d
            if "---> supervisory test time:" in d:
                w=d.replace(d[28:36], date.strftime(dateFormat))          
            match = next((x for x in posibles if x in d), False)
            if match:#if there is a match, save according to which it is
                if match==posibles[0]:
                    #w=d.replace(d[30:34],str(35.4))#critico
                   #w=d.replace(d[30:34],str(45.6))#importante
                    w=d.replace(d[30:34],str(70.3))#normal
                    #w=d.replace(d[30:34],str(random.randint(35,70)+random.randint(1,9)/10))
                    
                      
                elif (match==posibles[1] or match==posibles[6]):#link temp
                    w=d.replace(d[28:32],str(50.7))#bien
                    #w=d.replace(d[28:32],str(60.2))#mal
                    #w=d.replace(d[28:32],str(random.randint(30,70)+random.randint(1,9)/10))
                elif (match==posibles[2] or match==posibles[7]):#bore temp
                    w=d.replace(d[28:32],str(50.2))#bien
                    #w=d.replace(d[28:32],str(65.6))#mal
                    #w=d.replace(d[28:32],str(random.randint(30,70)+random.randint(1,9)/10))
                    
                elif match==posibles[3]:#magnet pressure
                    w=d.replace(d[26:30],str(15.3))#bien
                    #w=d.replace(d[26:30],str(16.4))#mal
                    #w=d.replace(d[26:30],str(random.randint(30,70)+random.randint(1,9)/10))
                elif match==posibles[4]:#coldhead temp
                     w=d.replace(d[32:36],str(41.1)) #bien                 
                     #w=d.replace(d[32:36],str(50.4))#mal
                    #w=d.replace(d[32:36],str(random.randint(37,55)+random.randint(1,9)/10))                  
                elif match==posibles[5]:
                    w=d.replace(d[40:44],str(0.03))
                    
#                        w=d.replace(d[40:44],str(random.randint(0,5)+random.randint(1,9)/10))
           
            f.write(w) 
        date+=datetime.timedelta(days=1)
        count+=1
    f.close()
    

    
    
 #%% Randomize C1
#Helium level upper a and Lower, Pressure


#abro el archivo que uso de base
doc =  open(glob.glob(os.path.join(path, '2765_C1.txt')), 'r')

#lista de nombres que van a tener los logs.
#newNames=['2765','3091','3280','3289']
newNames=['3289']
head=[]
standard = [] #3 lineas estandar, 3(upper) 4(lower) 5(pressure)
dateFormat = "%d-%b-%Y"
w=[]
values=[]#valores 
count=0
date=0 #numero de dia
for line in doc: #save standard log entry 
    #dependiendo del numero de linea, la informacion que guardo
    if 0<=count<3:head.append(line)
    if 3<=count<6:standard.append(line)
    count+=1
    if count==6: break #6 lineas iniciales estandar
    
head[1]=head[1].replace(head[1],"Hospital name \n")    #quito nombre de hospital
    
for n in newNames:
    f=open(os.path.join(path,n+'_C1.txt'),'w')    #creo el archivo con el nombre correcto
    
    for h in head:f.write(h)
    count=0
    date=datetime.datetime(2021,4,1)
    
    while count<61:
        # randomizo los valores ese dia.
        ''' lowerLev=random.randint(30,70)+random.randint(1,9)/10
        upperLev=round(lowerLev+random.randint(10,20)+random.randint(1,9)/10,2)
        magnetPres=random.randint(0,60)+random.randint(1,9)/10
        '''
        #NORMALES
        '''
        lowerLev=round(67.599998,2)
        upperLev=round(lowerLev+random.randint(10,20)-random.randint(1,9)/10,2)
        magnetPres=30
        #IMPORTANTE HE
        lowerLev=round(45.577998,2)
        upperLev=round(lowerLev+random.randint(5,10)-random.randint(1,9)/10,2)
        magnetPres=30
        '''
        '''
        #critico He
        lowerLev=round(34.556998,2)
        upperLev=round(lowerLev+random.randint(5,10)-random.randint(1,9)/10,2)
        magnetPres=30
        
        #Importante pres
        '''
        lowerLev=round(67.599998,2)
        upperLev=round(lowerLev+random.randint(5,10)-random.randint(1,9)/10,2)
        magnetPres=64
        
        #cambio los valores en las lineas estandar
        w.append(standard[0].replace(standard[0][77:82],str(upperLev) ))
        w.append(standard[1].replace(standard[1][77:82],str(lowerLev) ))
        w.append(standard[2].replace(standard[2][69:71],str(magnetPres) ))
        #escribo las lineas al archivo cambiando la fecha
        f.write(w[0].replace(standard[0][0:11],date.strftime(dateFormat).upper()))
        f.write(w[1].replace(standard[1][0:11],date.strftime(dateFormat).upper()))
        f.write(w[2].replace(standard[2][0:11],date.strftime(dateFormat).upper()))
        #agrego un dia a la fecha
        date+=datetime.timedelta(days=1)
        count+=1
    f.close()
    

  
#%%randomizado B1

import datetime as dt
import numpy as np
#abro el archivo que uso de base
doc =  open(glob.glob(os.path.join(path, '24_B1.txt')), 'r')

#lista de nombres que van a tener los logs.
'''newNames=['3096','1511','2589','3102','2604','3796','3097','33','26','7',
    '2932','2586','3095','3652','3138','42','3082','39','3849','41','1574','2816',
    '3795','3700','2668','2869','38','2035','14','1622','3279','40','2194','11',
    '3115','18','9','2583','2582','28','1509','3396','17','20','22','24','1630',
    '3815']  '''  
newNames=['3096','1511','2589','3102','2604','3796','3097','33','26','7',  '2932','2586','3095','3652','3138','42','3082','39','3849','41','1574','2816',  '3795','3700','2668','2869','38','2035','14','1622','3279','40','2194','11''3115','18']   
df = pd.read_csv(doc, sep = ',', header=0, skipinitialspace = True) 
       
dates=[]
count=0
date=dt.datetime(2021,4,1)
dateFormat='%d-%b-%y'
while count<61:
    
    dates.append(date.strftime(dateFormat))
    date+=dt.timedelta(days=1)
    count+=1
df2=df[0:61].copy()

for n in newNames:
        f=open(os.path.join(path,n+'_B1.txt'),'w')    #creo el archivo con el nombre correcto
        
        
        df2['Date']=dates
        df2['Time']='00:00'
        '''
        df2['HeLvl']=np.random.randint(3000, 8000, 61)/100
        df2['HePress']=np.random.randint(500,1500,61)/1000
        df2['Shield']=np.random.randint(35000,60000,61)/1000
        df2['ReconRuO']=np.random.randint(1200,2000,61)/1000
        df2['ReconSi410']=np.random.randint(3000,4000,61)/1000
        df2['ColdheadRuO']=np.random.randint(7000,12000,61)/1000
        '''
        
        #Normal
        df2['HeLvl']=np.zeros(61)+70.32#>50
        df2['HePress']=np.zeros(61)+0.921#<4
        df2['Shield']=np.zeros(61)+42.578#<45
        df2['ReconRuO']=np.zeros(61)+1.503#<0.2 restandole al reconsi
        df2['ReconSi410']=np.zeros(61)+3.662#
        df2['ColdheadRuO']=np.zeros(61)+8.464
        '''
        #he critico
        df2['HeLvl']=np.zeros(61)+35.32#>50
        df2['HePress']=np.zeros(61)+0.921#<4
        df2['Shield']=np.zeros(61)+42.578#<45
        df2['ReconRuO']=np.zeros(61)+1.503#<0.2 restandole al reconsi
        df2['ReconSi410']=np.zeros(61)+3.662#
        df2['ColdheadRuO']=np.zeros(61)+8.464
        '''
        '''
        #he importate
        df2['HeLvl']=np.zeros(61)+45.32#>50
        df2['HePress']=np.zeros(61)+0.921#<4
        df2['Shield']=np.zeros(61)+42.578#<45
        df2['ReconRuO']=np.zeros(61)+1.503#<0.2 restandole al reconsi
        df2['ReconSi410']=np.zeros(61)+3.662#
        df2['ColdheadRuO']=np.zeros(61)+8.464
        '''
        '''
        #Presion fuera
        df2['HeLvl']=np.zeros(61)+70.32#>50
        df2['HePress']=np.zeros(61)+5.674#<4
        df2['Shield']=np.zeros(61)+42.578#<45
        df2['ReconRuO']=np.zeros(61)+1.503#<0.2 restandole al reconsi
        df2['ReconSi410']=np.zeros(61)+3.662#
        df2['ColdheadRuO']=np.zeros(61)+8.464
        '''
        '''
        #Shield fuera
        df2['HeLvl']=np.zeros(61)+70.32#>50
        df2['HePress']=np.zeros(61)+0.921#<4
        df2['Shield']=np.zeros(61)+56.578#<45
        df2['ReconRuO']=np.zeros(61)+1.503#<0.2 restandole al reconsi
        df2['ReconSi410']=np.zeros(61)+3.662#
        df2['ColdheadRuO']=np.zeros(61)+8.464
        '''
        '''
        #coldheadru0 fuera
        df2['HeLvl']=np.zeros(61)+70.32#>50
        df2['HePress']=np.zeros(61)+0.921#<4
        df2['Shield']=np.zeros(61)+42.578#<45
        df2['ReconRuO']=np.zeros(61)+2.503#<0.2 restandole al reconsi
        df2['ReconSi410']=np.zeros(61)+3.662#
        df2['ColdheadRuO']=np.zeros(61)+13.464
        '''
        
        df2.to_csv(f, index=False)
        f.close()
        
#%% Randomize C2 FILES (CLOSED MRI)
doc =  open(glob.glob(os.path.join(path, '2358_C2.txt')), 'r')

#newNames=['2747','2762','2990','3286','3411','3930','3948','3979','2358','2466','2467','2468','2783']   
newNames=['2358','2466','2467','2468','2783']

dateFormat='%d-%b-%Y'
head=[]
standard=''
count=0
w=''

for line in doc: #save standard log entry 
    #dependiendo del numero de linea, la informacion que guardo
    if 0<=count<3:
        head.append(line)
        
    if count==3:standard=line
    count+=1
    if count==4: break #6 lineas iniciales estandar

head[1]='Hospital name	\n'
  
  
for n in newNames:
    count=0
    f=open(os.path.join(path,n+'_C2.txt'),'w')    #creo el archivo con el nombre correcto
    for h in head: f.write(h)
    date=datetime.datetime(2021,4,1)
    while count<61:
        w=standard.replace(standard[65:70],str(35) )#critico
        #w=standard.replace(standard[65:70],str(45) )#importante
       # w=standard.replace(standard[65:70],str(70) )#Normal
        #escribo las lineas al archivo cambiando la fecha
        f.write(w.replace(w[0:11],date.strftime(dateFormat).upper()))
        
        date+=datetime.timedelta(days=1)
        count+=1
    
    f.close()    
    
#%% Randomize C3 FILES (CLOSED MRI)
doc =  open(glob.glob(os.path.join(path, '2751_C3.txt')), 'r')

#newNames=['2187','2751','3164','3245','3281','3614']   
newNames=['3614']

dateFormat='%d-%b-%Y'
head=[]
standard=[]
count=0
w=''

for line in doc: #save standard log entry 
    #dependiendo del numero de linea, la informacion que guardo
    if 0<=count<3:
        head.append(line)
        
    if 3<count<14:standard.append(line)
    count+=1
    if count==14: break #14 lineas iniciales estandar

head[1]='Hospital name	\n'
  
  
for n in newNames:
    count=0
    f=open(os.path.join(path,n+'_C3.txt'),'w')    #creo el archivo con el nombre correcto
    for h in head: f.write(h)
    date=datetime.datetime(2021,4,1)
    while count<61:
        for s in standard:
            w=s
            if "Helium level"  in s:
                #w=s.replace(s[65:70],str(35.12) )#critico
                #w=s.replace(s[65:70],str(45.43) )#importante
                w=s.replace(s[65:70],str(70.34) )#Normal
            elif "Magnet pres. level" in s:
                #w=s.replace(s[69:72],str(30) )#normal
                w=s.replace(s[69:72],str(64) )#atencion
                #escribo las lineas al archivo cambiando la fecha
            f.write(w.replace(w[0:11],date.strftime(dateFormat).upper()))
            
        date+=datetime.timedelta(days=1)
        count+=1
    
    f.close()    