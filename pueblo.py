#!/usr/local/bin/python
#
# Pueblo: Python Markdown Static Blogger
#
# 17 December 2011
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

config = {
	"directory": ".",
	"site_url": "http://yoursite.net/",
	"site_title": "Your Website",
	"site_description": "Your blog tagline.",
	"google_analytics_tag": "UA-111111-1",
	"author_name": "Your Name",
	"author_bio_link": "about.html",
	"amazon_tag": "mikesheanet-20",
	"twitter_tag": "twitterid",
	"author_email": "your@emailaddress.com",
	"header_image_url": "",
	"header_image_width": "",
	"header_image_height": "",
	"sidebar_on_article_pages": False,
	"minify_html": False,
}

nonentryfiles = []

# Main Program
import glob, re, rfc822, time, cgi, datetime, markdown
from time import gmtime, strftime, localtime, strptime
def rebuildsite ():
	textfiles = glob.glob(config["directory"]+"//*.txt")
	for nonfile in nonentryfiles:
		textfiles.remove(config["directory"]+"/"+nonfile)
	indexdata = []
	
	# Rip through the stack of .txt markdown files and build HTML pages from it.
	for eachfile in textfiles:
		eachfile = eachfile.replace(config["directory"]+"\\", "")
		content = open(eachfile).read()
		lines = re.split("\n", content)
		title = re.sub("(Title: )|(  )", "", lines[0])
		title = cgi.escape(title)
		urltitle = title.replace("&", "%26")
		author = lines[1].replace("Author: ","")
		date = re.sub("(  )|(\n)|(Date: )","",lines[2])
		numdate = strftime("%Y-%m-%d", strptime(date, "%d %B %Y"))
		content = markdown.markdown(re.sub("(Title:.*\n)|(Author:.*\n)|(Date:.*\n\n)|    ", "", content))
		summary = re.sub("<[^<]+?>","", content)
		summary = summary.replace("\n", " ")[0:200]
		htmlfilenamefull = htmlfilename = eachfile.replace(".txt", ".html")
		htmlfilename = htmlfilename.replace(config["directory"]+"/", "")
		postname = htmlfilename.replace(".html", "")
		# Build the HTML file, add a bit of footer text.
		htmlcontent = [buildhtmlheader("article", title, date)]
		htmlcontent.append(content)
		htmlcontent.append(buildhtmlfooter("article", urltitle))
		htmlfile = open(htmlfilenamefull, "w")
		htmlfile.write(minify("".join(htmlcontent)))
		htmlfile.close()
		if numdate <= datetime.datetime.now().strftime("%Y-%m-%d"):
			indexdata.append([[numdate],[title],[summary],[htmlfilename],[content]])

	# The following section builds index.html, archive.html and index.xml.	
	indexdata.sort()
	indexdata.reverse()
	indexbody=archivebody=rssbody=""
	count=0
	
	for indexrow in indexdata:
		dateobject = strptime(indexrow[0][0], "%Y-%m-%d")
		rssdate = strftime("%a, %d %b %Y 06:%M:%S +0000", dateobject)
		nicedate = strftime("%d %B %Y", dateobject)
		articleitem = """
<h2><a href="%(article_link)s">%(article_title)s</a></h2>
<p>%(date)s - %(summary)s...</p>
"""		% {
		'article_link': indexrow[3][0],
		'article_title': indexrow[1][0],
		'date': nicedate,
		'summary': indexrow[2][0],
		}

		rssitem = """
<item>
<title>%(title)s</title>
<link>%(link)s</link>
<guid>%(link)s</guid>
<pubDate>%(pubdate)s</pubDate>
<description>%(description)s</description>
<content:encoded>
<![CDATA[%(cdata)s]]>
</content:encoded>
</item>
"""		% {
		'title': indexrow[1][0],
		'link': config["site_url"]+indexrow[3][0],
		'pubdate': rssdate,
		'description': indexrow[2][0],
		'cdata': indexrow[4][0],
		}

		count = count + 1
		if count < 15:
			rssbody = rssbody + rssitem
		if count < 30:
			indexbody = indexbody+articleitem
		archivebody = archivebody + articleitem
	sidebardata = open(config["directory"]+"/sidebar.html").read()
	rssdatenow = rfc822.formatdate()

	indexdata = [buildhtmlheader("index", config["site_title"], "none")]
	indexdata.append(indexbody)
	indexdata.append("<h2><a href=\"archive.html\">View All %(article_count)s Articles</a></h2>\n</div>\n" 
		% { 'article_count': str(count) })
	indexdata.append(buildhtmlfooter("index", ""))
	indexfile = open(config["directory"]+"/index.html", "w").write(minify("".join(indexdata)))

	archivedata = [buildhtmlheader("archive", config["site_title"]+" Article Archive", "none")]
	archivedata.append(archivebody)
	archivedata.append("\n</div>\n")
	archivedata.append(buildhtmlfooter("archive", ""))
	archivefile = open (config["directory"]+"/archive.html", "w").write(minify("".join(archivedata)))

	rsscontent = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
xmlns:atom="http://www.w3.org/2005/Atom"
xmlns:content="http://purl.org/rss/1.0/modules/content/"
xmlns:dc="http://purl.org/dc/elements/1.1/\"
>

<channel>
<title>%(site_title)s</title>
<link>%(site_url)s</link>
<description>%(site_description)s</description>
<pubDate>%(rssdatenow)s</pubDate>
<language>en</language>
<atom:link href="%(site_url)sindex.xml" rel="self" type="application/rss+xml" />
%(rssbody)s
</channel>
</rss>
"""	% {
	'site_url': config["site_url"],
	'site_title': config["site_title"],
	'site_description': config["site_description"],
	'rssdatenow': rssdatenow,
	'rssbody': rssbody,
	}
	
	rssfile = open(config["directory"]+"/index.xml", "w").write(minify(rsscontent))
		
# Subroutine to build out the page's HTML header
# Edit this to build your own HTML output
def buildhtmlheader(type, title, date):
	if config["header_image_url"] != "":
		headerimage = """
<img class="headerimg" src="%(header_image_url)s" alt="%(site_title)s: %(site_description)s" height="%(header_image_height)s" width="%(header_image_width)s" />
""" 	% {
		'header_image_url': config["header_image_url"],
		'site_title': config["site_title"],
		'site_description': config["site_description"],
		'header_image_height': config["header_image_height"],
		'header_image_width': config["header_image_width"],
		}

	htmlheader = """
<!DOCTYPE html>
<html>
<head>
<title>%(title)s</title>
<link rel="stylesheet" type="text/css" media="screen and (min-width: 481px)" href="style.css">
<link rel="stylesheet" type="text/css" media="only screen and (max-width: 480px)" href="iphone.css">
<link rel="alternate" type="application/rss+xml" title="%(title)s" href="index.xml">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="user-scalable=no, width=device-width" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black" />
<script type="text/javascript">
var _gaq = _gaq || [];
_gaq.push(['_setAccount', '%(google_analytics_tag)s']);
_gaq.push(['_trackPageview']);
(function() {  var ga = document.createElement('script');
 ga.type = 'text/javascript';
 ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0];
s.parentNode.insertBefore(ga, s);
})();
</script>
</head>
<body>
""" 	% { 
		'title': title, 
		'google_analytics_tag': config["google_analytics_tag"], 
		}

	# Tons of conditional checks lay ahead. Does it use a header image and do you want the sidebar on article pages?
	if config["sidebar_on_article_pages"] != True and type == "article":
		htmlheader += "\n<div class=\"article_container\">\n"
	else:
		htmlheader += "\n<div class=\"container\">\n"
	if config["header_image_url"] != "" and type == "index":
		htmlheader += headerimage
	elif config["header_image_url"] != "" and type != "index":
		htmlheader += "<a href=\"/\">\n" + headerimage + "</a>\n"
	elif config["header_image_url"] == "" and type == "index":
		htmlheader += "<div class=\"header\">\n<h1>"+config["site_title"]+"</h1>\n<p>"+config["site_description"]+"</p>\n</div>"
	elif config["header_image_url"] == "" and type != "index":
		htmlheader += "\n<p class=\"return_link\"><a href=\"index.html\">"+config["site_title"]+"</a></p>\n"
	if type == "index":
		htmlheader += "\n<div class=\"article_list\">\n"
	elif type == "archive":
		htmlheader += "\n<div class=\"article_list\">\n<h1>Article Archive</h1>\n"
	elif type == "article":
		htmlheader += "\n<div class=\"article\">\n<h1>" + title + "</h1>\n<p>by <a href=\""+config["author_bio_link"]+"\">"+config["author_name"]+"</a> on " + date +"</p>\n"
	return htmlheader

# Subroutine to remove all line breaks to make for some packed fast HTML
def minify(content):
	if config["minify_html"]:
		content = re.sub("\n","",content)
	return content
	
# Subroutine to build out the footer.
def buildhtmlfooter (type, urltitle):
	footer_parts = []
	sidebardata = open(config["directory"]+"/sidebar.html").read()
	if type == "index" or type == "archive" or config["sidebar_on_article_pages"]:
		footer_parts.append(sidebardata)
	if type == "article":
		footer_parts.append(
'''
<p>Send feedback to <a href="mailto:%(email)s">%(email)s</a> or <a href="http://twitter.com/share?via=%(twitter_tag)s&text=%(urltitle)s">share on twitter</a>.</p>
''' 	
		% {
		'email': config['author_email'], 
		'twitter_tag': config['twitter_tag'], 
		'urltitle': urltitle,
		})
	footer_parts.append("\n</div>\n</body>\n</html>")
	return "".join(footer_parts)

# This program is designed to run as a CGI script so you can rebuild your site by hitting a URL.
print "Content-type: text/html\n\n"
rebuildsite()
print "<html><head><title>Site Rebuilt</title></head><body><h1>Site Rebuilt</h1></body></html>"