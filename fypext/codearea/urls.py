from django.conf.urls import url
from codearea.views import *
from django.urls import path
urlpatterns = [

    #person
    path('person',personDetails),
    path('getAllPersons',getAllPersons),

#user url
    path('getuser',getAlluser),
    path('getuserdetail',userDetails),
    path('userlogin',userlogin),
    path('ForgetPassword',ForgetPassword),
    path('userlogout',userlogout),
    path('ForgetPasswordCode',ForgetPasswordCode),
    path('userregistrationtoken',userregistrationtoken),

# driver url
    path('getalldriver', getAllbus_drivers),
    path('getdriver',driverDetails),
    path('getunassigndriver',getunassigndriver),
    path('driverlogin',driverlogin),
    path('DriverForgetPassword',DriverForgetPassword),
    path('getsinglederiver',get_single_assign_driver),
    path('Driverlogout',Driverlogout),
    path('DriverForgetPasswordCode',DriverForgetPasswordCode),


# bus url
    path('getallsubbus', getAll_sub_bus),
    path('getsubbus', get_Sub_bus), 
    path('getunassignbus', getunassignbus),
    path('getbusnumber', getbusnumber),
    path('getassignbus',getassignbus),
    path('distinctunassignbus',distinctunassignbus),
    path('getbuslocation',get_bus_location),
    
# admin url
    path('getAlladmins',getAlladmins),
    path('getadmin',adminDetails),
    path('adminlogin',adminlogin),
    path('registeradmin',register_admin),
    path('deleteadmin',delete_admin),
    path('adminforgetpassword',adminforgetpassword),

# feedback
    path('getAllfeeds',getAllfeeds),
    path('sentfeedback',sentfeedback),
    path('deletefeedback',deletefeedback),
# history    
    path('createhistory',createhistory),
    path('gethistory',gethistory),
    path('deletehistroy',deletehistroy),

# assign bus
    path('showassignbusdriver',showassignbusdriver),
    path('assigbus',assigbus),
    path('deleteassignbus',deleteassignbus),
    path('singleassigndriver',singleassigndriver),
    path('updateassingdriver',Update_Assign_Driver),

#routemanager
    path('addroute',addroute),
    path('deleteroute',deleteroute),
    path('updateroute',updateroute),
    path('showbusroute', showbusroute),
    path('showbusnamelist', showbusnamelist),
    path('showroutelist',showroutelist), # station k nam ajae gay is say
    path('addfare',addfare),
    path('routefinder',routefinder)

# sms alert
    # path('verificationsms',verificationsms)    

]
