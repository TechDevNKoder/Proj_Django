from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Talks
from .forms import TalkForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    if request.user.is_authenticated:
        form = TalkForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                Talk = form.save(commit=False)
                Talk.user = request.user
                Talk.save()
                messages.success(
                    request, ("Your Thoughts have been shared.."))
                return redirect(home)

        talks = Talks.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"talks": talks, "form": form})

    else:
        return render(request, 'login.html')


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile.html', {"profiles": profiles})
    else:
        messages.success(
            request, ("You must be Logged In to access this page.."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        talks = Talks.objects.filter(user_id=pk)

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, "profile_user.html", {"profile": profile, "talks": talks})
    else:
        messages.success(
            request, ("You must be Logged In to access this page.."))
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, ("You Have Been Logged In.."))
            return redirect('home')
        else:
            messages.success(
                request, ("Invalid Username or Password .."))
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'login.html')
