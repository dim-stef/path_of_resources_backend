from django import forms
from django.contrib.admin import ModelAdmin
from django.forms.fields import CharField
from django.forms.widgets import Textarea
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib import admin
from .models import Paper, Bundle, BundleType

# Register your models here.
class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        exclude = ['papers']


class BundleAdmin(admin.ModelAdmin):
    form = BundleForm


admin.site.register(Bundle)
admin.site.register(BundleType)
