#!/usr/bin/python3.4 
 
from datetime import datetime import time,json,requests,signal,sys,uuid from cassandra.cluster import Cluster 
 
class MyClient(object):  
  def __init__(self):   
    cluster = Cluster(['10.0.2.9','10.0.2.10',9042])   
    self.session = cluster.connect()      
    self.url = "http://10.0.2.11/zabbix/api_jsonrpc.php"   
    self.headers = {"Content-Type":"application/json-rpc"}  
    user = 'Admin'   
    password = 'zabbix'   
    self.login={       
      "jsonrpc": "2.0",      
      "method": "user.login",       
      "params": {    
        "user": user,    
        "password": password       
      },
      "id": 1,       
      "auth": None   
    }      
    
    self.insert_statement  = self.session.prepare("""      
      INSERT INTO spark.z (uid,timestamp,name,key, value, itemid,hostid)      
      VALUES (?,?,?,?,?,?,?);      
    """)     
    
  def authorization(self):      
    r = requests.post(self.url,headers=self.headers,json=self.login)   
    self.auth =(r.json())['result']    
    
  def json_data(self): ###json data for zabbix   
    group="Thesis servers"   
    self.memory = {  ###memory       
      "jsonrpc": "2.0", 
      "method": "item.get",       
      "params": {    
        "output": ["name","key_","lastvalue","lastclock","itemid","hostid"],    
        "group": group,    "application" : "Memory",         
      },       
      "auth": self.auth,       
      "id": 1   
    }     
    
    self.cpu = {  ###cpu       
      "jsonrpc": "2.0",       
      "method": "item.get",       
      "params": {    
        "output": ["name","key_","lastvalue","lastclock","itemid","hostid"],    
         "group": group,    
         "application" : "CPU",         
      },       
      "auth": self.auth,       
      "id": 1   
    } 
 
    self.disk = {  ###disk        
      "jsonrpc": "2.0",        
      "method": "item.get",        
      "params": {     
        "output": ["name","key_","lastvalue","lastclock","itemid","hostid"],     
        "group": group,     
        "application" : "Filesystems",          
      },        
      "auth": self.auth,        
      "id": 1    
    } 
 
    self.net = {  ###network        
      "jsonrpc": "2.0",        
      "method": "item.get",        
      "params": {     
        "output": ["name","key_","lastvalue","lastclock","itemid","hostid"],     
        "group": group,     
        "application" : "Network interfaces",          
      },        
      "auth": self.auth,        
      "id": 1    
    }     
  
  def get_data(self):     
    
    #get cpu data 

    r = requests.post(self.url,headers=self.headers,json=self.cpu)   
    self.x=r.json()['result'] 
 
    #get ram data   
  
    r = requests.post(self.url,headers=self.headers,json=self.memory)   
    self.y=r.json()['result'] 
 
    #get disk data   
    r = requests.post(self.url,headers=self.headers,json=self.disk)   
    self.z=r.json()['result']     
    
    #get network data   
    r = requests.post(self.url,headers=self.headers,json=self.net)   
    self.w=r.json()['result'] 
 
    result=self.x+self.y+self.z+self.w      
    for w in result:    
      self.session.execute(self.insert_statement,[uuid.uuid1(),int(w['lastclock']),w['name'], w['key_'],w['lastvalue'],int(w['itemid']),int(w["hostid"])]) 
 
  def end_session(self):   
    print('\nSession Closed')   
    self.session.cluster.shutdown()   
    sys.exit()    
    
  def main():  
    try:   
      client = MyClient()   
      while True:    
        start_time = time.time()  ###start time of execution    
        client.authorization()    
        client.json_data()    
        client.get_data()    
        exec_time = time.time()-start_time ###end time of execution    
        time.sleep(abs(5-exec_time))  
    except KeyboardInterrupt:   
      client.end_session()   
 
if __name__ == "__main__":  main() 
