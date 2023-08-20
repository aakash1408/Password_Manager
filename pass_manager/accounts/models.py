from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=100, default='default_hash_value')
    notes = models.TextField(blank=True)

    


