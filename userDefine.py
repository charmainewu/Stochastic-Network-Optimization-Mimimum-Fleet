# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 23:03:44 2018

@author: jmwu
"""
#build the network

import xlrd
import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from scipy import optimize
import math

def excel_table_byindex(file= 'file.xls',by_index=0):
    data = xlrd.open_workbook(file)
    table = data.sheets()[by_index]
    nrow = table.nrows 
    ncol = table.ncols 
    return table,nrow,ncol

def compDistance():
    row = 1000
    table,nrows,ncols = excel_table_byindex("C:\\Users\\jmwu\\Desktop\\distance.xlsx",0)
    df = pd.DataFrame(np.random.randn(row,row))
    for i in range(row):
        for j in range(row):
            df[i][j] = 100000000000000            
    for i in range(row*row):
        df[int(table.cell(i + 1, 1).value)-1][int(table.cell(i + 1, 2).value)-1] = table.cell( i + 1, 3).value
        
    return df

def deletMatrix(df,batchn,unit):
    df1 = df.iloc[(0+unit*batchn):(unit+unit*batchn),(0+unit*batchn):(unit+unit*batchn)]
    return df1

    
def compfleet(dic,unit):
    fleet = {}
    count = 0
    num = 0
    i = 1
    while(0<i<=1000):
        fleet[count] = []
        i = 1
        while(0<i<=1000):
            if(dic.has_key(i)==True and dic[i]!=None):
                fleet[count].append(i)
                break
            else:
                i = i+1
        while(0<i<=1000): 
            if(dic.has_key(i)==True and dic[i]!=None):
                fleet[count].append(dic[i]-1000)
                temp = i
                i = dic[i]-1000
                del dic[temp]
            else:
                break
        count = count + 1
    for j in range(len(fleet)):
        for k in range(len(fleet)):
            if( fleet[j] != [] and fleet[k]!=[] and fleet[j][0] == fleet[k][-1]):
                del fleet[j][0]
                fleet[k] = list(fleet[k]+fleet[j])
                fleet[j] = []
                break
    for key in list(fleet.keys()):
        if not fleet.get(key):
           fleet.pop(key)
        else:
           num = num + len(fleet[key])
    fleetsize = len(fleet)+unit-num
    return fleet,fleetsize

def drawFNetwork(fleet,node):
    G = nx.Graph()
    for k in node:
        G.add_node(k)
    for key in list(fleet.keys()):
        j = 0
        while(j<30):
            try:
                G.add_edge(fleet[key][j],fleet[key][j+1]) 
                j = j + 1
            except:
                j = j + 1
                continue
    return G
          
      
def compNetwork(df,unit):
   speed =  60000
   table1,nrows1,ncols1 = excel_table_byindex("C:\\Users\\jmwu\\Desktop\\down.xls",0)
   table2,nrows2,ncols2 = excel_table_byindex("C:\\Users\\jmwu\\Desktop\\up.xls",0)
   B = nx.Graph()
   
   node = []
   for i in range(nrows1-1):
       for j in range(nrows2-1):
           try:
               distance = df[int(table1.cell(i+1,0).value)][int(table2.cell(j+1,0).value)]
               if distance/speed < (table2.cell(j+1,2).value - table1.cell(i+1,2).value):
                   '''
                   B.add_node(int(table1.cell(i+1,0).value), bipartite=0)
                   node.append(int(table1.cell(i+1,0).value))
                   B.add_node(int(table2.cell(j+1,0).value)+1000, bipartite=1)
                   node.append(int(table2.cell(j+1,0).value))
                   B.add_edge(int(table1.cell(i+1,0).value), int(table2.cell(j+1,0).value)+1000)
                   '''
                   if int(table1.cell(i+1,0).value) not in node:
                       B.add_node(int(table1.cell(i+1,0).value), bipartite=0)
                       node.append(int(table1.cell(i+1,0).value))
                   if int(table2.cell(j+1,0).value)+1000 not in node:
                       B.add_node(int(table2.cell(j+1,0).value)+1000, bipartite=1)
                       node.append(int(table2.cell(j+1,0).value)+1000)
                   B.add_edge(int(table1.cell(i+1,0).value), int(table2.cell(j+1,0).value)+1000)
           except:
                continue

   if(len(B)==0):
       return [],unit
   '''
   G = nx.Graph()
   for k in node:
       G.add_node(k)
   for i in range(nrows1-1):
       for j in range(nrows2-1):
           try:
               distance = df[i][j]
               if distance/speed <= (table2.cell(j+1,2).value - table1.cell(i+1,2).value):
                   G.add_edge(int(table1.cell(i+1,0).value), int(table2.cell(j+1,0).value))
           except:
                continue
   nx.draw(G, with_labels=True, font_weight='bold')
   plt.show()
   nx.draw_circular(B, with_labels=True, font_weight='bold')
   plt.show()
   node = list(set(node))
   '''
   fleet = nx.algorithms.bipartite.matching.hopcroft_karp_matching(B, top_nodes=None)
   ffleet, fleetsize = compfleet(fleet,unit)
   '''
   nx.draw_shell(drawFNetwork(ffleet,node), with_labels=True, font_weight='bold')
   plt.show()
   '''
   return ffleet, fleetsize
'''
def compDist(fleet,batch,df):
    delay = []
    fleetnode = []
    if fleet==[]:
        for i in range(batch*unit,(batch+1)*(unit)):
            dist = 0.00000000001
            time = np.random.uniform(100000,200000)  
            dist = dist + df[i][i]
            delay.append(time/dist)
        return np.mean(delay)
    
    for key in list(fleet.keys()):
        for item in list(fleet[key]):
            fleetnode.append(item)
    for key in list(fleet.keys()):
        j = 0
        dist = 0.00000000001
        time = np.random.uniform(100000,200000)
        while(j<20):
            try:
                dist = dist + df[fleet[key][j]][fleet[key][j]]
                dist = dist + df[fleet[key][j]][fleet[key][j+1]]
                j = j + 1
            except:
                j = j + 1
                continue
        delay.append(time/dist)
    for i in range(batch*unit,(batch+1)*(unit)):
        dist = 0.00000000001 
        time = np.random.uniform(100000,200000)  
        if i not in fleetnode:
            dist = dist + df[i][i]
            delay.append(time/dist)
    ave = np.mean(delay)
    return ave
'''

def compDist(fleet,df):
    delay = [] 
    node1 = []
    if fleet == []:
        for i in list(df.columns.values):
            dist = df[i][i]
            time = np.random.uniform(10000000,20000000)
            if dist ==0:
                continue
            else:
                delay.append(time/dist)
    else: 
        for fleetk in list(fleet.keys()):
            dist = 0
            for i in fleet[fleetk]:
                time = np.random.uniform(10000000,20000000)
                dist = dist + df[i][i]
                node1.append(i)
            if dist==0:
                continue
            else:
                delay.append(time/dist)
        for i in list(df.columns.values):
            if i not in node1:
                time = np.random.uniform(10000000,20000000)
                dist = df[i][i]
                if dist==0:
                    continue
                else:
                    delay.append(time/dist)
    if delay==[]:
        return 0
    ave = np.mean(delay)
    return ave
    
    
def f(x):
    a = 4
    b = 6
    v = 1
    mu = np.random.uniform(a,b)
    return  max(x+dav*mu*v,b)-v*dav
     
if __name__=="__main__":
    dfm = compDistance()
    asize = []
    price = []
    for unit in [10,20,25,40,50,100]:
        print unit
        x_m = []
        avesize = []
        for batchnum in range(int(math.ceil(1000/unit))):
           df = deletMatrix(dfm,batchnum,unit)
           Fleet,Fleetsize = compNetwork(df,unit)
           dav = compDist(Fleet,df)
           print dav
           x_min = optimize.fminbound(f, 0, 3)
           x_m.append(x_min)
           avesize.append(Fleetsize)
        price.append(np.mean(x_m))
        asize.append(sum(avesize))
       

    






            
        
    
    
    

