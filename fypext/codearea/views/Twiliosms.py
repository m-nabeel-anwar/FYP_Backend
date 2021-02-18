from django.http import JsonResponse
# from codearea.models import Twilio_sms
from django.views.decorators.csrf import csrf_exempt
import json

# from twilio.rest import Client
# from django_otp.oath import hotp




# def verificationsms(request):
#     if request.method == 'GET':           
#             json_data = json.loads(request.body)
#             # name = request.GET.get('Contact', ' ')
#             number = json_data['Contact']
#             try:
#                 code=varification_alert(number)

#                 response = {"code":code}
#                 return JsonResponse(response, safe=False)
#             except:
#                 response = {"error": "Error occurred"}
#                 return JsonResponse(response, safe=False)


# def varification_alert(number):

  
#     number="+92"+str(number[1:])
#     account_sid='AC7ba3bf663fa76df26fcca8e1e2323b7d'
#     auth_token='c013895716ba80bfa7ab30fbc7622438'
#     client = Client(account_sid, auth_token)
    
#     secret_key = b'1234567890123467890'
#     code=hotp(key=secret_key,counter=1,digits=6)
#     message = client.messages \
#         .create(
#             body='(Buss Arriver) Your varification code is'+str(code),
#             from_='+12064881819',
#             to=number
#         )
#     return str(code)    


# from twilio.rest import Client
# import random

# def varification_alert(number):
#     number="+92"+str(number[1:])
   
#     account_sid='AC7ba3bf663fa76df26fcca8e1e2323b7d'
#     auth_token='c013895716ba80bfa7ab30fbc7622438'
#     client = Client(account_sid, auth_token)

#     code=random.randint(234191,503045)
#     message = client.messages \
#         .create(
#             body='(Buss Arriver) Your varification code is '+str(code),
#             from_='+12064881819',
#             to=number
#         )
#     return str(code)