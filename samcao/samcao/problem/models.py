from django.db import models

# Create your models here.
class System(models.Model):
    system_name = models.CharField(max_length=30)

class User(models.Model):
    user_name = models.CharField(max_length=30)
    pass_word = models.CharField(max_length=30)

class Type(models.Model):
    way_type = models.CharField(max_length=50)
    system_name = models.ForeignKey(System)

class Way(models.Model):
    Key_world= models.CharField(max_length=200)
    user_name = models.ForeignKey(User)
    system_name=models.ForeignKey(System)
    way_type = models.ForeignKey(Type)
    way = models.CharField(max_length=200)
    ban_fa = models.TextField()
