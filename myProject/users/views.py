from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

# Register View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after successful registration
            return redirect("/")  # Redirect to home/dashboard
        else:
            # Get the first error only
            field, errors = next(iter(form.errors.items()))  # Get first field with errors

            messages.error(request, f"{errors[0]}")  # Show first error

    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})

# Login View
def login_view(request):
    e = False
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            e = False
            user = form.get_user()
            login(request, user)
            return redirect("/")
        else:
            e = True
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form , 'e' : e})


# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")
