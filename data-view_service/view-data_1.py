#!/usr/bin/python3.4 
# -*- coding: utf-8 -*- 
 
from cassandra.cluster import Cluster import time,sys from datetime import datetime 
 
 
cluster = Cluster(['10.0.2.9','10.0.2.10']) session = cluster.connect() 
 
results = session.execute("SELECT hostid,value,key,timestamp  FROM spark.z_stats1 ") current_time =int(time.time()) week_time= current_time-int(sys.argv[1])*3600*24 a=[] for row in results:  if (row.timestamp>= week_time and row.key=='system.cpu.util[,user]'): 
 
 a.append((row.timestamp,datetime.fromtimestamp(row.timestamp).strftime('%d %b %y'),row.hostid,row.value)) a.sort(key=lambda x:(x[2],x[0])) 
 
print('CPU AVG') for x in a:  print(x[1],x[2],x[3] ,'%') session.cluster.shutdown() 
 
