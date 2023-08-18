from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth

# Create your views here.
def signin(request):

    error_message = ""
    email_exists = ""
    name = ""
    signed = False
    if request.method == "POST":
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
                
            else:
                user = User.objects.create_user(email=email, password = password1, first_name=first_name, last_name=last_name)
                user.save()
                context = {"name": "Hi " + first_name + " " + last_name, "signed" : True}
                return render(request, "index.html", context)
                
        else:
            error_message = "Passwords do not match"
            context = {"error_message": error_message}
            return render(request, "signin.html", context)
    else:
        return render(request, 'signin.html')
    


def info(request):
    return render(request, "display.html")

def login(request):
    pass