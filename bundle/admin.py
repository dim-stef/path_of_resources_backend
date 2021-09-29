from django.contrib.admin import ModelAdmin
from django.forms.fields import CharField
from django.forms.widgets import Textarea
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib import admin
from .models import Paper, Bundle

# Register your models here.
admin.site.register(Bundle)