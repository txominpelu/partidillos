from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.forms import ModelForm

class UserProfile(models.Model):
    # This field is required. 
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField() 
    place = models.CharField(max_length=30)
    players = models.ManyToManyField(UserProfile)
    creator = models.ForeignKey(UserProfile, related_name='creator')

class MatchForm(ModelForm):

    class Meta:
        model = Match
        fields = ('date', 'place', 'creator')
