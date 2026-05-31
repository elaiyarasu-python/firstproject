from django.shortcuts import render , redirect
from django.contrib import messages
import requests


# jwt token login

TOKEN_URL =""

# customer curd

API_URl = ""


def Login_page(request):

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")

        data = {

            "username" :username,
            "password" :password
        }


        response = requests.post(TOKEN_URL, data=data)


        if response.status.code == 200:

            tokens = response.json()

            request.session["acess_token"] = tokens["acess"]
            request.session["refresh_token"] = tokens["refresh"]

            return redirect("dashboard")
        
        else:

            messages.error(request, "invalid username or password")

    return render(request, "login.html")  


def dashboard(request):

    token = request.session.get("acess_token")

    if token is None:

        return redirect("login_page")
    
    headers = {

        "Authorization" : f"Bearer {token}"
    }

    response = request.grt(API_URl,headers=headers)


    if response.status_code == 200:
        customers = response.json()

    else:
        customers = []


    return render(request, "dashboard.html", {"customers":customers})



def add_customer(request):

    token = request.session.get("acess_token")

    if token is None:

        return redirect("login_page")
    
    if request.method == "POST":

        headers = {

            "Authorization" : f"Bearer {token}"
        }

        customer_data = {
            "name" : request.POST.get("name"),
            "email" : request.POST.get("email"),
            "phone" : request.POST.get("phone"),
            "address" : request.POST.get("address"),
        }

        response = request.POST(API_URl,headers = headers, data = customer_data)

        if response.status_code == 201:

            messages.sucess(request,"customer added sucessfully")

        else:
            messages.error(request, "customer not added")

def edit_customer(request , pk):

    token = request.session.get("acess_token")

    if token is None:

        return redirect("login_page")
    
    headers = {
        "Authorization" : f"bearer {token}"
    }

    response = request.get("f{API_URl}{pk}/", headers = headers)

    if response.status_code == 200:

        customer = response.json()

    else:
        customer = None
        messages.error(request, "customer not found")
        return redirect("dashboard")
    

    if request.method == "POST":

        update_data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
        }

        patch_response = requests.patch(
            f"{API_URl}{pk}/",
            headers=headers,
            data=update_data
        )

        if patch_response.status_code == 200:
            messages.success(request, "Customer Updated Successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "Customer Update Failed")

    return render(request, "edit.html", {"customer": customer})

def delete_customer(request, pk):

    token = request.session.get("access_token")

    if token is None:
        return redirect("login_page")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Delete customer
    response = requests.delete(f"{API_URl}{pk}/", headers=headers)

    if response.status_code == 204:
        messages.success(request, "Customer Deleted Successfully")
    else:
        messages.error(request, "Customer Delete Failed")

    return redirect("dashboard")

def logout_page(request):

    # Remove all session data
    request.session.flush()

    messages.success(request, "Logged Out Successfully")
    return redirect("login_page")
    
