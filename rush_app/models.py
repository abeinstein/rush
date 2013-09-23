import urllib

from annoying.fields import AutoOneToOneField
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.core.files import File
from django.forms import ModelForm

from django_boto.s3.storage import S3Storage
# from django_facebook.models import FacebookProfileModel

s3 = S3Storage()


# TODO: Make this more robust. If user first takes an iPhone pic but then 
# uploads a web pic, picture_url should be updated accordingly.
class Rush(models.Model):
	'''A boy living out his last days as a GDI'''
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	phone_number = models.CharField(max_length=15, blank=True)
	email = models.EmailField(blank=True)
	bid = models.BooleanField(default=False)
	last_commented = models.DateTimeField(blank=True, null=True)
	notes = models.TextField(blank=True)
	frat = models.ForeignKey('Frat')
	dorm = models.CharField(max_length=50, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	picture = models.ImageField(storage=s3, upload_to="img/", blank=True) 


	def __unicode__(self):
		return self.first_name + " " + self.last_name



	def save(self, *args, **kwargs):
		# if self.picture and not self.picture_url:
		# 	self.picture_url = self.picture.url
		super(Rush, self).save(*args, **kwargs)

	@property
	def picture_url(self):
		if self.picture and hasattr(self.picture, 'url'):
			return self.picture.url
		elif self.picture:
			return self.picture
		else:
			return '#'

	def upload_picture_from_url(self, url):
		''' Takes a url to image, and stores it in the ImageField
		To be used when Adam sends me S3 urls generated from iPhone
		 '''
		result = urllib.urlretrieve(url)
		self.picture.save(url, File(open(result[0])))
		self.save()

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

	# blank because we may not yet know frat when created
	frat = models.ForeignKey(Frat, blank=True, null=True)  
	is_admin = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username

# from django.db.models.signals import post_save

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User)


class Reputation(models.Model):
	'''Encapsulates thumbs up/ thumbs down for each rush'''
	rush = AutoOneToOneField(Rush, primary_key=True)
	thumbsup_users = models.ManyToManyField(UserProfile, related_name='tu+', blank=True, null=True)
	thumbsdown_users = models.ManyToManyField(UserProfile, related_name='td+', blank=True, null=True)
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




