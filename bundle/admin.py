from django import forms
from django.contrib import admin
from .models import Paper, Bundle, BundleType

# Register your models here.


class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        exclude = ['papers']


class BundleAdmin(admin.ModelAdmin):
    list_display = ('surrogate', 'created_at', 'updated_at',
                    'bundle_type', 'stripe_id', 'name', 'slug', 
                    'airtable_url', 'description', 'image', 'price', 
                    'price_id')


admin.site.register(Bundle)
admin.site.register(BundleType)
