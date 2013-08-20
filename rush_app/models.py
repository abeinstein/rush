from annoying.fields import AutoOneToOneField
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm



class Rush(models.Model):
	'''A boy living out his last days as a GDI'''
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	phone_number = models.CharField(max_length=15, blank=True)
	email = models.EmailField(blank=True)
	bid = models.BooleanField(default=False)
	picture = models.URLField(blank=True) # URL to picture image
	last_commented = models.DateTimeField(blank=True, null=True)
	notes = models.TextField(blank=True)
	frat = models.ForeignKey('Frat')
	dorm = models.CharField(max_length=50, blank=True)
	hometown = models.CharField(max_length=100, blank=True)


	def __unicode__(self):
		return self.first_name + " " + self.last_name

	def save(self, *args, **kwargs):
		#self.reputation.save()
		super(Rush, self).save(*args, **kwargs)


class Frat(models.Model):
	'''Letters today, leaders tomorrow'''
	name = models.CharField(max_length=100)
	chapter = models.CharField(max_length=100)
	university = models.CharField(max_length=100, blank=True) # Maybe use 'choices' later?
	password = models.CharField(max_length=100)

	class Meta:
		unique_together = ("name", "chapter")


	def save(self, *args, **kwargs):
		''' Custom save method to hash frat passwords '''
		# First time save is called
		if not self.pk:
			self.password = make_password(self.password)
		super(Frat, self).save(*args, **kwargs)


	def __unicode__(self):
		return self.name + " at " + self.university


class UserProfile(models.Model):
	'''A Frat Star (Or sorority star)'''
	user = AutoOneToOneField(User, primary_key=True)
	frat = models.ForeignKey(Frat)
	is_admin = models.BooleanField(default=False)
	facebook_id = models.CharField(unique=True, max_length=50, null=True)

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

class Comment(models.Model):
	body = models.TextField()
	rush = models.ForeignKey(Rush)
	userprofile = models.ForeignKey(UserProfile)
	created = models.DateTimeField(auto_now_add=True)

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body']




