#!/usr/local/bin/python
#
# Pueblo: Python Markdown Static Blogger
#
# 15 December 2011
#
# A single Python script to build a simple blog from a directory full of markdown files.
#
# This script requires the Markdown python implementation available at:
# http://pypi.python.org/pypi/Markdown/2.1.0
#
# This script requires markdown files using the following multimarkdown metadata as the first three lines
# of the processed .txt markdown files as follows:
#
# Title: the Title of your Document
# Author: Joe Blow
# Date: 15 December 2011
#
# The program will generate an index.html homepage file, an archive.html archive file, 
# and an index.xml RSS file.
#
# Header and footer data can be edited in the variables throughout the program. 
#
# This script expects the following additional files:
# style.css: The main site's stylesheet.
# iphone.css: The mobile version of the site's stylesheet.
# sidebar.html: A secondary set of data usually displayed as a sidebar.
#
# Instructions
# Install the Markdown python module.
# Configure this script by changing the configuration variables below.
# Put your static markdown .txt files in the configured directory
# Run the script either manually, with a regular cronjob, or as a CGI script.
# View the output at index.html

# Configuration variables. Edit each of these to suit your site.
directory = "/your/public/directory/here" # Your markdown files and the output go here. No trailing slash.
nonentryfiles = [] # a list of text files you DON'T want to process.
site_url = "http://yoursite.net/" # site URL including an ending backslash.
site_title = "Your Website" # used for the RSS feed's title.
site_description = "Your blog tagline." # used for the RSS feed's description.
google_analytics_tag = "UA-111111-1" # used to track the site with Google Analytics.
author_name = "Your Name"
author_bio_link = "about.html" # relative or absolute depending on where you keep it.
amazon_tag = "mikesheanet-20" # Your tag to Amazon, used in the article footer and RSS feed.
twitter_tag = "twitterid" # The twitter tag to which you want tweeted articles referenced.
author_email = "your@emailaddress.com" # The feedback email address.
header_image_url = "" # Blank if no header image. (Default for style.css and iphone.css)
header_image_width = ""
header_image_height = ""
sidebar_on_article_pages = 0 # Show the sidebar on all pages. Anything but 1 will only show it on the homepage.
minify_html = 0 # set to 1 to remove line breaks from the HTML output

# Main Program
import glob, re, rfc822, time, cgi, datetime, markdown # The markdown module is the only non-default
from time import gmtime, strftime, localtime, strptime
def rebuildsite ():
	textfiles = glob.glob(directory+"//*.txt") # We're looking for text files in the primary directory
	for nonfile in nonentryfiles: textfiles.remove(directory+"/"+nonfile) # Except for non-entry files
	indexdata = [] # Define the index var
	
	# Rip through the stack of .txt markdown files and build HTML pages from it.
	for file in textfiles:
		file = file.replace(directory+"\\", "") # Remove the path from the file
		content = open(file).read() # Open up the file
		lines = re.split("\n", content) # We're going to split up the lines to grab Multimarkdown metadata.
		title = re.sub("(Title: )|(  )", "", lines[0]) # Grab the title off of the first line.
		title = cgi.escape(title) # Replace any ampersands with proper encoding.
		urltitle = title.replace("&", "%26") # ensure the url is encoded correctly
		author = lines[1].replace("Author: ","") # Remove the author line - we hardcode it for a single-author blog.
		date = re.sub("(  )|(\n)|(Date: )","",lines[2]) # Remove the flash around the Date. We just want the date itself.
		numdate = strftime("%Y-%m-%d", strptime(date, "%d %B %Y")) # Build the date from the remaining date text.
		content = markdown.markdown(re.sub("(Title:.*\n)|(Author:.*\n)|(Date:.*\n\n)|    ", "", content)) #process the resulting file through Markdown, remove title, author, and date lines.
		summary = re.sub("<[^<]+?>","", content) # For our summary, remove any HTML.
		summary = summary.replace("\n", " ")[0:200] # Remove linebreaks from the summary and limit it to 200 characters.
		htmlfilenamefull = htmlfilename = file.replace(".txt", ".html") # re-create the HTML filename by replacing .txt with .html
		htmlfilename = htmlfilename.replace(directory+"/", "") # Remove paths
		postname = htmlfilename.replace(".html", "") # Not sure why we need this...
		# Build the HTML file, add a bit of footer text.
		htmlfile = open(htmlfilenamefull, "w").write(minify(buildhtmlheader("article", title, date)+content+"<p>Send feedback to <a href=\"mailto:"+author_email+"\">"+author_email+"</a> or <a href=\"http://twitter.com/share?via="+twitter_tag+"&text="+urltitle+"\">share on twitter</a>.</p>"+buildhtmlfooter("article")))
		indexdata.append([[numdate],[title],[summary],[htmlfilename],[content]]) # Build a list of lists so we can sort all our entries.

	# The following section builds index.html, archive.html and index.xml.	
	indexdata.sort()
	indexdata.reverse()
	indexbody=archivebody=rssbody="" # Initiate all body strings.
	count=0 # Counter for index and RSS article increments
	
	for indexrow in indexdata:
		dateobject = strptime(indexrow[0][0], "%Y-%m-%d") # Create a date object
		rssdate = strftime("%a, %d %b %Y 06:%M:%S +0000", dateobject) # Generate an RSS friendly date format
		nicedate = strftime("%d %B %Y", dateobject) # Build a human-readable date format
		articleitem = "<h2><a href=\""+indexrow[3][0]+"\">"+indexrow[1][0]+"</a></h2>\n<p>"+nicedate+" - "+indexrow[2][0]+"...</p>\n" # Build out each article 
		rssitem = "<item>\n<title>"+indexrow[1][0]+"</title>\n<link>"+site_url+indexrow[3][0]+"</link>\n<guid>"+site_url+indexrow[3][0]+"</guid>\n<pubDate>"+rssdate+"</pubDate>\n<description>"+indexrow[2][0]+"</description>\n<content:encoded><![CDATA[\n"+indexrow[4][0]+"\n]]></content:encoded>\n</item>\n\n" # Generate each RSS article.
		count = count + 1 # Increment the counter
		if count < 15: rssbody = rssbody + rssitem # only do this many RSS items (15ish)
		if count < 30: indexbody = indexbody+articleitem # Only show this many articles on the home page (30ish)
		archivebody = archivebody + articleitem # Build an archive of all files
	sidebardata = open(directory+"/sidebar.html").read() # Load up an HTML chunk for the sidebar (stored in sidebar.html)
	rssdatenow = rfc822.formatdate() # Format the date in RFC822 for RSS
	indexfile = open (directory+"/index.html", "w").write(minify(buildhtmlheader("index", site_title, "none")+indexbody+"\n<h2><a href=\"archive.html\">View All "+str(count)+" Articles</a></h2>\n"+buildhtmlfooter("index"))) # Build the index.
	archivefile = open (directory+"/archive.html", "w").write(minify(buildhtmlheader("archive", site_title+" Article Archive", "none")+archivebody+"\n"+ buildhtmlfooter("archive"))) # Build the archive.
	rssfile = open(directory+"/index.xml", "w").write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<rss version=\"2.0\"\nxmlns:atom=\"http://www.w3.org/2005/Atom\"\nxmlns:content=\"http://purl.org/rss/1.0/modules/content/\"\nxmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n>\n\n<channel>\n<title>"+site_title+"</title>\n<link>"+site_url+"</link>\n<description>"+site_description+"</description>\n<pubDate>"+rssdatenow+"</pubDate>\n<language>en</language>\n<atom:link href=\""+site_url+"index.xml\" rel=\"self\" type=\"application/rss+xml\" />\n\n"+rssbody+"</channel>\n</rss>") # Build the RSS file
		
# Subroutine to build out the page's HTML header
# Edit this to build your own HTML output
def buildhtmlheader(type, title, date):
	if header_image_url is not "":
		headerimage = "<img class=\"headerimg\" src=\""+header_image_url+"\" alt=\""+site_title+": "+site_description+"\" height=\""+header_image_height+"\" width=\""+header_image_width+"\" />\n"
	htmlheader = "<!DOCTYPE html>\n<html>\n<head>\n<title>"+title+"</title>\n<link rel=\"stylesheet\" type=\"text/css\" media=\"screen and (min-width: 481px)\" href=\"style.css\">\n<link rel=\"stylesheet\" type=\"text/css\" media=\"only screen and (max-width: 480px)\" href=\"iphone.css\">\n<link rel=\"alternate\" type=\"application/rss+xml\" title=\"SlyFlourish.com\" href=\"index.xml\">\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n<meta name=\"viewport\" content=\"user-scalable=no, width=device-width\" />\n<meta name=\"apple-mobile-web-app-capable\" content=\"yes\" />\n<meta name=\"apple-mobile-web-app-status-bar-style\" content=\"black\" /><script type=\"text/javascript\">\nvar _gaq = _gaq || [];\n_gaq.push(['_setAccount', '"+google_analytics_tag+"']);\n_gaq.push(['_trackPageview']);\n(function() {  var ga = document.createElement('script');\n ga.type = 'text/javascript';\n ga.async = true;\nga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\nvar s = document.getElementsByTagName('script')[0];\ns.parentNode.insertBefore(ga, s);\n})();\n</script>\n</head>\n<body>\n"
	# Tons of conditional checks lay ahead. Does it use a header image and do you want the sidebar on article pages?
	if sidebar_on_article_pages is not 1 and type is "article":
		htmlheader += "\n<div class=\"article_container\">\n"
	else:
		htmlheader += "\n<div class=\"container\">\n"
	if header_image_url is not "" and type is "index":
		htmlheader += headerimage # show the header image without a link on the index page
	elif header_image_url is not "" and type is not "index":
		htmlheader += "<a href=\"/\">\n" + headerimage + "</a>\n" # show the header image with a hyperlink on all other pages
	elif header_image_url is "" and type is "index":
		htmlheader += "<div class=\"header\">\n<h1>"+site_title+"</h1>\n<p>"+site_description+"</p>\n</div>" # Show the site title w/o an image on the index
	elif header_image_url is "" and type is not "index":
		htmlheader += "\n<p class=\"return_link\"><a href=\"index.html\">"+site_title+"</a></p>\n" # Show a return link
	if type is "index":
		htmlheader += "\n<div class=\"article_list\">\n" # prep the article list
	elif type is "archive":
		htmlheader += "\n<div class=\"article_list\">\n<h1>Article Archive</h1>\n" # Prep the archive list
	elif type is "article":
		htmlheader += "\n<div class=\"article\">\n<h1>" + title + "</h1>\n<p>by <a href=\""+author_bio_link+"\">"+author_name+"</a> on " + date +"</p>\n" # Build the article section, author, and date.
	return htmlheader

# Subroutine to remove all line breaks to make for some packed fast HTML
def minify(content):
	if minify_html == 1:
		content = re.sub("\n","",content)
	return content
	
# Subroutine to build out the footer.
def buildhtmlfooter (type):
	sidebardata = open(directory+"/sidebar.html").read()
	htmlfooter = "\n</div>\n"
	if type is "index" or sidebar_on_article_pages == 1:
		htmlfooter += sidebardata
	htmlfooter += "</body>\n</html>"
	return htmlfooter

# This program is designed to run as a CGI script so you can rebuild your site by hitting a URL.
print "Content-type: text/html\n\n"
rebuildsite()
print "Site Rebuilt</body></html>"