from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
import os
from uuid import uuid4
import string
import random


# generate unique code for the room
def generate_unique_code():
    length = 8
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code = code).count() == 0:
            break
    return code

def unique_filename(instance, filename):
    """
    Generates a unique filename for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('profile_images', filename)

#User Model
class CustomUser(models.Model):
    first_name = models.CharField(validators=[
            MinLengthValidator(3, 'First Name must contain at least 3 characters'),
            MaxLengthValidator(50,'Fisrt Name must contain atmost 50 characters'),
            ], max_length = 50,null=False, blank=False)
    last_name = models.CharField(validators=[
            MinLengthValidator(3, 'Last Name must contain at least 3 characters'),
            MaxLengthValidator(50,'Last Name must contain atmost 50 characters')
            ],max_length = 50, null=False, blank=False)
    username = models.CharField(validators=[
            MinLengthValidator(3, 'User Name must contain at least 3 characters'),
            MaxLengthValidator(50,'User Name must contain atmost 50 characters')
            ],max_length = 50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    password = models.CharField(validators=[
            MinLengthValidator(8, 'Password must contain at least 8 characters'),
            MaxLengthValidator(50,'Password must contain atmost 50 characters')
            ],max_length = 50, null=False, blank=False)
    profile_picture = models.ImageField(upload_to=unique_filename, blank=False, null=False)

    


#Room modal
class Room(models.Model):
    code = models.CharField(max_length = 8, default = generate_unique_code, unique = True)
    host = models.CharField(max_length = 50, unique = True)
    guest_can_pause = models.BooleanField(null = False, default = False)
    votes_to_skip = models.IntegerField(null = False, default = 1)
    created_at = models.DateTimeField(auto_now_add = True)
