from django.db import models


class Post(models.Model):
    sender = models.CharField(max_length=100, blank=True)
    permalink = models.IntegerField()
    content = models.TextField(blank=True)
    media_urls = models.JSONField(blank=True, null=True)
    summary = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'



