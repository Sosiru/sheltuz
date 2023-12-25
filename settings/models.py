from django.db import models

from base.models import BaseModel


# Create your models here.
class SiteSetting(BaseModel):
	page_link = models.CharField(max_length=300)
	seo_txt = models.CharField(max_length=200)
	seo_keyword = models.TextField(default="...")
	author = models.CharField(max_length=50, default="sheltuz")

	def __str__(self):
		return self.seo_txt