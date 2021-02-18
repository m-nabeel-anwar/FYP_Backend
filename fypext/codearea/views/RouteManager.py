from django.http import JsonResponse
from codearea.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db
from rest_framework import status
# import datetime 
from datetime import date

from fcm_django.models import FCMDevice
from pyfcm import FCMNotification

@csrf_exempt
def addroute(request):
	if request.method=='POST':
		json_data=json.loads(request.body)
		To=json_data['To']
		From=json_data['From']
		Lat1=json_data['Lat1']
		Lng1=json_data['Lng1']
		Lat2=json_data['Lat2']
		Lng2=json_data['Lng2']
		distance=json_data['Distance']
		busname=json_data['Name']
		try:
			# print(type(distance)) api say data flote may he a raha hay bus save krnay ka way dhondho
			# print(type(Lat1))
			# result=db.cypher_query("MERGE (a:Station { Name:'"+To+"',Lat:'"+Lat1+"',Lng:'"+Lng1+"' }) MERGE(b:Station {Name:'"+From+"',Lat:'"+Lat2+"',Lng:'"+Lng2+"'}) MERGE(a)-[:NEXT { Distance:'"+distance+"' }]->(b) MERGE(bus:Bus{Name:'"+busname+"'}) MERGE(bus)-[:STOPAT]->(a) MERGE(bus)-[:STOPAT]->(b)")
			query=result="""MERGE (a:Station { Name:$To,Lat:$Lat1,Lng:$Lng1 }) MERGE(b:Station {Name:$From,Lat:$Lat2,Lng:$Lng2}) MERGE(a)-[:NEXT { Distance:$Distance }]->(b) MERGE(a)<-[:NEXT { Distance:$Distance }]-(b) MERGE(bus:Bus{Name:$busname}) MERGE(bus)-[:STOPAT]->(a) MERGE(bus)-[:STOPAT]->(b)"""
			result,meta=db.cypher_query(query,{'To':To,'From':From,'Lat1':Lat1,'Lng1':Lng1,'Lat2':Lat2,'Lng2':Lng2,'Distance':distance,'busname':busname})
			response={"message":"Route added"}
			return JsonResponse(response,safe=False)
		except:
			response={"erro":"Error occure"}
			return JsonResponse(response,safe=False)


	
	
# @csrf_exempt
# def updateroute(request):
#     if request.method=='POST':
#         json_data=json.loads(request.body)



@csrf_exempt
def deleteroute(request):
	if request.method=='DELETE':
		json_data=json.loads(request.body)
		route=json_data['Route']
		busname=json_data['Name']
		try:
			station=Station.nodes.get_or_none(Name=route)
			bus=Bus.nodes.get_or_none(Name=busname)
			#result=bus.stopat.connect(station)
		# print(bus.stopat.is_connected(station))
			if bus.stopat.is_connected(station):
				result=bus.stopat.disconnect(station)
				response={"message":"Route deleted"}
			else:
				response={"message":"Route not exist"}
			return JsonResponse(response,safe=False) 
		except:
			response={"erro":"Error occure"}
			return JsonResponse(response,safe=False)



# single route update ho gay yaha us k agay k sab update khud ni ho gay krna paray ga kkhud say
@csrf_exempt
def updateroute(request):
	if request.method=='PUT':
		json_data=json.loads(request.body)
		newroute=json_data['NewRoute']
		route=json_data['Route']
		busname=json_data['Name']
		try:
			station=Station.nodes.get_or_none(Name=route)
			newstation=Station.nodes.get_or_none(Name=newroute)
			bus=Bus.nodes.get_or_none(Name=busname)
		# result=bus.stopat.connect(station)
		# print(bus.stopat.is_connected(station))
			if bus.stopat.is_connected(station):
				result=bus.stopat.disconnect(station)
				res=bus.stopat.connect(newstation)

				notification_sender(bus.Name)
				response={"message":"Route updated"}
			else:
				response={"message":"Route not exist"}
			return JsonResponse(response,safe=False) 
		except:
			response={"erro":"Error occure"}
			return JsonResponse(response,safe=False)

		
push_service = FCMNotification(api_key="AAAAuQxSVZA:APA91bEeqAnBCoosLSvW4fRHVnOVH861jqMELsTLMcGWMOQZjgtH2NceNQOKqM0AEKhwxaP8ndIFdQSqZNZp-jPTnoIpsVTXy4_NYP5z9Ljwm9Jzp2i3PxW35as0fVDMK6c60ShxfQRr")
def notification_sender(bus):

	query="""match(u:User) where u.Deviceid <> '0' return u.Deviceid"""
	result,meta=db.cypher_query(query)
	for device_id in result:
		res=push_service.notify_single_device(registration_id=device_id[0], message_title="Bus Arriver", message_body=str(bus)+" Route update goto find bus and see new route")








# w11 k saray route show k lea
def showbusroute(request):
    if request.method=='GET':
        busname = request.GET.get('Name', ' ') #?Name=W11 url may likho
	   
        try:
            bus=Bus.nodes.get_or_none(Name=busname)
            response=[]
            for relation in bus.stopat:
                obj = {
                    "id": relation.id, 
                    "Name":relation.Name,
					"Lat": relation.Lat,
					"Lng":relation.Lng,                
                 }
                                     
                response.append(obj)              
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)						  
			

def showbusnamelist(request):
    if request.method == 'GET':
        try:
            bus=Bus.nodes.all()
            response = []
            #print(bd)
            for buses in bus:
                obj = {
                    "uid": buses.id,
					"Name":buses.Name,
				}                  
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)		

# jo hamaray system may bus k route hay in k lea is may  lat long bhi ae ga
def showroutelist(request):
    if request.method == 'GET':
        try:
            station=Station.nodes.all()
            response = []
            #print(bd)
            for stations in station:
                obj = {
                    "id": stations.id,
					"Name": stations.Name,
					"Lat": stations.Lat,
					"Lng":stations.Lng,
				}                  
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)



# native may api run k lea adb -s emulator-5554 reverse tcp:8000 tcp:8000


# fare k lea add/updaye

@csrf_exempt
def addfare(request):
	if request.method=='POST':

		json_data=json.loads(request.body)
		Name=json_data['Name']
		Fare=json_data['Fare']
		try:
			query="""MERGE (bus:Bus{ Name: $Name }) SET bus.Fare=$Fare  return bus.Fare"""
			result,meta=db.cypher_query(query,{'Name':Name,'Fare':Fare})
			# print(result)
			response={"message":"Now Fare is Rs."+str(result[0][0])}
			return JsonResponse(response,safe=False)
		except:
			response={"erro":"Error occure"}
			return JsonResponse(response,safe=False)


		






@csrf_exempt
def routefinder(request):
	if request.method=='POST':

		json_data=json.loads(request.body)
		SearchTo=json_data['To']
		
		SeacrhFrom=json_data['From']
		# SearchTo="A"
		# SeacrhFrom="E"
		uid=json_data['uid']
		# try:
		query="""MATCH (a:Station { Name:$To }), (d:Station {Name: $From}) MATCH route =  allShortestPaths((a)-[:STOPAT*]-(d)) return[x IN NODES(route) | CASE WHEN x:Station THEN   x.Name WHEN x:Bus THEN   x.Name ELSE '' END] AS itinerary"""
		Recommended_Route,meta=db.cypher_query(query,{'To':SearchTo,'From':SeacrhFrom})
		
		
		OuterRoute=[] 
		# OuterRoute={}


		route_id = 0
		for Recommended_Route_Result in Recommended_Route:   # yaha wo route aye gay jo system nay recommend kea hay e.g[Route A,Bus 2, Route D]
			Route = []
			# i=i+1
			i=0
			for x in range(2,len(Recommended_Route_Result[0]),2):
			# 	# print(data[i])
				
				Source = Recommended_Route_Result[0][i]
				Destination = Recommended_Route_Result[0][i+2]
				BusName = Recommended_Route_Result[0][i+1]

				busfare=Bus.nodes.get_or_none(Name=BusName) # bus ka fare yaaha say a raaha hay
				Fare=busfare.Fare

				i=i+2
				
				Count_Array=[]
				Route_Distance=[]
				query="""MATCH (a:Station { Name:$Source}), (d:Station {Name:$Destination}) match stops = allShortestPaths((a)-[:NEXT*]->(d)) RETURN [x in NODES(stops)| case when x:Station then x.Name else ''end] as rastay, REDUCE(d = 0, x IN RELATIONSHIPS(stops) | d + x.Distance) AS distance"""
				Particular_Route_List, meta = db.cypher_query(query,{'Source':Source,'Destination':Destination})
				

				for Particular_Route_List_Output in Particular_Route_List:  # is say saray mide nodes ae gay Like A-D pay anay kay saray nodes ae gay
					# print(Particular_Route_List_Output[0])

				# 	# distance.append(rel[0])
					# print(Particular_Route_List_Output[1])

					Route_Distance.append(Particular_Route_List_Output[1])
					
				
					Stop_Count=0
				
					for Singel_Bu_Stop in Particular_Route_List_Output[0]: # is loop sayh hamay sigle node milay ge jisay ham agay pas kar kay stop at check karay gay
						# print('0.', Singel_Bu_Stop)
						
				
						query="match (bus:Bus{ Name:$BusName}), (s:Station{ Name:$result}), p=(bus)-[:STOPAT]->(s) return p"
						Bus_StopAt_Or_Not, meta = db.cypher_query(query,{'BusName':BusName,'result':Singel_Bu_Stop})

						for condition in Bus_StopAt_Or_Not:
							# print(rell)
							if condition!=None:
								Stop_Count= Stop_Count+1


					Count_Array.append(Stop_Count)
					# print(Stop_Count)


				# print('2.',Count_Array)
				# print('3.', Count_Array.index(max(Count_Array)))
				# print('Reult of right path distance4.', Route_Distance[Count_Array.index(max(Count_Array))]) # distance a raah hay jo select kea hay us ka
				Distance =  Route_Distance[Count_Array.index(max(Count_Array))]

				if Distance >=5 and Distance <=10.5:
					Fare = Fare+5

				if Distance >=10.5 and Distance <=15.5:
					Fare = Fare+10
				if Distance >=15.5 and Distance <=20.5:
					Fare = Fare+15
				if Distance >=20.5 and Distance <=25.5:
					Fare = Fare+20
				if Distance >=26:
					Fare = Fare+25

				obj={
					"To":Source,
					"From":Destination,
					"BusName":BusName,
					"Fare":Fare,
					"Distance":round(Distance,2)
				}
				Route.append(obj)

			route_id += 1
			single_route_dict = {"id":route_id, "route_name": "Route "+str(route_id), "route":Route}
			OuterRoute.append(single_route_dict)


		# print(OuterRoute)
		# response={"ok":"Done"}
		# response={"route":OuterRoute}
		# return JsonResponse(response,safe=False)
		sethistory(SearchTo,SeacrhFrom,uid)

		return JsonResponse(OuterRoute,safe=False)
		# except:
		# 	response={"erro":"Error occure"}
		# 	return JsonResponse(response,safe=False)



# @csrf_exempt
def sethistory(To,From,uid):

	user = User.nodes.get_or_none(uid=uid)	
	hist=History(To=To,From=From,Date=date.today())
	hist.save()	
	resp=user.history.connect(hist)	
	# response={
	# 	"success":
	# }
	return True
        # except :
        #     response = {"error": "Error occurred"}
        #     return JsonResponse(response, safe=False)














