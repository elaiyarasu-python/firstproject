from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee


# Create your views here.

def Register(request):
   
   return render(request , "customer_form.html")

class EmployeeView(APIView):

    def post(self,request):
       
    #   print(Response.data)

       new_Employee = Employee(name = request.data['name'],
                               department = request.data['department'],
                               email = request.data['email'],
                               salery = request.data['salery'])
       
       new_Employee.save()

       return Response("new Employee added")

    def get (self,request):

        all_employee = Employee.objects.all()
        Employee_list = []
        
        for s in all_employee:

         Employee_dict = {
            "id" : s.id,
            "name":s.name,
            "department":s.department,
            "email":s.email,
            "salery":s.salery
        }
         Employee_list.append(Employee_dict)
        
        return Response(Employee_list)
    

    def patch (self,request,Employee_id):
       
       print(Employee_id, "Employee_id")
       
       Employee_data = Employee.objects.filter(id = Employee_id)

       print(request.data)

       Employee_data.update(name = request.data['name'],
                            department = request.data['department'],
                               email = request.data['email'],
                               salery = request.data['salery'])
       

       print(Employee_data)

       return Response("Employee data update")
    

    def delete(self,request,Employee_id):
       
       Employee_id = Employee.objects.get(id = Employee_id)

       Employee_id.delete()

       return Response("Employee id deteted")
       
    
   
    
    

    

    