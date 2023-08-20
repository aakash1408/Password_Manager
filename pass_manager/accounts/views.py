from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from .models import PasswordEntry


# Create your views here.
def signin(request):

    signed = False
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                email_exists = "This email already exists"
                context = {"email_exists": email_exists}
                return render(request, "signin.html", context)
                
            elif User.objects.filter(username=username).exists():
                username_taken = "This username is already taken"
                context = {"username_taken": username_taken}
                return render(request, "signin.html",context )
            
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password = password1)
                user.save()
                user = authenticate(request, username = username, password = password1)
        
                if user is not None:
                    login(request, user)
                    current_user = request.user
                    login_state = True
                    return render(request, "index.html", {"user":current_user, "login_state": True})
                
                
        else:
            error_message = "Passwords do not match"
            context = {"error_message": error_message}
            return render(request, "signin.html", context)
    else:
        return render(request, 'signin.html')
    


def info(request):
    if request.method == "POST":
        website_name = request.POST["website"]
        password = request.POST["password"]
        text = request.POST["notes"]
        user = request.user

        # password_hash = make_password(password)
        passowordentry = PasswordEntry.objects.create(user = user, website = website_name, password_hash = password, notes = text)
        # passs = PasswordEntry.objects.all()
        return redirect("info")
        
        #return render(request, "display.html") 
    else:
    
        user = request.user
        print(user)
        user_passwords = PasswordEntry.objects.filter(user = user)
        context = {'user_passwords': user_passwords}
        return render(request, "display.html", context)

def login_views(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            current_user = request.user
            login_state = True
            return render(request, "index.html", {"user":current_user, "login_state": True})
        else:
            error_message = 'Invalid username or password'
            context = {'error_message': error_message}
            return render(request, 'login.html', context)


    else:
        return render(request, "login.html")
    

