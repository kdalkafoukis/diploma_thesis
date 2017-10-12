//script for analyzing cassandra tables with Apache Spark and stores results back to Apache Cassandra
//specific changes for readability reasons not sure if they run (eg. (21..27),(9..32),(42,44))


import com.datastax.spark.connector._ 
import org.apache.spark.SparkContext 
import org.apache.spark.SparkContext._ 
import org.apache.spark.SparkConf 
 
object SimpleApp {
  def main(args: Array[String]) { 
    //configuration to connect Spark with Cassandra cluster
    val conf = new SparkConf(true).set("spark.cassandra.connection.host", "10.0.2.9,10.0.2.10")
    val sc = new SparkContext("spark://10.0.2.7:7077", "analysis_1", conf)     
    val rdd= sc.cassandraTable("spark", "z")                         //connection with table z in db space spark
    val current_time=System.currentTimeMillis/1000.toInt     
    val n = 1     
    val myfilter = current_time-n*3600*24  
 
    //selects columns and filters timestamp (eg n=1 => one day) and keys
    val rdd2= rdd.select("hostid","value","itemid","key")        
      .where("timestamp>=? and timestamp<=?",myfilter,current_time)
      .filter(x=>x.getString("key")=="vm.memory.size[availa ble]" 
              || x.getString("key")== "system.cpu.util[,user]" 
              || x.getString("key")=="net.if.in[eth0]" 
              || x.getString("key")=="net.if.out[eth0]" 
              || x.getString("key")== "vfs.fs.size[/,used]"
             )    
//map choses the id of the host vm machince ,the item id ,the key and counts their value and the number of they show
//reduce counts both of the quantities
//collect starts the lazy process and ssves the results to an array
    val z  = rdd2       
                 .map(x=>((x.getInt("hostid"),x.getInt("itemid"),x.getString("key")),(x.getFloat("value"),1) )) 
                 .reduceByKey((x,y)=>(x._1 + y._1, x._2 + y._2))
                 .collect         
    
    def uuid = java.util.UUID.randomUUID         
    
    var myList = List[(java.util.UUID,Int,Int,String,Float)]()     //creates an empty list 
    
     //appends elements to the list , calculates the average of the above key values
    for (i<- z){       
      myList  = (uuid,current_time.toInt,i._1._1,i._1._3,i._2._1/i._2._2) :: myList      
    }      
    
    //save the list to Cassandra
    val x = sc
              .parallelize(myList)
              .saveToCassandra("spark","z_stats1",SomeColumns("uid"," timestamp","hostid","key","value"))
 
  } } 
