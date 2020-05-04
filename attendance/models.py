from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone  #datetime.datetime.now()
from django.contrib.auth.models import User
from products.models import Product
import datetime

import config

class Attendance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_attendances')
    attendant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendant_attendances')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    client_score = models.FloatField(default=3, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    attendant_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    attendant_was_evaluated = models.BooleanField(default=False)
    client_was_evaluated = models.BooleanField(default=False)


    @property
    def client_can_evaluate(self):
        now = timezone.now()
        diff = now - self.created_at
        hour_diff = diff.total_seconds()/(60*60)

        if config.MAX_TIME_TO_CLIENT_AVALIATE > hour_diff and hour_diff > config.MIN_TIME_TO_CLIENT_AVALIATE:
            return not self.attendant_was_evaluated
        else:
            return False

    @property
    def attendant_can_evaluate(self):
        now = timezone.now()
        diff = now - self.created_at
        hour_diff = diff.total_seconds()/(60*60)

        if config.MAX_TIME_TO_ATTENDANT_AVALIATE > hour_diff:
            if not self.client_can_evaluate:
                return not self.client_was_evaluated
            else:
                return False
        else:
            return False

    @property
    def min_time_to_client_evaluate(self):
        h_created_at = self.created_at
        min_time = datetime.timedelta(hours=config.MIN_TIME_TO_CLIENT_AVALIATE)
        return h_created_at + min_time

    @property
    def max_time_to_client_evaluate(self):
        h_created_at = self.created_at
        max_time = datetime.timedelta(hours=config.MAX_TIME_TO_CLIENT_AVALIATE)
        return h_created_at + max_time


    @property
    def max_time_to_attendant_evaluate(self):
        h_created_at = self.created_at
        max_time = datetime.timedelta(hours=(config.MAX_TIME_TO_ATTENDANT_AVALIATE))
        return h_created_at + max_time



    def evaluate_attendant(self, score):
        self.attendant_score = score
        self.attendant_was_evaluated = True
        self.save()
        self.attendant.profile.set_points('ATTENDANT')

    def evaluate_client(self, score):
        self.client_score = score
        self.client_was_evaluated = True
        self.save()
        self.client.profile.set_points('CLIENT')
        # self.attendant.profile.set_points('ATTENDANT')
        # self.attendant.profile.check_premium()

    
    def __str__(self):
        return f"cliente {self.client}, atendente {self.attendant}, id {self.id}"

    