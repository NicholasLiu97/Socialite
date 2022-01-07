from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
# displays info about current signed in user


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))
    # ------------------------------- how to redirect to homepage ---------------------------------
    # return render(request, "users/user.html")
    return redirect('homepage:index')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:  # authentication successful
            login(request, user)
            # ------------------------------- how to redirect to homepage ---------------------------------
            # return HttpResponseRedirect(reverse("users:index"))
            return redirect('homepage:index')

        else:
            return render(request, "users/login.html", context={
                "message": "invalid credentials"
            })
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged Out"
    })
