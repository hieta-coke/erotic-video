from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(max_length=150)
    thumb = models.ImageField(blank=True)
    iframe = models.TextField(null=True, blank=False)
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tag = models.TextField(blank=False)
    view = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=150)
    comment = models.TextField(null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name