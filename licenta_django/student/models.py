from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    LEVEL_CHOICES = [
        ('LowLevel', 'LowLevel'),
        ('MediumLevel', 'MediumLevel'),
        ('AdvancedLevel', 'AdvancedLevel'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_of_birth = models.DateField()
    interests = models.ManyToManyField('Interest')
    goals = models.ManyToManyField('Goal')
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, default='low')
    vark_model = models.CharField(max_length=30, default="")



class Interest(models.Model):
    name = models.CharField(max_length=50)


class Goal(models.Model):
    name = models.CharField(max_length=50)

class Question(models.Model):
    question= models.CharField(max_length=300)
    choices = models.ManyToManyField('Choice')
    is_vark = models.BooleanField(default=True)

class Choice(models.Model):
    choice = models.CharField(max_length=300)