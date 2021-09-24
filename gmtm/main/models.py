from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from gm2m import GM2MField


class Video(models.Model):
    title = models.CharField(max_length=255)


class Movie(Video):
    pass


class Documentary(Video):
    pass


class Opera(Video):
    pass


class User(models.Model):
    name = models.CharField(max_length=255)
    preferred_videos = GM2MField()


class User2(models.Model):
    name = models.CharField(max_length=255)
    preferred_videos = GM2MField(through='pv')


class pv(models.Model):
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    video = GenericForeignKey(ct_field='video_ct', fk_field='video_fk')
    video_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    video_fk = models.CharField(max_length=255)


'''
from main.models import *
'''
