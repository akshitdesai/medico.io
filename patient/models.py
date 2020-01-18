from django.db import models

# Create your models here.
class doctor(models.Model):
    fname = models.CharField(max_length=30,default='u')
    lname = models.CharField(max_length=30,default='u')
    degree = models.CharField(max_length=30,default='u')
    exper = models.IntegerField(default=10)
    hospname = models.CharField(max_length=30,default='u')
    no = models.CharField(max_length=10,default='u')
    email = models.EmailField()
    pass1 = models.CharField(max_length=30)
    
     
class patient(models.Model):
    fname = models.CharField(max_length=30,default='u')
    lname = models.CharField(max_length=30,default='u')
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')
    # image = models.ImageField(upload_to='uploads/')
    height = models.IntegerField(default=10)
    weight = models.IntegerField(default=10)
    bgroup = models.CharField(max_length=5)
    Email = models.EmailField()
    qid = models.IntegerField()
    allergy = models.TextField()
    address = models.TextField(default='u')
    no = models.CharField(max_length=10,default='u')