#!/usr/local/bin/python

import pueblo

PARAMS = {
	'DIR': '/dir/to/your/html/files/',
	'TEMPLATE_DIR': '/dir/to/store/your/templates/',
	'IGNORE_LIST': ['ignorethis.txt'],
	'PAGEBUILD_DELTA': 30
	}

print "Content-type: text/html\n\n"

site = pueblo.Site()
site.build_site(PARAMS)

print "<html><head><title>Site Rebuilt</title></head><body><h1>Site Rebuilt</h1></body></html>"

