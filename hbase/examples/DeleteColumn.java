import java.io.IOException;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.MasterNotRunningException;
import org.apache.hadoop.hbase.client.HBaseAdmin;

public class DeleteColumn{

   public static void main(String args[]) throws MasterNotRunningException, IOException{

      // Instantiating configuration class.
      Configuration conf = HBaseConfiguration.create();

      // Instantiating HBaseAdmin class.
      HBaseAdmin admin = new HBaseAdmin(conf);

      // Deleting a column family
      admin.deleteColumn("emp","contactDetails");
      System.out.println("coloumn deleted"); 
   }
}
