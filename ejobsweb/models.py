from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#Added for Friendlist model
from django.conf import settings
	
#Posts by User Model    

class Profile(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	pfp = models.ImageField(upload_to="pfp")
	headline = models.CharField(default=None, blank=True, null=True, max_length=100)
	location = models.CharField(default=None, blank=True, null=True, max_length=50)
	about = models.TextField(default=None)
	instagram = models.URLField(default=None, blank=True, null=True)
	youtube = models.URLField(default=None, blank=True, null=True)
	linkedin = models.URLField(default=None, blank=True, null=True)
	facebook = models.URLField(default=None, blank=True, null=True)
	def __str__(self):
		return self.user.username

	def name(self):
		return self.user.first_name + " " + self.user.last_name
	
	def username(self):
		return self.user.username
		
class Experience(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	designation = models.CharField(default=None, null=True, max_length=50)
	company = models.CharField(max_length=50, blank=True, null=True)
	img = models.ImageField(default=None, null=True, upload_to="experience_img")
	joining_date = models.CharField(max_length=50)
	resigning_date = models.CharField(max_length=50)
	about = models.TextField()
	def __str__(self):
		return self.user.username + " as " + self.designation

class Education(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	university = models.CharField(default=None, null=True, max_length=50)
	degree = models.CharField(max_length=50, blank=True, null=True)
	img = models.ImageField(default=None, null=True, upload_to="education_img")
	joining_date = models.CharField(max_length=50)
	resigning_date = models.CharField(max_length=50)
	about = models.TextField()
	def __str__(self):
		return self.user.username + "'s education of " + self.degree

#Messages by Users
class Room(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_reciever')
    
    def __str__(self):
        return self.sender.username + " to " + self.reciever.username

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.ForeignKey(Room,on_delete=models.CASCADE) 

#Model for Friendlist
class FriendList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends") 

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add a new friend.
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			self.save()

	def remove_friend(self, account):
		"""
		Remove a friend.
		"""
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		remover_friends_list = self # person terminating the friendship

		# Remove friend from remover friend list
		remover_friends_list.remove_friend(removee)

		# Remove friend from removee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(remover_friends_list.user)


	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
	receiver 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

	is_active			= models.BooleanField(blank=False, null=False, default=True)

	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username+" to "+self.receiver.username

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()


class Blog(models.Model):

	name = models.CharField(max_length=50)
	img = models.ImageField(default=None, upload_to="Profession_Images")
	content = models.TextField()

	def __str__(self):
		return self.name

class Profession(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Job(models.Model):

	profession = models.CharField(max_length=50)
	company_name = models.CharField(max_length=50)
	img = models.ImageField(default=None, upload_to="Company Profile Picture")
	location = models.CharField(max_length=50)
	date = models.DateTimeField(default=timezone.now, blank=True)
	url = models.URLField(default=None)
	about = models.TextField()

	def __str__(self):
		return self.profession +" job by "+ self.company_name + " on " + str(self.date)

class Post(models.Model):
	profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
	img = models.ImageField(default=None, upload_to='posts_img')
	caption = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return str(self.profile.user) + " " + str(self.created_on)
	def pfp (self):
		return self.profile.pfp
	def headline(self):
		return self.profile.headline