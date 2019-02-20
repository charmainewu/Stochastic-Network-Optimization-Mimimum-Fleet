# -*- coding: cp936 -*-
#find the up and down point

f = open('C:\\Users\\jmwu\\Desktop\\TaxiData.csv','r')
up = open('C:\\Users\\jmwu\\Desktop\\up.csv','w')
down = open('C:\\Users\\jmwu\\Desktop\\down.csv','w')
arr_bef = []
arr_cur = []
user_id = 0

for line in f:
    arr_cur = line.split(',')
    
    if arr_bef==[]:
        arr_bef = arr_cur
        continue
    
    elif arr_cur[0]==arr_bef[0] and arr_cur[2]==arr_bef[2]:
        arr_bef = arr_cur    
        continue
    
    elif arr_cur[0]!=arr_bef[0]:
        if arr_cur[2] == '1':
            up.writelines(str(user_id)+','+arr_cur[0]+','+arr_cur[1]+','
                            +arr_cur[2]+','+arr_cur[3]+','+arr_cur[4]+'\n')
        if arr_bef[2] == '1':
            down.writelines(str(user_id)+','+arr_bef[0]+','+arr_bef[1]+','
                            +arr_bef[2]+','+arr_bef[3]+','+arr_bef[4]+'\n')
            user_id = user_id + 1
        arr_bef = arr_cur
        continue
        
    elif arr_cur[0]== arr_bef[0] and arr_cur[2]!=arr_bef[2] and arr_bef[2]=='0':
        up.writelines(str(user_id)+','+arr_cur[0]+','+arr_cur[1]+','
                      +arr_cur[2]+','+arr_cur[3]+','+arr_cur[4]+'\n')
        
    elif arr_cur[0]== arr_bef[0] and arr_cur[2]!=arr_bef[2] and arr_bef[2]=='1':
        down.writelines(str(user_id)+','+arr_cur[0]+','+arr_cur[1]+','
                        +arr_cur[2]+','+arr_cur[3]+','+arr_cur[4]+'\n')
        user_id = user_id + 1
        
    arr_bef = arr_cur

down.writelines(str(user_id)+','+arr_cur[0]+','+arr_cur[1]+','
                        +arr_cur[2]+','+arr_cur[3]+','+arr_cur[4]+'\n')
  
f.close()
up.close()    
down.close()


        
        
        
        
        
        
        








