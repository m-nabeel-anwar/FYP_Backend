from django.http import JsonResponse
from codearea.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db

@csrf_exempt
def assigbus(request):
    if request.method=='POST':
        json_data = json.loads(request.body)
        uid=json_data['uid']            #ya driver id hay
        busname = json_data['BusName']
        numberplate=json_data['NumberPlate']
        try:
            driver = BusDriver.nodes.get_or_none(uid=uid)
            bus=SubBus.nodes.get(Name=busname,NumberPlate=numberplate)
            # print(bus)
            # print(driver)
            res=driver.drives.connect(bus)
            driver.Status="Assign"
            driver.save()
            bus.Status="Assign"
            bus.save()          
            response={
                # "uid":feed.uid,
                "message":"Bus Assign"
            }
            return JsonResponse(response, safe=False)
        except :
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

#  isko assign bus , assign driver , delte assign bus show assign  bus may use krlo
def showassignbusdriver(request):
    if request.method=='GET':
        try:
            result=db.cypher_query("Match(D:BusDriver)-[:Drives]->(B:SubBus)" "return D.uid,D.Name,D.Contact,B.uid,B.Name,B.NumberPlate")[0]
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
                    "NumberPlate":record[5],
                }
                # print(obj)
                response.append(obj)
            return JsonResponse(response,safe=False)
        except:
            response={"error":"error occure"}
            return JsonResponse(response,safe=False)
            




@csrf_exempt
def Update_Assign_Driver(request):
    if request.method=='POST':
        json_data = json.loads(request.body)

        NewDriverId = json_data['NewDriverId']            #ya driver id hay
        NewNumberPlate = json_data['NewNumberPlate']
        NewBusName = json_data['NewBusName']

        
        OldDriverId = json_data['OldDriverId']
        OldBusName = json_data['OldBusName']
        OldeNumberPlate=json_data['OldeNumberPlate']

        print(".........NEW")
        print(NewDriverId)
        print(NewNumberPlate)
        print(NewBusName)

        print(".....Old")
        print(OldDriverId)
        print(OldBusName)
        print( OldeNumberPlate)



        try:
            NewBus=SubBus.nodes.get(Name=NewBusName,NumberPlate=NewNumberPlate)
            if NewBus != None:

                OldDriver = BusDriver.nodes.get_or_none(uid=OldDriverId)
                OldBus=SubBus.nodes.get(Name=OldBusName,NumberPlate=OldeNumberPlate)

                OldDriver.Status="Unassign"
                OldDriver.save()
                OldBus.Status="Unassign"
                OldBus.save()
                Old_Relation_Disconnect = OldDriver.drives.disconnect(OldBus)


                NewDriver = BusDriver.nodes.get_or_none(uid=NewDriverId)

                New_Result_Create = NewDriver.drives.connect(NewBus)
                NewDriver.Status="Assign"
                NewDriver.save()
                NewBus.Status="Assign"
                NewBus.save()          
                response={ "message":"New Update Set"}
                return JsonResponse(response, safe=False)

            else:
                response={"message":"Busname and NumberPlate are incorrect"}
                return JsonResponse(response, safe=False)
        except :
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)















@csrf_exempt
def deleteassignbus(request):
     if request.method=='DELETE':

         json_data = json.loads(request.body)
         uid=json_data['uid']            #ya driver id hay
         busname = json_data['BusName']
         numberplate=json_data['NumberPlate']

         try:
             driver = BusDriver.nodes.get_or_none(uid=uid)
             bus=SubBus.nodes.get(Name=busname,NumberPlate=numberplate)
             driver.Status="Unassign"
             driver.save()
             bus.Status="Unassign"
             bus.save()
             res=driver.drives.disconnect(bus)   
            # # print("chal gaya")       
             response={
                # "uid":feed.uid,
                "message":" Assing Bus Deleted"
             }
             return JsonResponse(response, safe=False)
         except :
             response = {"error": "Error occurred"}
             return JsonResponse(response, safe=False)





def singleassigndriver(request):
    if request.method=='GET':
        uid = request.GET.get('uid', ' ')
        try:
            result=db.cypher_query("Match(D:BusDriver{ uid:$uid })-[:Drives]->(B:SubBus)" "return D.uid,D.Name,B.Name,B.NumberPlate",{'uid':uid})[0]
            # print(result)
           
            # response=[]
        # for record in result:
        #     # print(record[0])
        #     # print(record[1])
            record=result[0]
            response={
                "Driverid":record[0],
                "DriverName":record[1],
                # "DriverContact":record[2],
                # "BusId":record[3],
                "BusName":record[2],
                "NumberPlate":record[3],
            }
            # print(obj)
            # response.append(obj)
            return JsonResponse(response,safe=False)
        except:
            response={"error":"error occure"}
            return JsonResponse(response,safe=False)