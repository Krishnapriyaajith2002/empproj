from datetime import date
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from .models import Department, Employee
from .serializers import EmployeeSerializer
from rest_framework import status
# Create your tests here.
class EmployeeViewSetTest(APITestCase):
    #defining a function to setup some basic data for testing
    def setUp(self):
    #create a sample department
       self.department = Department.objects.create(DepartmentName = "HR")
      #create a sample employee object and assign the department
       self.employee = Employee.objects.create(
         EmployeeName = "kichu",
         Designation = "officer",
         DateOfJoining = date(2024,11,13),
         DepartmentId = self.department,
         Contact = "korea",
         IsActive = True
       )
      #since we are testing API,we need to create APIClient object
       self.client = APIClient()

      #TESTCASE 1 : Listing employees

   #defining a function to test employee listing api/endpoint
    def test_employee_list(self):
     #the default reverse url for listing modelname-list
     url = reverse('employee-list')
     response = self.client.get(url) #send the api url and get the response
     #get all employee objects
     employees = Employee.objects.all()
     #create a similar object from employee serializer
     serializer = EmployeeSerializer(employees ,many=True) #get all employees

     #check and compare the response aainst the setup data
     self.assertEqual(response.status_code, status.HTTP_200_OK)
     #check if status code is 200
     self.assertEqual(response.data ,serializer.data)
     #check if serializer data matches the actual data format


     
 #TESTCASE 2 : to get a particular employee details

   #defining a function to test employee listing api/endpoint
    def test_employee_details(self):
     #the default reverse url for listing modelname-list
     #also provide the employee id as argument
     url = reverse('employee-detail' , args=[self.employee.EmployeeId])
     response = self.client.get(url) #send the api url and get the response
     #create a serializer object from EmployeeSerializer using the setup data
     serializer = EmployeeSerializer(self.employee) #get  employees details

     #check and compare the response aainst the setup data
     self.assertEqual(response.status_code, status.HTTP_200_OK)
     #check if status code is 200
     self.assertEqual(response.data ,serializer.data)
     #check if serializer data matches the actual data format


     
 