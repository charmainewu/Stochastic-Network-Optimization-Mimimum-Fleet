# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 23:03:44 2018

@author: jmwu
"""
#build the network

import xlrd
import pandas as pd
import numpy as np
import math
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from scipy import optimize

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

def getMatrix(df,unit,batchn,T):
    picklist = []
    for i in range(1000):
        if issuet[i]<=1+unit*batchn and td[i]<=(1+unit*batchn)+T and i not in nodesig:
            picklist.append(i)
            nodesig.append(i)
    df1 = df.iloc[picklist,picklist]
    return df1

def compfleet(dic,total):
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
    fleetsize = len(fleet)+total-num
    return fleet,fleetsize

def compNetwork(df):
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
       return [],len(df.columns) 
   fleet  = {}
   for c in nx.connected_components(B):
       f = nx.algorithms.bipartite.matching.hopcroft_karp_matching(B.subgraph(c), top_nodes=None)
       fleet = dict(fleet.items()+f.items())
   ffleet, fleetsize = compfleet(fleet,len(df.columns))
   return ffleet, fleetsize

def compDist(fleet,df):
    delay = [] 
    node1 = []
    if fleet == []:
        for i in list(df.columns.values):
            dist =  df[i][i]
            time = np.random.uniform(1000000,2000000)
            if dist==0:
                continue
            else:
                delay.append(time/dist)

    else: 
        for fleetk in list(fleet.keys()):
            dist = 0
            for i in fleet[fleetk]:
                time = np.random.uniform(1000000,2000000)
                dist = dist + df[i][i]
                node1.append(i)
            if dist==0:
                continue
            else:
                delay.append(time/dist)
        for i in list(df.columns.values):
            if i not in node1:
                time = np.random.uniform(1000000,2000000)
                dist =  df[i][i]
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
    td = []
    issuet = []
    table2,nrows2,ncols2 = excel_table_byindex("C:\\Users\\jmwu\\Desktop\\up.xls",0)
    for i in range(nrows2-1):
        td.append(table2.cell(i+1,2).value)
        issuet.append(table2.cell(i+1,6).value)
    asize = []
    price = []
    for unit in range(50,1001,100):
        unit = unit*0.01
        print unit
        x_m = []
        nodesig = []
        avesize = []
        for batchnum in range(1,int(math.ceil(10/unit)+1)):
           df = getMatrix(dfm,unit,batchnum,0.5)
           Fleet,Fleetsize = compNetwork(df)
           dav = compDist(Fleet,df)
           avesize.append(Fleetsize)
           if dav == 0:
               continue
           else:
               x_min = optimize.fminbound(f, 0, 3)
               x_m.append(x_min)
               print x_min,Fleetsize 
        price.append(np.mean(x_m))
        asize.append(sum(avesize))
    
    
            
        