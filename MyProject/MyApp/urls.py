from django.urls import path 
from MyApp.views import EmployeeView , Register
from Authentication.views import *


urlpatterns = [
    path('html/', Register),
    path('Employee/',EmployeeView.as_view()),
    path('Employee/<int:Employee_id>/', EmployeeView.as_view()),
    path("customers/", customer_list_create),
    path("customers/<int:id>/", customer_detail),
]
