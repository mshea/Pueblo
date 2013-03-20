## To Do:
## Redo CSS
## Test with full set of documents

import markdown
import jinja2
import re
import datetime
import time
import glob
import cgi

class Article:
	def __init__(self, local_dir, local_file):
		local_file = local_file.replace('/','')
		self.file_text = ''
		self.local_file_name = local_file
		with open(local_dir + '/' + local_file) as f:
			self.lines = f.readlines()
		self.file_text = ''.join(self.lines[4:])		

	def text(self):
		return self.file_text
	
	def title(self):
		title = self.lines[0].strip()
		title = re.sub('\n','',title)
		title = re.sub('Title: ','',title)
		title = cgi.escape(title)
		return title

	def html_filename(self):
		html_filename = re.sub('.txt','.html',self.local_file_name)
		return html_filename

	def author(self):
		title = self.lines[1].strip()
		title = re.sub('\n','',title)
		title = re.sub('Author: ','',title)
		return title

	def date_text(self):
		date_text = self.lines[2].strip()
		date_text = re.sub('\n','',date_text)
		date_text = re.sub('Date: ','',date_text)
		return date_text
	
	def date_datetime(self):
		date_txt = self.date_text()
		date_obj = datetime.datetime.strptime(date_txt, '%d %B %Y')
		return date_obj

	def date_rss(self):
		date = time.strptime(self.date_text(), '%d %B %Y')
		rss_date = time.strftime('%a, %d %b %Y 06:%M:%S +0000', date)
		return rss_date
		
	def summary(self):
		summary = re.sub('<[^<]+?>','', self.html())[0:200]
		summary = re.sub('\n',' ',summary)
		return summary
		
	def html(self):
		md = markdown.Markdown()
		converted_text = md.convert(self.file_text).encode('utf-8')
		return converted_text
		
class FileList:
	def __init__(self, dir, ignore_list):
		self.textfiles = glob.glob(dir+"/*.txt")
		for ignored_file in ignore_list:
			self.textfiles.remove(dir+ignored_file)

	def files(self):
		return self.textfiles
		
class Site:
	def load_article_data(self, dir, ignore_list):
		file_list = FileList(dir, ignore_list)
		articles = []
		for file in file_list.files():
			article = Article(dir, file.replace(dir,''))
			articles.append({
					'title': article.title(),
					'datetime': article.date_datetime(),
					'text': article.text(),
					'summary': article.summary(),
					'html': article.html(), 
					'date_text': article.date_text(),
					'html_filename': article.html_filename(),
					'date_rss': article.date_rss()
					},)
		articles = sorted(articles, key=lambda k: k['datetime'], reverse=True)
		return articles

	def build_html_page(self, data, template, output_file, dir):
		with open(template) as f:
			template = jinja2.Template(f.read())
		with open(dir + '/' + output_file,'w') as i:
			i.write(template.render(data = data))
		return True

	def build_site(self, params):
		dir = params['DIR']
		template_dir = params['TEMPLATE_DIR']
		index_template = template_dir + '/index_template.txt'
		archive_template = template_dir + '/archive_template.txt'
		rss_template = template_dir + '/rss_template.txt'
		article_template = template_dir + '/article_template.txt'
		index_output = '/index.html'
		archive_output = '/archive.html'
		rss_output = '/index.xml'		
		site = Site()
		
		articles = site.load_article_data(dir, params['IGNORE_LIST'])		
		for article in articles:
			output = article['html_filename']
			site.build_html_page(article, article_template, output, dir)
		site.build_html_page(articles, index_template, index_output, dir)
		site.build_html_page(articles, archive_template, archive_output, dir)
		site.build_html_page(articles, rss_template, rss_output, dir)	
		return True