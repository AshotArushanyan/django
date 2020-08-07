from django.shortcuts import render
from first_app import forms
from django.http import HttpResponse, HttpResponseRedirect
from first_app.models import Topic, Webpage, AccessRecord
from first_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    return render(request,"first_app/index.html")


@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm

    return render(request, 'first_app/registration.html', {"user_form": user_form, 'profile_form': profile_form, 'registered': registered})



def form_name_view(request):
    form = forms.FormName()

    if request.method == "POST":
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("validdatin success")
            print("Name: "+form.cleaned_data["name"])
            print("Email: "+form.cleaned_data["email"])
            print("Text: "+form.cleaned_data["text"])

    return render(request,"first_app/form_page.html", {"form": form})


def user(request):
    webpage_list = AccessRecord.objects.order_by("date")
    date_dict = {"access_records": webpage_list}
    return render(request,'first_app/users.html',context=date_dict)

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("someone tried to login and failed")
            print(f"Username: {username} and password {password}")
            return HttpResponse("INVALID LOGIN DETAILS SUPPLIED!")
    else:
        return render(request, 'first_app/login.html', {})
