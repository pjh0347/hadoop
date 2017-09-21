import java.io.IOException;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.MasterNotRunningException;
import org.apache.hadoop.hbase.client.HBaseAdmin;

public class DisableTable{

   public static void main(String args[]) throws MasterNotRunningException, IOException{

      // Instantiating configuration class
      Configuration conf = HBaseConfiguration.create();
 
      // Instantiating HBaseAdmin class
      HBaseAdmin admin = new HBaseAdmin(conf);

      // Verifying weather the table is disabled
      Boolean bool = admin.isTableDisabled("emp");
      System.out.println(bool);

      // Disabling the table using HBaseAdmin object
      if(!bool){
         admin.disableTable("emp");
         System.out.println("Table disabled");
      }
   }
}
