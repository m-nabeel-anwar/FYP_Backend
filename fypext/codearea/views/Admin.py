from django.http import JsonResponse
from neo4j import graph
from codearea.models import Admin
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db

def getAlladmins(request):
    if request.method == 'GET':
        try:
            adm = Admin.nodes.all()
            response = []
            # print(adm)
            for admins in adm:
                obj = {
                    "uid": admins.uid,
                    "Name": admins.admin_name,
                    "Email": admins.admin_email,
                    # "password": admins.admin_password,
                    "Contact": admins.admin_contact,
                    "Cnic": admins.admin_cnic,
                    "Address":admins.address
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

@csrf_exempt
def adminlogin(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        try:
        
            admin = Admin.nodes.get_or_none(admin_email=email, admin_password=password) # for condition 
            if admin != None:              
                response = {              
                    "uid": admin.uid,
                    "message":"Found"
                }
                print(Admin.uid)
                return JsonResponse(response,safe=False)              
            else:
                response={"message":"Email or Password are incorrect"}
                return JsonResponse(response,safe=False)
        except:
            response={"error":"Error occurred"}
            return JsonResponse(response,safe=False)


#http://127.0.0.1:8000/getadmin?admin_name=Fariya
@csrf_exempt
def adminDetails(request):
    if request.method == 'GET':
        # get one admin by name
        name = request.GET.get('admin_name', ' ')
        try:
            admin = Admin.nodes.get(admin_name=name)
            response = {
                "uid": admin.uid,
                "Name": admin.admin_name,
                "Email": admin.admin_email,
                # "password": admin.admin_password,
                "Contact": admin.admin_contact,
                "Cnic": admin.admin_cnic,
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        # update one person
        json_data = json.loads(request.body)
        name = json_data['name']
        email = json_data['email']
        # password = json_data['password']
        contact = json_data['contact']
        cnic = json_data['cnic']
        uid = json_data['uid']
        try:
            adm = Admin.nodes.get(uid=uid)
            adm.admin_name = name
            adm.admin_email = email
            # adm.admin_password = password
            adm.admin_contact = contact
            adm.admin_cnic = cnic
            adm.save()
            response = {
                "uid": adm.uid,
                "name": adm.admin_name,
                "email": adm.admin_email,
                "contact": adm.admin_contact,
                "cnic": adm.admin_cnic,
            }
            return JsonResponse(response, safe=False)
        except:
         response = {"error": "Error occurred"}
         return JsonResponse(response, safe=False)







@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        # create one admin
            json_data = json.loads(request.body)
            name = json_data['Name']
            email = json_data['Email']
            password = json_data['Password']
            contact = json_data['Contact']
            cnic = json_data['Cnic']
            address = json_data['Address']

            try:
                check = Admin.nodes.get_or_none(admin_email=email)
                if check == None:
                    bd = Admin(admin_name=name, admin_email=email, admin_password= password, admin_contact= contact, admin_cnic= cnic,address=address)
                    bd.save()
                    response = {
                        "uid": bd.uid,
                        "message":"Admin Registerd"
                    }
                    return JsonResponse(response, safe=False)
                else:
                    response = {"message": "This email already exist"}
                    return JsonResponse(response, safe=False)       
            except:
                response = {"error": "Error occured"}
                return JsonResponse(response, safe=False)

@csrf_exempt
def delete_admin(request):
    if request.method == 'DELETE':
            # delete one person
            json_data = json.loads(request.body)
            uid = json_data['uid']
            try:
                adm = Admin.nodes.get(uid=uid)
                adm.delete()
                response = {"message": "Admin deleted"}
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)



@csrf_exempt
def adminforgetpassword(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        try:            
            user = Admin.nodes.get_or_none(admin_email=email)
            # print(email)
            # print(password)
           
            if user != None: 
                user.admin_password=password
                user.save()
                response = {              
                    "uid": user.uid,
                    "Check":"True"
                }
                return JsonResponse(response,safe=False)              
            else:
                response={"Check":"False"}
                return JsonResponse(response,safe=False)
        except:
            response={"error":"Error occurred"}
            return JsonResponse(response,safe=False)
