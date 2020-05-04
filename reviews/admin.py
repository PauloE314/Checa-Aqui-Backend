from django.contrib import admin
# from django.contrib.admin.site import register
# Register your models here.
from reviews.models import Review

admin.site.register(Review)
