from rest_framework import serializers # type: ignore #import module
from .models import Employee,Department
#we create a serializer for built in model called user
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    #creating a custom field called group_name
    group_name = serializers.CharField(write_only=True, required=False)
    #write_only means the field will be used for input

    #function to create user
    def create(self,validated_data):
         #we will receiving username,passwd and group_name
    #at first we remove  group name from the validated_data,
    #so that we have only username and passwd to create the user
     group_name = validated_data.pop("group_name",None)
     #as part of the security ,encrypt the password and save it
     validated_data['password'] = make_password(validated_data.get('password'))
     #create the user
     #super is used to refer formal serializer ,here modelserializer is super of signupserializer
     user = super(SignupSerializer,self).create(validated_data)
     #now we can add the created user to the group
     if group_name:
         group , created = Group.objects.get_or_create(name=group_name)
         #attempting to create a group object with the specified group name if not exists
         user.groups.add(group) #add the user to that group
     return user #return the newly created user
    
    class Meta:
        model = User 
        fields = ['username','password','group_name']

class LoginSerializer(serializers.ModelSerializer):
    #creating the custom field for username
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username','password']
        

#create serializer by inheriting ModelSerializer class
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: #will provide metadata to the model
        model = Department
        fields = ('DepartmentId' , 'DepartmentName')
       
        #add function for employee name validation(should be more than 3 chars)

def name_validation(employee_name):
    if len(employee_name)<3:
        raise serializers.ValidationError("Name must be atleast 3 chars")
    return employee_name
        
class EmployeeSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer(source='DepartmentId',read_only=True)

    #adding validation to the field employeename

    EmployeeName = serializers.CharField(max_length=200, validators= [name_validation])
    class Meta: #will provide metadata to the model
        model = Employee
        fields = ( 'EmployeeId','EmployeeName','Designation','DateOfJoining','IsActive','DepartmentId','Department')
         #get all fields


class UserSerializer(serializers.ModelSerializer):
    class Meta: #will provide metadata to the model
        model = User
        fields = ('id','username') #get only these two fields, there are so many other fields bcoz user is a built in class

