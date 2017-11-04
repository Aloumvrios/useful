import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.slf4j.ext.XLogger;
import org.slf4j.ext.XLoggerFactory;

public class Parser {

	private final XLogger logger = XLoggerFactory.getXLogger(this.getClass());

	/*
	 * Purpose: Parser search input string for a specific regex
	 * expression(keyword) Input: keyword -> regex String | input -> input
	 * string from collector Output: ArrayList containing the matches of the
	 * regex(keyword) with all groups
	 */

	public ArrayList<ArrayList<String>> returnNonZeroGroups(String keyword, String input) {

		logger.entry();

		Pattern pattern = Pattern.compile(keyword, Pattern.MULTILINE | Pattern.DOTALL);
		Matcher matcher = pattern.matcher(input);
		ArrayList<ArrayList<String>> match = new ArrayList<ArrayList<String>>();
		while (matcher.find()) {
			ArrayList<String> groups = new ArrayList<String>();

			logger.debug("keyword:{}", keyword);
			logger.debug("group count " + matcher.groupCount());
			for (int i = 0; i <= matcher.groupCount(); i++) {
				if (i == 0) {
					groups.add("group 0 not handled");
				} else {
					logger.debug("for index " + i + " " + matcher.group(i) + " to be added");
					groups.add(matcher.group(i));
					logger.debug("groups size " + groups.size());
				}

			}
			match.add(groups);
			logger.debug("matcher size:" + match.size());

		}

		logger.debug("final matcher size:" + match.size());

		logger.exit();
		return match;

	}
