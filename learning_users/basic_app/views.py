from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm, UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required #if ever you have a view that's required, you can decorate it with this built-in library


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")


@login_required  #one cannot logout unless he first logged in.
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index')) #when log out, redirect to the homepage
    # reverse returns the url string by taking the name of a view: path('', views.index, name='index'), name is "index"
    # HttpResponseRedirect takes in a path, a url, or a relative path, and returns the view's result


def register(request):
    registered = False

    if request.method == 'POST':
        profile_form = UserProfileInfoForm(request.POST)
        user_form = UserForm(request.POST)

        #check if both forms are valid:
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #save it to the database instead of commit: user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic'] #a dictionary

            # profile.portfolio_site

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        #else, no post request submitted, then we just display the forms:
        #since its just displaying, we don't need to check if registered
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request, 'basic_app/registration.html', context={'user_form':user_form, 'profile_form':profile_form, 'registered':registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #remember in login.html, we have: <input class="form-control" type="text" name="username" placeholder="Enter username">
        password = request.POST.get('password')

        user = authenticate(username = username, password = password) #pass username and password to the authenticate Function
        #sometimes, it is OK to just pass in: user = authenticate(username, password); this returns an object if authenticated


        if user: #if user is authentiated (i.e. the object returned is not NULL)
            if user.is_active: #sometimes, when user activity is inactive, they need to re-login
                login(request, user) #we have imported this function from: django.contrib.auth --> login, logout
                return HttpResponseRedirect(reverse('index')) #reverse or redirect user back to homepage
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else: #someone tried to login but the system either does not have this username, or does not have this password
            print("Someone tried to login and failed...")
            print("Username: {} and password {}".format(username, password)) #this will print to the console, not the web page
            return HttpResponse("invalid login details replied!")
    else:
        return render(request, 'basic_app/login.html', {}) #if no login submit, just display login page
