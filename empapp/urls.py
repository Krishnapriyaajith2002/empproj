from rest_framework.routers import DefaultRouter 
from . import views 
from django.urls import path

#create an instance of the DefaultRouter class
router = DefaultRouter()
#register the mapping for url and views 
router.register(r'departments',views.DepartmentViewset)
router.register(r'employees',views.EmpolyeeViewset)
router.register(r'users',views.UserViewset)

#creating the urls for the login and signup API views
#They are not viewset,they are api views so it should be addes to the
#url pattern list directly

urlpatterns = [
  path("signup/",views.SignupAPIView.as_view(),name="user-signup"),
  path("login/",views.LoginAPIView.as_view(),name="user-login"),
]
#create a url patterns list from the router urls
urlpatterns += router.urls