from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.db import connection
from django.conf import settings
from django.contrib.auth import authenticate, login


User = get_user_model()


# Registration view
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create the new user
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()

            # Automatically log the user in after registration
            login(request, user)
            return redirect("product_list")  # Redirect to the product list page

    return render(request, "core/register.html")


# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Use Django's authenticate method
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is found, log them in
            login(request, user)
            return redirect("product_list")  # Redirect to the product list page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "core/login.html")


# Logout view
def logout_view(request):
    logout(request)
    return redirect("product_list")
