from django.shortcuts import render
from rest_framework import viewsets # type: ignore
from .models import Employee,Department
from django.contrib.auth.models import User
from.serializers import EmployeeSerializer,DepartmentSerializer, UserSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny 
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


# Create your views here.


   #create an APIview for signup
class SignupAPIView(APIView):
    permission_classes = [AllowAny]
#allowany is ggiven for view,because login and signup pages can be viewed by everyone bcoz they are not login users so we give allow anyone to view login and signup page
#defining post function to handle signup post data
#when we use apiview instead of viewset we need to define post 
    def post(self,request):
        #create an object for the signup serializers 
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            #create a new user if the serializer is valid
            user = serializer.save() #will give back a user object
            #after creating the user,create a token for the user
            token, created =   Token.objects.get_or_create(user=user) #will give back token obj
            #once the user is created , give back the response with userid,username,group
            return Response({
                "user_id": user.id ,
                "username": user.username,
                "token": token.key,
                "role": user.groups.all()[0].id if user.groups.exists() else None
                #give back the first role id of the user if the role /groups  exists
            }, status=status.HTTP_201_CREATED )
        else:
            #if the serializer is not valid 
            response ={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

#create an APIview for login
class LoginAPIView(APIView):
    permission_classes=[AllowAny] #Signup does not need logging in

    #defining fn to handle signup post data
    def post(self,request):
        #create an object for the SignupSerializer
        #by giving the data received to its constructor
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            #get the username,password from the validated_data
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            #try to authenticate the user using this username and password
            #if successfully authenticated,it will return back a valid user object

            user = authenticate(request,username=username,password=password)
            if user is not None:
                #get the token for the authenticated user
                token =Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"Success",
                    "username":user.username,
                    "role":user.groups.all()[0].id if user.groups.exists() else None,
                    "data":{
                        "Token":token.key
                    }
                }
                return Response(response,status=status.HTTP_200_OK)#login was success
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid username or password",
            
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED) #login failed
        else:
             #if the serializer is not valid
            response = {'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)



class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all() #get all objects of the model
    serializer_class = DepartmentSerializer #and render it using this render
    permission_classes = [] #to bypass the authentication
    # permission_classes = [IsAuthenticated] #(to restrict for login users)


class EmpolyeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all() 
    serializer_class = EmployeeSerializer 
    #add search option using employee name or designation
    filter_backends = [filters.SearchFilter] #create a search filter
    search_fields = ['EmployeeName', 'Designation'] #add fields to search
    permission_classes = [] #to bypass the authentication
    # permission_classes = [IsAuthenticated]
    
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class = UserSerializer 
        




