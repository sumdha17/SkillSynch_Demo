from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import CommonFields, Choice
from user.manager import UserManager
from django.core.validators import MinLengthValidator

# Create your models here.


class CustomUser(AbstractUser, CommonFields):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=10, unique=True,validators=[MinLengthValidator(10)], blank=True, null=True)
    gender = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='user_gender', limit_choices_to={'choice_type': 'gender'}, null=True, blank= True)
    type = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='users_type', limit_choices_to={'choice_type': 'user'},null=True, blank=True)
    status = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='user_status', limit_choices_to={'choice_type': 'status'}, null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    designation = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='assignee_designation',limit_choices_to={'choice_type': 'designation'}, blank=True, null=True )  

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'customusers'
    