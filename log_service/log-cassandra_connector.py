#!/usr/bin/python3.4 
 
 '''
 This script parses the bellow log file into Cassandra
 '''
 
import time,linecache,sys,signal,uuid 
from cassandra.cluster import Cluster 
 
filename = 'Server_Logs/nova_controller/nova-api.log.1' 
x=1 #old lines 
y=1 #new lines 
cluster = Cluster(['10.0.2.9','10.0.2.10',9042]) 
session = cluster.connect() 
insert_statement  = session.prepare("""  INSERT INTO spark.logs_1 (
 uid,date,time,id,priority,service,host,info)  VALUES (?,?,?,?,?,?,?,?);         
 """) 
 
while True:  
 try:     
  with open(filename, 'r') as f:    
   x=y    
   y=sum(1 for _ in f)+1   
   if y<x:   
    x=1 
 
  for i in range(x,y):    
   l=linecache.getline(filename,i).rstrip()    
   l2=l.split()    
   session.execute(insert_statement,[uuid.uuid1(),l2[0],     l2[1],l2[2],l2[3],l2[4],l2[6]," ".join(l2[7:])])   
   linecache.clearcache()   
   time.sleep(5)      
   
 except KeyboardInterrupt:   
  print('Session closed')   
  session.cluster.shutdown()   
  sys.exit()
