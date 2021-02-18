from django.http import JsonResponse
from codearea.models import BusDriver
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db
from rest_framework import status
import random


def getAllbus_drivers(request):
    if request.method == 'GET':
        try:
            bd = BusDriver.nodes.all()
            response = []
            #print(bd)
            for drivers in bd:
                obj = {
                    "uid": drivers.uid,
                    "Name": drivers.Name,
                    "Email": drivers.Email,
                    #"password": drivers.password,
                    "Contact": drivers.Contact,
                    "Cnic": drivers.Cnic,
                    "Address":drivers.Address,
                    "Status":drivers.Status
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except ValueError as e:
            # response = {"error": "Error occurred"}
            # return JsonResponse(response, safe=False)
            return JsonResponse(e.args[0],status.HTTP_400_BAD_REQUEST)

def getunassigndriver(request):
    if request.method == 'GET':
        try:
            bd=BusDriver.nodes.filter(Status='Unassign')

            response = []
            #print(bd)
            for drivers in bd:
                obj = {
                    "uid": drivers.uid,
                    "Name": drivers.Name,
                    "Email": drivers.Email,
                    #"password": drivers.password,
                    "Contact": drivers.Contact,
                    "Cnic": drivers.Cnic,
                    "Address":drivers.Address,
                    "Status":drivers.Status
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

@csrf_exempt
def driverlogin(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        device_Id = json_data['deviceid']
        try:
            
            driver = BusDriver.nodes.get_or_none(Email=email, Password=password) # for condition 
            if driver != None:              
                response = {              
                    "uid": driver.uid,
                    "Status":driver.Status,
                    "Check":"True"
                }
                driver.Deviceid=device_Id
                driver.save()

                return JsonResponse(response,safe=False)              
            else:
                response={"Check":"False"}
                return JsonResponse(response,safe=False)
        except:
            response={"error":"Error occurred"}
            return JsonResponse(response,safe=False)

def Driverlogout(request):

    if request.method == 'GET':        
        uid = request.GET.get('uid', ' ')
        try:
            Driver = BusDriver.nodes.get(uid=uid)
            Driver.Deviceid="0"
            Driver.save()
            response = {
                        "Check":"True"
                    }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)


@csrf_exempt
def DriverForgetPassword(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        try:            
            user = BusDriver.nodes.get_or_none(Email=email)
           
            if user != None: 
                user.Password=password
                user.save()
                response = {              
                    # "uid": user.uid,
                    "Check":"True"
                }
                return JsonResponse(response,safe=False)              
            else:
                response={"Check":"False"}
                return JsonResponse(response,safe=False)
        except:
            response={"error":"Error occurred"}
            return JsonResponse(response,safe=False)




@csrf_exempt
def DriverForgetPasswordCode(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        try:            
            user = BusDriver.nodes.get_or_none(Email=email)
           
            if user != None: 

                Contact=user.Contact
                code =varification_alert(Contact)

                response = {              
                    "Check":"True",
                    "Code":code
                }
                return JsonResponse(response,safe=False)              
            else:
                response={"Check":"False"}
                return JsonResponse(response,safe=False)
        except:
            response={"error":"Error occurred"}
            return JsonResponse(response,safe=False)





# for message sending 
from twilio.rest import Client

def varification_alert(number):
    number="+92"+str(number[1:])
   
    account_sid='AC7ba3bf663fa76df26fcca8e1e2323b7d'
    auth_token='c013895716ba80bfa7ab30fbc7622438'
    client = Client(account_sid, auth_token)

    code=random.randint(234191,503045)
    message = client.messages \
        .create(
            body='(Buss Arriver) Your varification code is '+str(code),
            from_='+12064881819',
            to=number
        )
    return str(code)















#http://127.0.0.1:8000/getadmin?admin_name=Fariya

@csrf_exempt
def driverDetails(request):
    if request.method == 'GET':
        # get one driver by name
        uid = request.GET.get('uid', ' ')
        try:
            drivers = BusDriver.nodes.get(uid=uid)
            response = {
                "uid": drivers.uid,
                "Name": drivers.Name,
                "Email": drivers.Email,
                #"password": drivers.password,
                "Contact": drivers.Contact,
                "Cnic": drivers.Cnic,
                "Address":drivers.Address,
                "Status":drivers.Status
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'POST':
     # create one driver
        json_data = json.loads(request.body)
        name = json_data['Name']
        email = json_data['Email']
        password = json_data['Password']
        contact = json_data['Contact']
        cnic = json_data['Cnic']
        address = json_data['Address']

        try:
            check = BusDriver.nodes.get_or_none(Email=email)
            if check == None:
                bd = BusDriver(Name=name, Email=email, Password= password, Contact= contact, Cnic= cnic,Address=address)
                bd.save()
                response = {
                    "uid": bd.uid,
                    "message":"Driver Registerd"
                }
                return JsonResponse(response, safe=False)
            else:
                response = {"message": "This email already exist"}
                return JsonResponse(response, safe=False)       
        except:
            response = {"error": "Error occured"}
            return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        # update one driver
        json_data = json.loads(request.body)
        name = json_data['Name']
        email = json_data['Email']
        # password = json_data['Password']
        contact = json_data['Contact']
        cnic = json_data['Cnic']
        address = json_data['Address']
        uid = json_data['uid']
        try:
            bd = BusDriver.nodes.get(uid=uid)
            
            bd.Name = name
            bd.Email = email
            # bd.Password = password
            bd.Contact = contact
            bd.Cnic = cnic
            bd.Address=address
            bd.save()
            response = {
                "uid": bd.uid,
                # "Name": drivers.Name,
                # "Email": drivers.Email,
                # #"password": drivers.password,
                # "Contact": drivers.Contact,
                # "Cnic": drivers.Cnic,
                # "Address":drivers.Address,
                # "Status":drivers.Status
                "message":"Information updated"
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'DELETE':
          # delete one driver
        json_data = json.loads(request.body)
        # print(json_data)
        uid = json_data['uid']
        #   print(uid)
        try:   
            adm = BusDriver.nodes.get(uid=uid)
            if adm.Status=='Unassign':
                adm.delete()
                response = {"message": "Driver Deleted"}               
            else:
                query="""Match(d:BusDriver) where d.uid=$uid  match(d)-[:Drives]->(b:SubBus) Set b.Status='Unassign' detach delete d"""
                result=db.cypher_query(query,{'uid':adm.uid})[0]
                response = {"message": "Driver Deleted"}            
            return JsonResponse(response, safe=False)            
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)




def get_single_assign_driver(request):
    if request.method == 'GET':
          # delete one driver
        uid = request.GET.get('uid', ' ')
        try:  
            Driver = BusDriver.nodes.get(uid=uid)
        
            query="""Match(d:BusDriver) where d.uid=$uid  match(d)-[:Drives]->(b:SubBus) return d.uid , d.Name , d.Email,d.Cnic,d.Contact,d.Address,b.Name,b.NumberPlate"""
            result=db.cypher_query(query,{'uid':Driver.uid})[0][0]
            # ,[])

            response = {
                "uid":result[0],
                "Name":result[1],
                "Email":result[2],
                "Cnic":result[3],
                "Contact":result[4],
                "Address":result[5],
                "BusName":result[6],
                "NumberPlate":result[7],

            }            
            return JsonResponse(response, safe=False)            
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)


# match(d:BusDriver) where d.uid='a93b0d960f9a4606878f2c618ebf2e7b'
# match(d)-[:Drives]->(b:SubBus) return b.Name,d.Name