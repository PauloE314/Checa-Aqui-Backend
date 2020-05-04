from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
import config

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", blank=True)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    points = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.user}'s Profile"

    @property
    def score(self):
        return (self.attendant_score + self.client_score)/2



    #CLIENT SCORE ------------
    @property
    def client_score(self):
        score_sum = 3
        score_len = 1

        for client_attendance in self.user.client_attendances.all():
            if client_attendance.client_was_evaluated or client_attendance.max_time_to_attendant_evaluate > timezone.now():
                score_sum += client_attendance.client_score
                score_len += 1
        
        return (score_sum / score_len)


    #ATTENDANT SCORE --------------------
    @property
    def attendant_score(self):
        score_sum = 3
        score_len = 1
        
        for attendant_attendance in self.user.attendant_attendances.all():
            if attendant_attendance.attendant_was_evaluated or not attendant_attendance.client_can_evaluate:
                score_sum += attendant_attendance.attendant_score
                score_len += 1
        
        return (score_sum / score_len)
                
    @property
    def is_premium(self):
        qt_votes = len(list(map(
            lambda atend: atend.attendant_was_evaluated
        , self.user.attendant_attendances.all())))

        if qt_votes >= config.MIN_VOTES_AMOUNT_TO_PREMIUM and self.score >= config.MIN_SCORE_TO_PREMIUM:
            return True
        else:
            return False


    def set_points(self, category):
        points = config.POINTS[category]
        self.points += points

        if self.points < 0:
            self.points = 0
            
        self.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
