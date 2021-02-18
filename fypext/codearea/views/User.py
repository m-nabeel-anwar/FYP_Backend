from django.http import JsonResponse
from codearea.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db

from fcm_django.models import FCMDevice
from pyfcm import FCMNotification

import random

def getAlluser(request):
     if request.method == 'GET':
        try:
            user = User.nodes.all()
            response = []
            for users in user :
                obj = {
                    "uid": users.uid,
                    "Name": users.Name,
                    "Email": users.Email,
                    # "Password": users.Password,
                    "Contact": users.Contact,
                    "Cnic": users.Cnic,                    
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)




@csrf_exempt
def userlogin(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        deviceId = json_data['deviceId']
        try:            
            user = User.nodes.get_or_none(Email=email, Password=password)
           
            if user != None:              
                response = {              
                    "uid": user.uid,
                    "Check":"True"
                }
                # send_notification(user.uid,deviceId)
                # save_deviceid(user.uid,deviceId)

                user.Deviceid=deviceId
                user.save()
                # notification_sender()
                return JsonResponse(response,safe=False)              
            else:
                response={"Check":"False"}
                return JsonResponse(response,safe=False)
        except:
            response={"error":"Error occurred"}
            return JsonResponse(response,safe=False)



@csrf_exempt
def ForgetPasswordCode(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        try:            
            user = User.nodes.get_or_none(Email=email)
           
            if user != None: 
                # user.Password=password
                # user.save()
                Contact=user.Contact
                code=varification_alert(Contact)
                response = {              
                    # "uid": user.uid,
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


@csrf_exempt
def ForgetPassword(request):
    if request.method=='POST':
        json_data = json.loads(request.body)       
        email = json_data['Email']
        password = json_data['Password']
        try:            
            user = User.nodes.get_or_none(Email=email)
           
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
def userregistrationtoken(request):
    if request.method == 'POST':           
    # create one person
        json_data = json.loads(request.body)
        #print(json_data)
        name = json_data['Name']
        email = json_data['Email']
        password = json_data['Password']
        contact= json_data['Contact']
        cnic=json_data['Cnic']
        try:
            check = User.nodes.get_or_none(Email=email)
            if check == None:

                # user = User(Name=name,Email=email,Password=password,Contact=contact,Cnic=cnic)
                # user.save()
                code=varification_alert(contact)
                response = {
                "Check":"True",
                "Code":code
                }
                return JsonResponse(response, safe=False)
            else:
                response = {"Check": "False"}
                return JsonResponse(response, safe=False)
        except:

            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)




@csrf_exempt
def userDetails(request):
        if request.method == 'GET':
            uid = request.GET.get('uid', ' ')
            try:
                user = User.nodes.get(uid=uid)
                response = {
                            "uid": user.uid,
                            "Name": user.Name,
                            "Email": user.Email,
                            # "Password": user.Password,
                            "Contact": user.Contact,
                            "Cnic": user.Cnic,
                        }
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)
        
        if request.method == 'POST':           
        # create one person
            json_data = json.loads(request.body)
            #print(json_data)
            name = json_data['Name']
            email = json_data['Email']
            password = json_data['Password']
            contact= json_data['Contact']
            cnic=json_data['Cnic']
            try:
                check = User.nodes.get_or_none(Email=email)
                if check == None:
                    user = User(Name=name,Email=email,Password=password,Contact=contact,Cnic=cnic)
                    user.save()
                    response = {
                            "Check":"True",
                    }
                    return JsonResponse(response, safe=False)
                else:
                    response = {"Check": "False"}
                    return JsonResponse(response, safe=False)
            except :
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)
        
        if request.method == 'PUT':
         # update one person
            json_data = json.loads(request.body)
            name = json_data['Name']
            email = json_data['Email']
            # password = json_data['Password']
            contact= json_data['Contact']
            cnic=json_data['Cnic']
            uid=json_data['uid']
            try:
                user = User.nodes.get(uid=uid)
                user.Name = name
                user.Email=email
                user.Contact=contact
                user.Cnic=cnic
                user.save()
                response = {
                    "uid": user.uid,
                    "Check":"True"
                    # "name": person.name,
                    # "age": person.age,
                }
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)
        
        if request.method == 'DELETE':
            json_data = json.loads(request.body)
            uid = json_data['uid']
            try:
                user = User.nodes.get(uid=uid)
                user.delete()
                response = {"success": "user deleted"}
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)
        



def userlogout(request):

    if request.method == 'GET':        
        uid = request.GET.get('uid', ' ')
        try:
            user = User.nodes.get(uid=uid)
            user.Deviceid="0"
            user.save()
            response = {
                        "Check":"True"
                    }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)




# from django_otp.oath import hotp
# from Twiliosms import varification_alert
# def verificationsms(request):
#     if request.method == 'GET':           
#             json_data = json.loads(request.body)
#             number = json_data['Contact']
#             # print("url wala"+str(number))
#             try:
#                 code=varification_alert(number)

#                 response = {"code":code}
#                 return JsonResponse(response, safe=False)
#             except:

#                 response = {"error": "Error occurred"}
#                 return JsonResponse(response, safe=False)








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








# pip install django_otp
#Your new Phone Number is +12064881819
# from codearea.models import *
 #us = User(name="nabeel",email="smnabeel@gmail.com",password="123456",contact="0321121212",cnic="42101121212")
 # {'id': 'b2071d6c0d8e459b84a52a5e9897cd93', 'name': 'abcdd', 'email': 'smnabeel@gmail.com', 'password': '123456', 'contact': '0321121212', 'cnic': '42101121212'}



# error when enter wrong number
#  POST /Accounts/AC7ba3bf663fa76df26fcca8e1e2323b7d/Messages.json

# Twilio returned the following information:

# Unable to create record: The number  is unverified. Trial accounts cannot send messages to unverified numbers; verify  at twilio.com/user/account/phone-numbers/verified, o
# r purchase a Twilio number to send messages to unverified numbers.

# More information may be available here:

# https://www.twilio.com/docs/errors/21608