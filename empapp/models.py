from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
# Create your amazing models here.
#create a reciever for the signal 'post_save' for the user model
#once its created create a token for that user
@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance) #create token for the user


#create class dept model class by inheriting in model class
class Department(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    # dept name is char field with max char length of 200
    DepartmentName = models.CharField(max_length=200)    
    #instead of memory address of he object
    # we need to return the name of the dept               
    def __str__(self):
        return self.DepartmentName

class Employee(models.Model):
    EmployeeId =  models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=200)
    Designation = models.CharField(max_length=150)
    DateOfJoining = models.DateField()
    #datefield shows current date
    #deptid is a foriegn key from dept model
    DepartmentId = models.ForeignKey(Department,on_delete=models.CASCADE)
    #if a dept get deleted all employess under the dept get deleted
    Contact = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.EmployeeName
