from django.http import JsonResponse
from codearea.models import SubBus
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db
def getAll_sub_bus(request):
    if request.method == 'GET':
        try:
            sb = SubBus.nodes.all()
            response = []
            for subbus in sb:
                obj = {
                    "uid": subbus.uid,
                    "Name": subbus.Name,
                    "NumberPlate": subbus.NumberPlate,
                    "Status": subbus.Status,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

# assign bus or asssign driver dono may use krlo isko
def getassignbus(request):
    if request.method=='GET':
        try:
            result=db.cypher_query("Match(D:BusDriver)-[:Drives]->(B:SubBus)" "return D.uid,D.Name,D.Contact,B.uid,B.Name,B.NumberPlate,D.Email,D.Address,D.Status,B.Status")[0]
            # print(result)
            
            response=[]
            for record in result:
                # print(record[0])
                # print(record[1])
                obj={
                    "Driverid":record[0],
                    "DriverName":record[1],
                    "DriverContact":record[2],
                    "BusId":record[3],
                    "BusName":record[4],
                    "NumberPlate": record[5],
                    "Email": record[6],
                    "Address":record[7],
                    "DriverStatus":record[8],
                    "BusStatus":record[9],

                    
                }
                # print(obj)
                response.append(obj)
            return JsonResponse(response,safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)


def getunassignbus(request):
    if request.method == 'GET':
        try:
            #status='Unassign'
            # status = request.GET.get('Status', ' ')
            # print(status)
            # #sb = SubBus.nodes.get(Status=status)
            sb=SubBus.nodes.filter(Status='Unassign')
            response = []
            for subbus in sb:
                obj = {
                    "uid": subbus.uid,
                    "Name": subbus.Name,
                    "NumberPlate": subbus.NumberPlate,
                    "Status": subbus.Status,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)




def distinctunassignbus(request):
    if request.method == 'GET':
        try:
            # sb=SubBus.nodes.filter(Status='Unassign') 
            sb=db.cypher_query("match (b:SubBus) where b.Status='Unassign' return DISTINCT b.Name As Name")[0]
            # print(sb)
            response = []
            i=0
            for subbus in sb:
               
                obj = {
                    "uid": str(i),
                    "Name": subbus[0],              
                  
                }
             
                i=i+1
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)










def getbusnumber(request):
    if request.method == 'GET':
        name = request.GET.get('Name', ' ') #?Name=W11 url may likho
        try:
            sb = SubBus.nodes.filter(Name=name,Status='Unassign')
            response=[]
            for bus in sb:
                    obj = {
                        "uid": bus.uid,
                        "NumberPlate": bus.NumberPlate,
                        # "Status": sb.Status,
                    }
                    response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    





#http://127.0.0.1:8000/getadmin?admin_name=Fariya

@csrf_exempt
def get_Sub_bus(request):
    if request.method == 'GET':
        # get one sub_bus by name
        uid = request.GET.get('uid', ' ')
        try:
            sb = SubBus.nodes.get(uid=uid)
            response = {
                "uid": sb.uid,
                "Name": sb.Name,
                "NumberPlate": sb.NumberPlate,
                # "Status": sb.Status,
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'POST':
     # create one sub_bus
        json_data = json.loads(request.body)
        name = json_data['Name']
        number_plate = json_data['NumberPlate']
        # status = json_data['Status']
        try:
            check = SubBus.nodes.get_or_none(NumberPlate=number_plate)
            if check == None:               
                sb = SubBus(Name=name, NumberPlate= number_plate)             
                sb.save()
                # response = {
                # "uid": sb.uid,
                # }
                response={
                "message":"New Bus added",
                }
                return JsonResponse(response, safe=False)
            else:
                response = {"message": "Bus already exist"}
                return JsonResponse(response, safe=False)       
        except:
            response = {"error": "Error occured"}
            return JsonResponse(response, safe=False)
            
    if request.method == 'PUT':
        # update one sub_bus
        json_data = json.loads(request.body)
        name = json_data['Name']
        number_plate = json_data['NumberPlate']
        # status = json_data['Status']
        uid = json_data['uid']
        try:
            sb = SubBus.nodes.get(uid=uid)
            sb.Name = name
            sb.NumberPlate = number_plate
            sb.Status = sb.Status
            sb.save()
            # response = {
            #     "uid": sb.uid,
            #     # "Name": sb.Name,
            #     # "NumberPlate": sb.NumberPlate,
            #     # "Status": sb.Status,
            # }
            response={"message":"BusUpdate"}
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'DELETE':
          # delete one sub_bus
          json_data = json.loads(request.body)
          uid = json_data['uid']
          try:
              adm = SubBus.nodes.get(uid=uid)
              if adm.Status == 'Unassign':
                  adm.delete()
                  response = {"message": "Unassignbus deleted"}
              else:

                  query="""Match(d:SubBus) where d.uid=$uid  match(d)-[:Drives]->(b:BusDriver) Set b.Status='Unassign' detach delete d"""
                  result=db.cypher_query(query,{'uid':adm.uid})[0]
                  response = {"message": "Assign bus deleted"}
              return JsonResponse(response, safe=False)
          except:
              response = {"error": "Error occurred"}
              return JsonResponse(response, safe=False)


@csrf_exempt
def get_bus_location(request):
    if request.method=='POST':
        
        # print(request.body)
        json_data = json.loads(request.body)
        # print("body")
        BusName = json_data['BusName']
        NumberPlate = json_data['NumberPlate']
        Lat = json_data['Lat']
        Lng = json_data['Lng']
        Speed = json_data['Speed']
        # print(BusName)
        # print(NumberPlate)
        # print(Lat)
        # print(Lng)
        # print(Speed)

        try:

            query="""Match(d:SubBus) where d.Name=$Name And d.NumberPlate = $NumberPlate SET d.Lat=$Lat , d.Lng=$Lng , d.Speed=$Speed return d.Lat , d.Lng"""
            result=db.cypher_query(query,{'Name':BusName,'NumberPlate':NumberPlate,'Lat':Lat,'Lng':Lng,'Speed':Speed})[0][0]

            response = {
                "Lat":result[0],
                "Lng":result[1]
            }
            return JsonResponse(response, safe=False)
                
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
