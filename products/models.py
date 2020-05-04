from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

import config

class Product(models.Model):
    name = models.CharField(max_length=50, default="",  primary_key=True)
    product_type = models.CharField(max_length=50, default=None, null=True)
    url_image = models.URLField(max_length=500, blank=True, default=None, null=True)

    def __str__(self):
        return self.name if self.name else "None"


    def update(self, **kwargs):
        for field in kwargs:
            if field in self.__dict__:
                setattr(self, field, kwargs[field])
        self.save()

    

#     stores = ArrayField(
#         models.CharField(max_lenght=10, choices=config.STORES),
#         size=100
#     )
