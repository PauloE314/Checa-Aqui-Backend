from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from products.models import Product

import config

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="reviews")
    store = models.CharField(max_length=20, choices=config.STORES)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews")
    description = models.TextField(blank=True, default=None, null=True)

    grade = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    like_users = models.ManyToManyField(User, related_name="liked_reviews", blank=True)


    @property
    def likes(self):
        return len(self.like_users.all())

    def __str__(self):
        return f"product: {self.product} - author: {self.author} - grade: {self.grade}"