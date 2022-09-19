from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Profession)
admin.site.register(Experience)
admin.site.register(Education)


#For Post
admin.site.register(Post)

#For messaging
admin.site.register(Message)
admin.site.register(Room)

#For Friend List
admin.site.register(FriendList)

#For Friend Request
admin.site.register(FriendRequest)

admin.site.register(Blog)

admin.site.register(Job)
