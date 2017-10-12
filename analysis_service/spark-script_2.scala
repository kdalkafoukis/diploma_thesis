
import com.datastax.spark.connector._ 
import org.apache.spark.SparkContext 
import org.apache.spark.SparkContext._ 
import org.apache.spark.SparkConf 
 
object SimpleApp {   

  def main(args: Array[String]) { 
 
    val conf = new SparkConf(true).set("spark.cassandra.connection.host", "10.0.2.9,10.0.2.10")     
    
    val sc = new SparkContext("spark://10.0.2.7:7077", "analysis_2", conf)     
    val rdd= sc.cassandraTable("spark", "z")          
    
    val current_time=System.currentTimeMillis/1000.toInt     
    val n = 1     //one day
    val myfilter = current_time-n*3600*24  //one day with n=1
    
    val lim : Float = 30 //current limit is 30
 
    val rdd2= rdd
                  .select("hostid","itemid","value", "key")
                  .where("timestamp>=? and timestamp<=?",myfilter,current_time)
                  .filter(x=> x.getString("key")== "system.cpu.util[,user]")          // choses for cpu utilization per user
    
    //map  if value passes threshold (here 30 count it) + count values per hostid
    //reduceByKey groups the data 
    val z  = rdd2
                  .map(x=>(x.getInt("hostid"),(if(x.getFloat("value")>=lim) 1 else 0,1)))   
                  .reduceByKey((x,y)=>(x._1 + y._1,x._2 + y._2))
                  .collect          
    
    def uuid = java.util.UUID.randomUUID 
 
    var myList = List[(java.util.UUID,Int,Int,Float,Float)]()     
    
    // the list has the UUID,the time,the hostid,the threshold we had and the percentage of the time that is happend (here in a day)
    for (i<- z){       
      myList  = (uuid,current_time.toInt,i._1,lim,i._2._1.toFloat/i._2._2.toFloat) :: myList         
    
    val x = sc
              .parallelize(myList)
              .saveToCassandra("spark","z_stats2",SomeColumns("uid"," timestamp","hostid","lim","value")) 
 
 } }
