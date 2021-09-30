from django import forms
from django.db import models
from ckeditor.fields import RichTextField
import stripe

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
    stripe_id = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100)
    airtable_url = models.URLField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to="bundle_images", null=True, blank=True)
    price = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            product = stripe.Product.create(name=self.name,
                                            metadata={
                                                'id': self.id
                                            })
            self.stripe_id = product.id
        else:
            product = stripe.Product.update(self.stripe_id, name=self.name, images=[
                                            self.image.url] if self.image else [])
        super(Bundle, self).save(*args, **kwargs)
