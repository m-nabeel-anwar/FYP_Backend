from django.http import JsonResponse
from codearea.models import Feedback
from codearea.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import datetime



def getAllfeeds(request):
     if request.method == 'GET':
        try:
            feed = Feedback.nodes.all()
           
            response = []
            for feeds in feed:
               
                obj = {
                    "uid": feeds.uid,
                    "Name": feeds.Name,
                    "Subject": feeds.Subject,
                    "Feedback":feeds.Feedback,
                    "Date":feeds.Date,        
                }
              
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

@csrf_exempt
def sentfeedback(request):
    if request.method=='POST':
        json_data = json.loads(request.body)
        uid=json_data['uid']            #ya user id hay
        subject = json_data['Subject']
        feedback=json_data['Feedback']
        try:
            user = User.nodes.get_or_none(uid=uid)
        #    print(datetime.datetime.now)
            feed=Feedback(Name=user.Name,Subject=subject,Feedback=feedback,Date=datetime.datetime.now())
            feed.save()
            response={
                "uid":feed.uid,
            }
            return JsonResponse(response, safe=False)
        except :
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
@csrf_exempt
def deletefeedback(request):
    if request.method=='DELETE':
        json_data = json.loads(request.body)
        uid = json_data['uid']
        try:
            user = Feedback.nodes.get(uid=uid)
            user.delete()
            response = {"success": "Feedback deleted"}
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
        