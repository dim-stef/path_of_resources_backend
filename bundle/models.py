from django import forms
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import stripe
import uuid

# Create your models here.

class BundleType(models.Model):
    class Meta:
        ordering = ['-updated_at',]

    surrogate = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=100, default="")
    slug = models.CharField(max_length=120, default="")
    image = models.ImageField(upload_to="bundle_type_images", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BundleType, self).save(*args, **kwargs)


class Paper(models.Model):
    url = models.URLField()
    nickname = models.CharField(max_length=250)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.url


class Bundle(models.Model):
    class Meta:
        ordering = ['-updated_at',]

    surrogate = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    bundle_type = models.ForeignKey(BundleType, on_delete=models.CASCADE, null=True, blank=True, related_name="bundles")
    stripe_id = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=120, default="")
    airtable_url = models.URLField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to="bundle_images", null=True, blank=True)
    price = models.IntegerField(default=0)
    price_id = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.stripe_id:
            product = stripe.Product.create(name=self.name, metadata={
                'id': self.id
            })
            self.stripe_id = product.id
        # else:
        #     product = stripe.Product.update(self.stripe_id, name=self.name, images=[
            # self.image.url] if self.image else [])
        super(Bundle, self).save(*args, **kwargs)
