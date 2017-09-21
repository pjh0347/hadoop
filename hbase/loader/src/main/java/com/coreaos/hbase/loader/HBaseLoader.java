package com.coreaos.hbase.loader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.RegionLocator;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.HFileOutputFormat2;
import org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles;
import org.apache.hadoop.io.compress.SnappyCodec;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/**
 * <pre>
 * HBase Loader
 * 
 * Description:
 * This is an example of HBase loader demonstrating how to load Apache Access Log file on the HDFS into HBase.
 * Appropriate parser and mapper should be implemented depends on the applications.
 * 
 * Usage:
 * hadoop jar hbase-loader-0.0.1-SNAPSHOT-jar-with-dependencies.jar \
 *     com.coreaos.hbase.loader.HBaseLoader \
 *     -D hbase.loader.tableName=&lt;HBase Table Name&gt; \
 *     -D hbase.loader.inputPath=&lt;HDFS file path&gt; \
 *     -D hbase.loader.hFilePath=&lt;Temporary HFile path&gt; \
 *     -D hbase.loader.serverAddress=&lt;Server Host&gt;
 * </pre>
 * 
 * @author pjh0347
 *
 */
public class HBaseLoader extends Configured implements Tool {

	public static void main(String[] args) throws Exception {
		int exitCode = ToolRunner.run(HBaseConfiguration.create(), new HBaseLoader(), args);
		System.exit(exitCode);
	}

	@Override
	public int run(String[] arg0) throws Exception {
		
		// configuration
		Configuration conf = getConf();
		HBaseConfiguration.addHbaseResources(conf);
		
		// variable initialization
		String tableName = conf.get("hbase.loader.tableName");
		String jobName = "HBaseLoader::" + tableName;
		Path inputPath = new Path(conf.get("hbase.loader.inputPath"));
		Path hFilePath = new Path(conf.get("hbase.loader.hFilePath"));

		// job setting
		Job job = Job.getInstance(conf);
		job.setJarByClass(HBaseLoader.class);
		job.setJobName(jobName);
		job.setInputFormatClass(TextInputFormat.class);
		job.setMapOutputKeyClass(ImmutableBytesWritable.class);
		job.setMapOutputValueClass(Put.class);
		job.setMapperClass(ApacheAccessLogMapper.class);
		job.setOutputFormatClass(HFileOutputFormat2.class);
		FileInputFormat.addInputPath(job, inputPath);
		FileOutputFormat.setOutputPath(job, hFilePath);

		try (
			// preparing for HBase usage
			Connection conn = ConnectionFactory.createConnection(conf);
			Admin admin = conn.getAdmin();
			Table table = conn.getTable(TableName.valueOf(tableName));
			RegionLocator regionLocator = conn.getRegionLocator(TableName.valueOf(tableName));
		) {
			// HFile configuration
			HFileOutputFormat2.configureIncrementalLoad(job, table, regionLocator);
			HFileOutputFormat2.setOutputPath(job, hFilePath);
			HFileOutputFormat2.setCompressOutput(job, true);
			HFileOutputFormat2.setOutputCompressorClass(job, SnappyCodec.class);
			
			// make HFile
			if (!job.waitForCompletion(true)) {
				System.out.println("Loading failed.");
				return 1;
			}
			
			// load HFile
			LoadIncrementalHFiles loadIncrementalHFiles = new LoadIncrementalHFiles(conf);
			loadIncrementalHFiles.doBulkLoad(hFilePath, admin, table, regionLocator);
			
			// delete HFile
			FileSystem.get(conf).delete(hFilePath, true);
		}

		System.out.println("Loading completed successfully.");
		return 0;
	}

}
