import markdown
import jinja2
import re
import datetime
import time
import glob
import cgi
import os

class Article(object):
	def __init__(self, file):
		md = markdown.Markdown()
		with open(file) as f:
			self.lines = f.readlines()
		fulltext = ''.join(self.lines)
		self.text = ''.join(self.lines[4:])
		self.html_filename = os.path.basename(file).replace('.txt','.html')
		self.title = cgi.escape(
				re.search('Title: (.*)\n',fulltext).group(1).strip()
				)
		self.date_txt = re.search('Date: (.*)\n',fulltext).group(1).strip()
		self.author = re.search('Author: (.*)\n',fulltext).group(1).strip()
		self.datetime = datetime.datetime.strptime(self.date_txt, '%d %B %Y')
		self.html = md.convert(self.text).encode('utf-8')
		self.summary = re.sub('<[^<]+?>','', 
				self.html)[0:200].replace('\n', ' ')
		date = time.strptime(self.date_txt, '%d %B %Y')
		self.date_rss = time.strftime('%a, %d %b %Y 06:%M:%S +0000', date)
	
class Site(object):
	def get_files(self, dir, ignore_list):
		textfiles = glob.glob(os.path.join(dir, '*.txt'))
		for ignored_file in ignore_list:
			textfiles.remove(dir+ignored_file)
		return textfiles

	def load_articles(self, dir, ignore_list):
		articles = []
		for file in self.get_files(dir, ignore_list):
			article = Article(file)
			if article.datetime < datetime.datetime.now():
				articles.append(article)
		articles.sort(key=lambda k: k.datetime, reverse=True)
		return articles

	def build_from_template(self, data, template, output_file, dir):
		with open(template) as f:
			template = jinja2.Template(f.read())
		with open(os.path.join(dir, output_file),'w') as i:
			i.write(template.render(data = data))

	def build_site(self, params):
		article_template = os.path.join(params['TEMPLATE_DIR'], 
				'article_template.html')
		site = Site()
		articles = site.load_articles(params['DIR'], params['IGNORE_LIST'])		
		for article in articles:
			output = article.html_filename
			if article.datetime > datetime.datetime.now() - datetime.timedelta(
					days=params['PAGEBUILD_DELTA']):
				site.build_from_template(article, article_template, output, 
						params['DIR'])

		pages_to_build = (
			(os.path.join(params['TEMPLATE_DIR'], 'index_template.html'),
				'index.html'),
			(os.path.join(params['TEMPLATE_DIR'], 'archive_template.html'),
				'archive.html'),
			(os.path.join(params['TEMPLATE_DIR'], 'rss_template.xml'),
				'index.xml')
			)
		for page in pages_to_build:
			site.build_from_template(articles, page[0], page[1], 
					params['DIR'])