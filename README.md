# Diploma Thesis

__A platform for monitoring cloud infrastructures by the infrastructure administrator.Completed on June, 2016.__

__In a few words:  
The platform that works in the Cloud Infrastructure, gathers Logs from Openstack & Zabbix elements and stores them
  to Apache Cassandra which is a NoSQL database and Apache Spark on top of Cassandra does batch analysis__
  
  
__This repository has been created to show samples of the architecture & code, of the platform.__

 ## Programming Languages, Libraries, Api's and Frameworks were used:

* Python 3.4 

* Scala 2.10.4 

* Java 1.8.0_72-b15 

* ApacheSpark 1.5.2 

* Apache Cassandra 3.2 

* Zabbix 3.0 

* Spark Cassandra Connector 1.5.0 DataStax Python Driver for Apache Cassandra 3.0.0 

* Requests 2.9.1

 ## Architecture
![Image of Architecture](https://github.com/kdalkafoukis/diploma_thesis/blob/master/platform_arch.PNG)

- [**Monitoring Service**](http://github.com)
This service is responisble for the collection (through Zabbix Rest Api) and forwarding of Zabbix Data from VM's to Cassandra

- [**Log Service**](http://github.com)
This service parses Openstack log files to Cassandra.

- [**Data Analysis Service**](http://github.com)
This service uses Spark on top of Cassandra to analyze data.

- [**Administration Interconnection Service**](http://github.com)
This services is responsible to represent the requested queries about the Cloud infrastracture to the administrator of the infrastructure

