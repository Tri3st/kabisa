from django.db import models


# Create your models here.
class Quote(models.Model):
    author = models.CharField(max_length=100)
    quote = models.TextField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.author
