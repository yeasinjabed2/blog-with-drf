from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    tags = models.TextField()

    def __str__(self):
        return self.title
