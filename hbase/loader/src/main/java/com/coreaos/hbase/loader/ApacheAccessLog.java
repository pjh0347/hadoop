package com.coreaos.hbase.loader;

import java.lang.String;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Apache Access Log Class
 * 
 * @author pjh0347
 *
 */
public class ApacheAccessLog {

	private static final String LOG_FORMAT =
			"^(\\S+)" + 							// 1: address
			" (\\S+)" + 							// 2: identity
			" (\\S+)" + 							// 3: user
			" \\[([\\w:/]+\\s[+\\-]\\d{4})\\]" + // 4: time
			" \"(\\S+)?" + 						// 5: method
			" ?(\\S+)?" + 						// 6: url
			" ?(\\S+)?\"" + 						// 7: protocol
			" (\\d{3})" + 						// 8: code
			" ([\\d-]+)" + 						// 9. size
			" ?\"?([^\"]+)?\"?" + 				// 10. referer
			" ?\"?([^\"]+)?\"?"  				// 11. agent
			;
	private static final Pattern LOG_PATTERN = Pattern.compile(LOG_FORMAT);

	private static final SimpleDateFormat logDateFormat = new SimpleDateFormat("dd/MMM/yyyy:HH:mm:ss Z");
	private static final SimpleDateFormat textDateFormat = new SimpleDateFormat("yyyyMMddHHmmss");

	private String address;
	private String identity;
	private String user;
	private String time;
	private String method;
	private String url;
	private String protocol;
	private String code;
	private String size;
	private String referer;
	private String agent;

	public ApacheAccessLog(String address, String identity, String user, String time, String method, String url,
			String protocol, String code, String size, String referer, String agent) {
		this.address = address;
		this.identity = identity;
		this.user = user;
		this.time = time;
		this.method = method;
		this.url = url;
		this.protocol = protocol;
		this.code = code;
		this.size = size;
		this.referer = referer;
		this.agent = agent;
	}

	public static ApacheAccessLog parse(String line) throws ParseException {

		Matcher matcher = LOG_PATTERN.matcher(line);

		if (!matcher.find()) {
			System.out.println("apache access log parsing error : " + line);
			return null;
		}

		Date date = logDateFormat.parse(matcher.group(4));
		String time = textDateFormat.format(date);
		String size = "-".equals(matcher.group(9)) ? "0" : matcher.group(9);

		return new ApacheAccessLog(matcher.group(1), matcher.group(2), matcher.group(3), time, matcher.group(5),
				matcher.group(6), matcher.group(7), matcher.group(8), size, matcher.group(10), matcher.group(11));
	}

	@Override
	public String toString() {
		return "ApacheAccessLog [address=" + address + ", identity=" + identity + ", user=" + user + ", time=" + time
				+ ", method=" + method + ", url=" + url + ", protocol=" + protocol + ", code=" + code + ", size=" + size
				+ ", referer=" + referer + ", agent=" + agent + "]";
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

	public String getIdentity() {
		return identity;
	}

	public void setIdentity(String identity) {
		this.identity = identity;
	}

	public String getUser() {
		return user;
	}

	public void setUser(String user) {
		this.user = user;
	}

	public String getTime() {
		return time;
	}

	public void setTime(String time) {
		this.time = time;
	}

	public String getMethod() {
		return method;
	}

	public void setMethod(String method) {
		this.method = method;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getProtocol() {
		return protocol;
	}

	public void setProtocol(String protocol) {
		this.protocol = protocol;
	}

	public String getCode() {
		return code;
	}

	public void setCode(String code) {
		this.code = code;
	}

	public String getSize() {
		return size;
	}

	public void setSize(String size) {
		this.size = size;
	}

	public String getReferer() {
		return referer;
	}

	public void setReferer(String referer) {
		this.referer = referer;
	}

	public String getAgent() {
		return agent;
	}

	public void setAgent(String agent) {
		this.agent = agent;
	}

}
