from django.http import JsonResponse
# from codearea.models import History
# from codearea.models import User
from codearea.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
def createhistory(request):
    if request.method=='POST':
        json_data = json.loads(request.body)
        uid=json_data['uid']            
        to = json_data['To']
        fromm=json_data['From']
        try:
            user = User.nodes.get_or_none(uid=uid)
          
            hist=History(To=to,From=fromm,Date=datetime.datetime.now())
            hist.save()
            
            resp=user.history.connect(hist)
            
            response={
                "success":resp
            }
            return JsonResponse(response, safe=False)
        except :
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

def gethistory(request):
    if request.method=='GET':
        # json_data=json.loads(request.body)  # body may uid pass kro user ki
        uid = request.GET.get('uid', ' ')
        try:
            user=User.nodes.get(uid=uid)
            response=[]
            for relation in user.history:
                obj = {
                    "hid": relation.uid, # ya id history k node ki hay
                    "To": relation.To,
                    "From": relation.From,
                    "Date": relation.Date                   
                 }
                                     
                response.append(obj)              
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)





@csrf_exempt
def deletehistroy(request):
    if request.method=='POST':
        json_data=json.loads(request.body)  # body may uid pass kro user ki
        uid=json_data['uid']
        historyid=json_data['hid']  # delete history k time pay mob ui may hid krna hoga
        try:
            user=User.nodes.get(uid=uid)         
            hist=History.nodes.get(uid=historyid)           
            res=user.history.disconnect(hist)
            # print(res)
            response={"message":"deleted"}                    
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
