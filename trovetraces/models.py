from django.db import models

# Create your models here.


class Page(models.Model):
	checksum = models.CharField(max_length=250)
	url = models.URLField(blank=True, null=True)
	page_title = models.CharField(max_length=250, blank=True, null=True)
	domain = models.CharField(max_length=100, blank=True, null=True)
	tld = models.CharField(max_length=20, blank=True, null=True)
	cleaned_html = models.TextField(blank=True, null=True)
	text = models.TextField(blank=True, null=True) 


class Article(models.Model):
	url = models.URLField()
	title = models.TextField()
	date = models.DateField()
	page = models.CharField(max_length=20)
	newspaper_id = models.CharField(max_length=10)
	newspaper_title = models.CharField(max_length=250)


class Backlink(models.Model):
	domain = models.CharField(max_length=100)
	href = models.TextField()
	target = models.ForeignKey(Article, blank=True, null=True)
	anchor = models.TextField(blank=True, null=True)
	context = models.TextField(blank=True, null=True)
	page = models.ForeignKey(Page, blank=True, null=True)


