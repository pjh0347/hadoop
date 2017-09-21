import java.io.IOException;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.MasterNotRunningException;
import org.apache.hadoop.hbase.client.HBaseAdmin;

public class AddColumn{

   public static void main(String args[]) throws MasterNotRunningException, IOException{

      // Instantiating configuration class.
      Configuration conf = HBaseConfiguration.create();

      // Instantiating HBaseAdmin class.
      HBaseAdmin admin = new HBaseAdmin(conf);

      // Instantiating columnDescriptor class
      HColumnDescriptor columnDescriptor = new HColumnDescriptor("contactDetails");
      
      // Adding column family
      admin.addColumn("emp", columnDescriptor);
      System.out.println("coloumn added");
   }
}
