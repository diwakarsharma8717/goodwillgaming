from django.dispatch import receiver
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404

# To create User
from django.contrib.auth.models import User

# For authenticate user and let him login and logout
from django.contrib.auth import authenticate, login, logout
# To check whether or not person is loggedin
from django.contrib.auth.decorators import login_required
# For Mesaages
from django.http import JsonResponse
import json

# For File Upload
from django.core.files.storage import FileSystemStorage

# Create your views here.


def index(request):

    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        # Check for error
        if user is None:
            return redirect('index')

        if user is not None:
            global username
            username = loginusername
            login(request, user)
            return redirect('home')

    else:
        blogs = Blog.objects.all()
        return render(request, 'goodwill/index.html', {'blogs': blogs})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for error
        if {'username': username} in User.objects.values('username'):

            return redirect('index')

        if pass1 != pass2:

            return redirect('index')

        if len(pass1) < 8:

            return redirect('index')

        # Creating User
        myuser = User.objects.create_user(username, email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        user = authenticate(username=username, password=pass1)
        login(request, user)
        friend_list = FriendList.objects.create(user=user)
        friend_list.save()

        return redirect('profilesetup')

    else:
        return render(request, 'goodwill/sign-up.html')


def profilesetup(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        headline = request.POST['headline']
        about = request.POST['about']

        profile = Profile.objects.create(
            user=request.user, pfp=filename, about=about, headline=headline)
        profile.save()

        return redirect('home')

    else:
        pass

    return render(request, "goodwill/set-profile.html")


def blog(request, id):
    blog = Blog.objects.get(id=id)
    blogs = Blog.objects.all()
    return render(request, "goodwill/blog-single.html", {'blog': blog, 'blogs': blogs})


@login_required(login_url='index')
def home(request):
    profile = Profile.objects.get(user=request.user)

    posts = Post.objects.filter(profile=profile)
    friendlist = FriendList.objects.get(user=request.user)
    print(friendlist.friends)

    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            caption = request.POST['caption']

            post = Post.objects.create(
                profile=profile, img=filename, caption=caption)
            post.save()

        except:
            caption = request.POST['caption']

            post = Post.objects.create(profile=profile, caption=caption)
            post.save()

    else:
        pass

    return render(request, "goodwill/home.html", {'posts': posts, 'profile': profile})


def search(request):
    if request.method == 'GET':
        search = request.GET['search']

    users1 = User.objects.filter(first_name__icontains=search)
    users2 = User.objects.filter(last_name__icontains=search)

    users = users1 | users2
    print("users:", users)
    profiles = Profile.objects.none()
    for user in users:
        profiles1 = Profile.objects.filter(user=user)
        profiles = profiles | profiles1

    print(profiles)

    jobs1 = Job.objects.filter(profession__icontains=search)
    jobs2 = Job.objects.filter(company_name__icontains=search)

    jobs = jobs1 | jobs2

    return render(request, 'goodwill/search.html', {'profiles': profiles, 'jobs': jobs})

def search_people(request, title):
    user = User.objects.get(username=title)
    search_profile = Profile.objects.get(user=user)
    experiences = Experience.objects.filter(user=user)
    educations = Education.objects.filter(user=user)
    posts = Post.objects.filter(profile=search_profile)
    print(profile)
    print(posts)
    return render(request, 'goodwill/search_people.html', {'experiences': experiences, 'educations': educations, 'search_profile': search_profile, 'posts':posts})

def log_out(request):
    logout(request)

    return redirect('index')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    user = User.objects.get(username=username)
    reciever = request.session['reciever']
    recieveing_user = User.objects.get(username=reciever)

    room_details = Room.objects.get(sender=user, reciever=recieveing_user)
    new_message = Message.objects.create(
        value=message, user=username, room=room_details)
    new_message.save()

    room_details2 = Room.objects.get(sender=recieveing_user, reciever=user)
    new_message2 = Message.objects.create(
        value=message, user=reciever, room=room_details2)
    new_message2.save()

    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    user = User.objects.get(username=request.user.username)
    reciever = request.session['reciever']
    recieveing_user = User.objects.get(username=reciever)

    room_details = Room.objects.get(sender=user, reciever=recieveing_user)

    messages = Message.objects.filter(room=room_details)
    return JsonResponse({"messages": list(messages.values())})


def accept_request(request):
    sender = request.POST['sender']
    sender_user = User.objects.get(username=sender)
    receiver = request.POST['receiver']
    receiver_user = User.objects.get(username=receiver)

    friend_request = FriendRequest.objects.get(
        sender=sender_user, receiver=receiver_user)
    friend_request.accept()
    friend_request.save()

    return HttpResponse('Request accepted successfully')


def connect(request):
    sender = request.POST['sender']
    sender_user = User.objects.get(username=sender)
    receiver = request.POST['receiver']
    receiver_user = User.objects.get(username=receiver)

    friend_request = FriendRequest.objects.create(
        sender=sender_user, receiver=receiver_user)
    friend_request.accept()
    friend_request.save()

    return HttpResponse('Request sent successfully')


@login_required(login_url='index')
def network(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    requests = FriendRequest.objects.filter(receiver=user)

    userlist = User.objects.all()
    return render(request, 'goodwill/network.html', {'userlist': userlist, 'profile': profile, 'requests': requests})


@login_required(login_url='index')
def jobs(request):
    professions = Profession.objects.all()
    jobs = Job.objects.all()
    return render(request, 'goodwill/jobs.html', {'professions': professions, 'jobs': jobs})


def search_jobs(request):
    if request.method == 'GET':
        search_jobs = request.GET['search_jobs']

    jobs1 = Job.objects.filter(profession__icontains=search_jobs)
    jobs2 = Job.objects.filter(company_name__icontains=search_jobs)

    jobs = jobs1 | jobs2

    return render(request, 'goodwill/search_jobs.html', {'jobs': jobs})


def job_tags(request, title):
    search_profession = title
    professions = Profession.objects.all()

    jobs1 = Job.objects.filter(profession__icontains=search_profession)
    jobs2 = Job.objects.filter(company_name__icontains=search_profession)

    jobs = jobs1 | jobs2

    return render(request, 'goodwill/job_tags.html', {'search_profession': search_profession, 'professions': professions, 'jobs': jobs})


def job_profile(request, id):
    job = Job.objects.get(id=id)
    jobs = Job.objects.all()
    return render(request, "goodwill/job_profile.html", {'job': job, 'jobs': jobs})


def createjob(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        profession = request.POST['profession']
        company_name = request.POST['company_name']
        location = request.POST['location']
        link = request.POST['link']
        about = request.POST['about']

        job = Job.objects.create(profession=profession, company_name=company_name,
                                 img=filename, location=location, url=link, about=about)
        job.save()

        return redirect('jobs')

    else:
        pass

    return render(request, "goodwill/job.html")


@login_required(login_url='index')
def message(request):
    return render(request, 'goodwill/messages.html')


@login_required(login_url='index')
def notifications(request):
    return render(request, 'goodwill/notifications.html')


@login_required(login_url='index')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    educations = Education.objects.filter(user=request.user)
    posts = Post.objects.filter(profile=profile)
    return render(request, 'goodwill/profile.html', {'experiences': experiences, 'educations': educations, 'profile': profile, 'posts':posts})


def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            headline = request.POST['headline']
            instagram = request.POST['instagram']
            youtube = request.POST['youtube']
            linkedin = request.POST['linkedin']
            facebook = request.POST['facebook']

            profile_update = Profile.objects.update(user=request.user, pfp=filename, headline=headline,
                                                    instagram=instagram, youtube=youtube, linkedin=linkedin, facebook=facebook)

            return redirect('profile')

        except:
            headline = request.POST['headline']
            instagram = request.POST['instagram']
            youtube = request.POST['youtube']
            linkedin = request.POST['linkedin']
            facebook = request.POST['facebook']

            profile_update = Profile.objects.update(user=request.user, headline=headline,
                                                    instagram=instagram, youtube=youtube, linkedin=linkedin, facebook=facebook)

            return redirect('profile')

    else:
        pass

    return render(request, "goodwill/edit_profile.html", {'profile': profile})


def edit_about(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        about = request.POST['about']

        profile_update = Profile.objects.update(user=request.user, about=about)

        return redirect('profile')

    else:
        pass

    return render(request, "goodwill/edit_about.html", {'profile': profile})


def add_experience(request):
    professions = Profession.objects.all()
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            designation = request.POST['designation']
            company = request.POST['company']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            experience_create = Experience.objects.create(user=request.user, img=filename, designation=designation,
                                                          company=company, joining_date=joining_date, resigning_date=resigning_date, about=about)
            experience_create.save()
            return redirect('profile')

        except:
            designation = request.POST['designation']
            company = request.POST['company']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            experience_create = Experience.objects.create(user=request.user, designation=designation,
                                                          company=company, joining_date=joining_date, resigning_date=resigning_date, about=about)
            experience_create.save()
            return redirect('profile')

    else:
        pass

    return render(request, "goodwill/add_experience.html", {'professions': professions})


def edit_experience(request, id):
    experience = Experience.objects.get(id=id)
    professions = Profession.objects.all()
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            designation = request.POST['designation']
            company = request.POST['company']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            experience_update = Experience.objects.update(user=request.user, img=filename, designation=designation,
                                                          company=company, joining_date=joining_date, resigning_date=resigning_date, about=about)

            return redirect('profile')

        except:
            designation = request.POST['designation']
            company = request.POST['company']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            experience_update = Experience.objects.update(user=request.user, designation=designation,
                                                          company=company, joining_date=joining_date, resigning_date=resigning_date, about=about)

            return redirect('profile')

    else:
        pass

    return render(request, "goodwill/edit_experience.html", {'experience': experience, 'professions': professions})


def add_education(request):
    professions = Profession.objects.all()
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            university = request.POST['university']
            degree = request.POST['degree']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            education_create = Education.objects.create(user=request.user, img=filename, university=university,
                                                        degree=degree, joining_date=joining_date, resigning_date=resigning_date, about=about)
            education_create.save()
            return redirect('profile')

        except:
            university = request.POST['university']
            degree = request.POST['degree']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            education_create = Education.objects.create(user=request.user, university=university,
                                                        degree=degree, joining_date=joining_date, resigning_date=resigning_date, about=about)
            education_create.save()
            return redirect('profile')

    else:
        pass

    return render(request, "goodwill/add_education.html", {'professions': professions})


def edit_education(request, id):
    education = Education.objects.get(id=id)
    professions = Profession.objects.all()
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            university = request.POST['university']
            degree = request.POST['degree']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            education_update = Education.objects.update(user=request.user, img=filename, university=university,
                                                        degree=degree, joining_date=joining_date, resigning_date=resigning_date, about=about)

            return redirect('profile')

        except:
            university = request.POST['university']
            degree = request.POST['degree']
            joining_date = request.POST['joining_date']
            resigning_date = request.POST['resigning_date']
            about = request.POST['about']

            education_update = Education.objects.update(user=request.user, university=university,
                                                        degree=degree, joining_date=joining_date, resigning_date=resigning_date, about=about)

            return redirect('profile')

    else:
        pass

    return render(request, "goodwill/edit_education.html", {'education': education, 'professions': professions})


def aboutus(request):
    return render(request, 'aboutus.html')


def messages(request):
    return render(request, 'messages.html')


def room(request, room):
    reciever = request.GET.get('reciever')
    sending_user = User.objects.get(username=request.user.username)
    recieveing_user = User.objects.get(username=reciever)

    room_details = Room.objects.get(
        sender=sending_user, reciever=recieveing_user)

    return render(request, 'messageroom.html', {
        'username': request.user.username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    reciever = request.POST['reciever']
    room = request.user.username + " to "+reciever
    sending_user = User.objects.get(username=request.user.username)
    recieveing_user = User.objects.get(username=reciever)
    request.session['reciever'] = reciever

    if Room.objects.filter(sender=sending_user, reciever=recieveing_user).exists():
        return redirect('/messages/'+room+'/?reciever='+reciever)
    else:
        new_room1 = Room.objects.create(
            sender=sending_user, reciever=recieveing_user)
        new_room1.save()
        new_room2 = Room.objects.create(
            sender=recieveing_user, reciever=sending_user)
        new_room2.save()

        return redirect('/messages/'+room+'/?reciever='+reciever)
