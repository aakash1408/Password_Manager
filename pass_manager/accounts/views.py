from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from .models import PasswordEntry
from django.contrib import messages



# Create your views here.

def authenticate_user(username, password):
    try:
        user = User.objects.get(username=username)
        # In a real application, you should hash the stored password and compare hashes
        if user.password == password:
            return True
    except User.DoesNotExist:
        pass
    return False



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
        website_name = request.POST["websitee"]
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

def view(request):
    if request.method == "POST":
        provided_username = request.POST['username']
        provided_password = request.POST['password']
        
        # try:
        #     entry = User.objects.get(username=provided_username)
        # except User.DoesNotExist:
        #     context = {'error_message': 'User not found'}
        #     return render(request, 'display.html', context)
        
        # if entry.password == provided_password:
        user = authenticate(username=provided_username, password=provided_password)
        if user is not None:
            user = request.user   # Set the authenticated user
            user_passwords = PasswordEntry.objects.filter(user=user)
            context = {'user_passwords': user_passwords, "view_yes": True}
            return render(request, 'display.html', context)
        else:
            user = request.user
            user_passwords = PasswordEntry.objects.filter(user=user)
            context = {'error_message': 'Incorrect password', 'user_passwords': user_passwords, "view_yes": False}
            return render(request, 'display.html', context)
    
    else:
        user = request.user
        user_passwords = PasswordEntry.objects.filter(user=user)
        context = {'user_passwords': user_passwords, "view_yes": False}  # Set view_yes to False
        return render(request, 'display.html', context)

def update(request):
    if request.method == "POST":
        username = request.POST["username"]
        master_password = request.POST["master_password"]
        new_password = request.POST["password"]
        entry_id = request.POST.get('entry_id')
        
        user = authenticate(username=username, password=master_password)
        if user is not None:
            password_entry = PasswordEntry.objects.get(id=entry_id)
            password_entry.password_hash = new_password
            password_entry.save()
            messages.success(request, 'Your password has been updated successfully!')
            return redirect("view")
        else:
            user = request.user
            user_passwords = PasswordEntry.objects.filter(user=user)
            context = {'error_message': 'Incorrect password', 'user_passwords': user_passwords}
            return render(request, 'display.html', context)
    else:
        return render(request, "display.html")
    
def delete(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        entry_id = request.POST["idd"]
        
        user = authenticate(username=username, password=password)
        if user is not None:
            password_entry = PasswordEntry.objects.get(id=entry_id)
            password_entry.delete()
            messages.success(request, 'Your password has been deleted successfully!')
            return redirect("view")
        else:
            user = request.user
            user_passwords = PasswordEntry.objects.filter(user=user)
            context = {'error_message': 'Incorrect password', 'user_passwords': user_passwords}
            return render(request, 'display.html', context)

    else:
        return render(request, "display.html")





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
    





# def update(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = request.user
#         entry = PasswordEntry.objects.get(user) 
#         entry.password_hash = password
        
#     else:
         
#         return render(request, "display.html")

    


# def delete(request):
#     if request.method == "POST":
#         pass

    
        
    

