import re
import csv
import base64
import datetime
import tldextract
import requests
import time
import hashlib
from requests import ConnectionError, HTTPError, Timeout
from bs4 import BeautifulSoup
from readability.readability import Document

from trove_python.trove_core import trove

from trovetraces.models import Backlink, Article, Page
from trovetraces.credentials import TROVE_API_KEY

PAGE_DIR = '/Users/tim/mycode/trovespace-django/trovespace/trovetraces/data/pages/'

def process_seo_links(file_path, start=0):
	backlink = Link()
	with open(file_path, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		for i, row in enumerate(reader):
			print i
			if i >= start:
				if re.match(r'http://trove\.nla\.gov\.au/ndp/del/article|http://nla\.gov\.au/nla\.news\-article', row[1]):
					backlink.process_page(row[0].strip())

class Link:

	def __init__(self):
		self.trove_api = trove.Trove(TROVE_API_KEY)

	def process_page(self, url):
		page = self.get_page(url)
		if page:
			
			self.page = page
			self.url = url
			self.soup = self.make_soup()
			links = self.get_links()
			print links
			if links:
				html, text = self.clean_html()
				checksum = self.create_checksum(html)
				linkpage, page_created = Page.objects.get_or_create(checksum=checksum)
				if page_created:
					title = self.get_title()
					print title
					domain, tld = self.get_domain()
					linkpage.url = url
					linkpage.page_title = title
					linkpage.domain = domain
					linkpage.tld = tld
					self.save_page(linkpage.id)
					html, text = self.clean_html()
					linkpage.cleaned_html = html
					linkpage.text = text
					linkpage.save()
				
					for href, trove_id, target, anchor, context in links:
						backlink, created = Backlink.objects.get_or_create( 
							href=href,
							anchor=anchor,
							context=context,
							#page=linkpage
							domain=domain 
						)
						if created:
							backlink.page = linkpage
							try:
								article = self.trove_api.get_item(item_id=trove_id, item_type='article')
							except trove.TroveItem.TroveException:
								Backlink.objects.filter(page=linkpage).delete()
								linkpage.delete()
								raise
							if article.record:
								article_details = article.get_details()
								year, month, day = article_details['date'].split('-')
								article_date = datetime.date(int(year), int(month), int(day))
								article, article_created = Article.objects.get_or_create(
									url=target,
									title=article_details['title'],
									date=article_date,
									page=article_details['page'],
									newspaper_id=article_details['newspaper_id'],
									newspaper_title=article_details['newspaper_title']
								)
								backlink.target = article
							backlink.save()
							time.sleep(1)
						else:
							#Replace archive or tags pages with item pages
							if re.search(r'/category/|/tag/|/archive/', backlink.page.url) and not re.search(r'/category/|/tag/|/archive/', url):
								backlink.page = linkpage
								backlink.save()

	def create_checksum(self, page_text):
		return hashlib.sha256(page_text.encode('utf-8')).hexdigest()

	def clean_html(self):
		html = Document(self.page.text).summary()
		soup = BeautifulSoup(html)
		try:
			text = soup.body.get_text()
		except AttributeError:
			text = ''
		return (html, text)

	def get_title(self):
		try:
			title = self.soup.find('title').string.strip()
		except AttributeError:
			try:
				title = self.soup.find('h1').string.strip()
			except:
				title = ''
		return title[:250]

	def get_domain(self):
		domains = tldextract.extract(self.url)
		if not domains[0] or domains[0].lower() == 'www':
			domain = '.'.join(domains[1:])
		elif 'blogspot' in domains[2]:
			domain = '{}.{}'.format(domains[1], 'blogspot')
		else:
			domain = '.'.join(domains)
		return (domain, domains[2])

	def get_sibling_words(self, siblings, direction):
		strings = []
		words = []
		for sibling in siblings:
			try:
				strings.append(sibling.get_text(' ', strip=True).strip().encode('utf-8'))
			except AttributeError:
				strings.append(unicode(sibling).encode('utf-8'))
		if direction == 'previous':
			strings = strings[::-1]
		for string in strings:
			words.extend(string.split())
		return words

	def get_context(self, link, number=100):
		anchor = '<span class="anchor">{}</span>'.format(' '.join(link.get_text().strip().split()).encode('utf-8'))
		before_words = self.get_sibling_words(link.previous_siblings, 'previous')
		if not before_words:
			before_words = self.get_sibling_words(link.parent.previous_siblings, 'previous')
		after_words = self.get_sibling_words(link.next_siblings, 'next')
		if not after_words:
			after_words = self.get_sibling_words(link.parent.next_siblings, 'next')
		before = before_words[0-number:] if len(before_words) > number else before_words
		after = after_words[:number] if len(after_words) > number else after_words 
		return '{} {} {}'.format(' '.join(before), anchor, ' '.join(after)).strip()

	def get_links(self):
		links = []
		for link in self.soup.find_all('a'):
			href = link.get('href')
			try:
				groups = re.match(r'http://trove\.nla\.gov\.au/ndp/del/article/(\d+)|http://nla\.gov\.au/nla\.news\-article(\d+)', href).groups()
				ids = [id for id in groups if id is not None]
				if ids:
					trove_id = ids[0]
					target = 'http://nla.gov.au/nla.news-article{}'.format(trove_id)
					anchor = ' '.join(link.get_text().strip().split())
					context = self.get_context(link)
					print context
					links.append([href, trove_id, target, anchor, context])
			except (TypeError, AttributeError) as e:
				pass
		return links

	def make_soup(self):
		soup = BeautifulSoup(self.page.text)
		for script in soup('script'):
			script.decompose()
		return soup

	def save_page(self, file_id):
		with open('{}{}.html'.format(PAGE_DIR, file_id), 'wb') as html_file:
			html_file.write(self.page.text.encode('utf-8'))

	def get_page(self, url):
		page = None
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',}
		try:
			page = requests.get(url, headers=headers, timeout=30)
		except Exception as e:
			print e
		return page