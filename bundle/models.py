from djongo import models
from django import forms

# Create your models here.


class Paper(models.Model):
    url = models.URLField()
    nickname = models.CharField(max_length=250)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.url


class Bundle(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="bundle_images", null=True, blank=True)
    papers = models.ArrayField(
        model_container=Paper,
    )
