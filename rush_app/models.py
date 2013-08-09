from annoying.fields import AutoOneToOneField
from django.db import models
from django.contrib.auth.models import User

class Rush(models.Model):
	'''A boy living out his last days as a GDI'''
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	phone_number = models.CharField(max_length=15, blank=True)
	email = models.EmailField(blank=True)
	bid = models.BooleanField(default=False)
	picture = models.URLField(blank=True) # URL to picture image
	last_commented = models.DateTimeField(blank=True, null=False)
	notes = models.TextField(blank=True)
	frat = models.ForeignKey('Frat')
	dorm = models.CharField(max_length=50, blank=True)
	hometown = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.first_name + " " + self.last_name

	def save(self, *args, **kwargs):
		self.reputation.save()
		super(Reputation, self).save(*args, **kwargs)


class Frat(models.Model):
	'''Letters today, leaders tomorrow'''
	name = models.CharField(max_length=100)
	chapter = models.CharField(max_length=100)
	university = models.CharField(max_length=100) # Maybe use 'choices' later?

	def __unicode__(self):
		return self.name + " at " + self.university


class UserProfile(models.Model):
	'''A Frat Star (Or sorority star)'''
	user = AutoOneToOneField(User, primary_key=True)
	frat = models.ForeignKey(Frat)

	def __unicode__(self):
		return self.user.username

class Reputation(models.Model):
	'''Encapsulates thumbs up/ thumbs down for each rush'''
	rush = AutoOneToOneField(Rush, primary_key=True)
	thumbsup_users = models.ManyToManyField(UserProfile, related_name='tu+')
	thumbsdown_users = models.ManyToManyField(UserProfile, related_name='td+')
	thumbsup = models.IntegerField(default=0)
	thumbsdown = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.thumbsup = self.thumbsup_users.count()
		self.thumbsdown = self.thumbsdown_users.count()
		super(Reputation, self).save(*args, **kwargs)




