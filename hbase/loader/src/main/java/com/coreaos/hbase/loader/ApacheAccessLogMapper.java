package com.coreaos.hbase.loader;

import java.io.IOException;
import java.time.Instant;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * <pre>
 * The mapper implementation which maps parsed Apache access log into HBase Put object to make HFile.
 * 
 * I think that storing log data into HBase is not the best practice for HBase usage.
 * When querying on the log, we usually set some conditions on columns rather than use row key.
 * But we should pass row key to retrieve efficiently in HBase. 
 * Besides, it doesn't provide secondary index feature basically.
 * 
 * Row key design:
 * I added timestamp and client address to distribute data as much as possible.
 * And I put timestamp - generated on map task - into the Put object to version on the same row key. 
 * </pre>
 * 
 * @author pjh0347
 *
 */
public class ApacheAccessLogMapper extends Mapper<LongWritable, Text, ImmutableBytesWritable, Put> {

	private static final byte[] time = Bytes.toBytes("time");
	private static final byte[] client = Bytes.toBytes("client");
	private static final byte[] server = Bytes.toBytes("server");
	private static final byte[] request = Bytes.toBytes("request");
	private static final byte[] response = Bytes.toBytes("response");
	private static final byte[] address = Bytes.toBytes("address");
	private static final byte[] identity = Bytes.toBytes("identity");
	private static final byte[] user = Bytes.toBytes("user");
	private static final byte[] agent = Bytes.toBytes("agent");
	private static final byte[] method = Bytes.toBytes("method");
	private static final byte[] url = Bytes.toBytes("url");
	private static final byte[] protocol = Bytes.toBytes("protocol");
	private static final byte[] referer = Bytes.toBytes("referer");
	private static final byte[] code = Bytes.toBytes("code");
	private static final byte[] size = Bytes.toBytes("size");
	
	private String serverAddress = null;

	public void setup(Context context) {
		Configuration conf = context.getConfiguration();
		serverAddress = conf.get("hbase.loader.serverAddress");
	}

	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		
		try {
			ApacheAccessLog log = ApacheAccessLog.parse(value.toString());
			
			if (log == null) {
				return ;
			}
			
			byte[] rowKey = createRowKey(log.getTime(), log.getAddress());
			
			long ts = System.nanoTime();
			
			Put put = new Put(rowKey);
			put.addColumn(time,     time,     ts, toBytes(log.getTime()));
			put.addColumn(client,   address,  ts, toBytes(log.getAddress()));
			put.addColumn(client,   identity, ts, toBytes(log.getIdentity()));
			put.addColumn(client,   user,     ts, toBytes(log.getUser()));
			put.addColumn(client,   agent,    ts, toBytes(log.getAgent()));
			put.addColumn(server,   address,  ts, toBytes(serverAddress));
			put.addColumn(request,  method,   ts, toBytes(log.getMethod()));
			put.addColumn(request,  url,      ts, toBytes(log.getUrl()));
			put.addColumn(request,  protocol, ts, toBytes(log.getProtocol()));
			put.addColumn(request,  referer,  ts, toBytes(log.getReferer()));
			put.addColumn(response, code,     ts, toBytes(log.getCode()));
			put.addColumn(response, size,     ts, toBytes(log.getSize()));
			context.write(new ImmutableBytesWritable(rowKey), put);
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private byte[] createRowKey(String time, String address) {
		String rowKey = time + "-" + address;
		return Bytes.toBytes(rowKey);
	}
	
	private byte[] toBytes(String str) {
		if (str == null) {
			return null;
		} else {
			return Bytes.toBytes(str);
		}
	}
	
}
