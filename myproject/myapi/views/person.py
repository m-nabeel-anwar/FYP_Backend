from django.http import JsonResponse
from myapi.models import Person
from django.views.decorators.csrf import csrf_exempt
import json


def getAllPersons(request):
    if request.method == 'GET':
        try:
            persons = Person.nodes.all()
            response = []
            for person in persons :
                obj = {
                    "uid": person.uid,
                    "name": person.name,
                    "age": person.age,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)