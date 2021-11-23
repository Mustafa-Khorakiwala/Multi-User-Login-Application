from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    rollno = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return str(self.rollno)
    
class Teacher(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    staffcode = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.staffcode

class Person(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.name

