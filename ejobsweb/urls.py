from django.contrib import admin
from django.urls import path
from ejobsweb import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<int:id>', views.blog, name='blog'),

    path('signup', views.signup, name='signup'),
    path('profile_setup', views.profilesetup, name='profilesetup'),

    path('search', views.search, name='search'),
    path('search_people/<str:title>', views.search_people, name='search_people'),

    path('home', views.home, name='home'),

    path('network', views.network, name='network'),
    path('connect', views.connect, name='connect'),
    path('accept_request', views.accept_request, name='accept_request'),


    path('jobs', views.jobs, name='jobs'),
    path('search_jobs', views.search_jobs, name='search_jobs'),
    path('job_tags/<str:title>', views.job_tags, name='job_tags'),

    path('job_profile/<int:id>', views.job_profile, name='job_profile'),
    path('createjob', views.createjob, name='createjob'),

    path('message', views.message, name='message'),
    path('notifications', views.notifications, name='notifications'),

    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_about', views.edit_about, name='edit_about'),
    path('add_experience', views.add_experience, name='add_experience'),
    path('edit_experience/<int:id>', views.edit_experience, name='edit_experience'),
    path('add_education', views.add_education, name='add_education'),
    path('edit_education/<int:id>', views.edit_education, name='edit_education'),

    path('profile', views.profile, name='profile'),

    path('aboutus', views.aboutus, name='aboutus'),
    path('logout', views.log_out, name='log_out'),
    path('messages', views.messages, name='messages'),
    path('messages/<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]