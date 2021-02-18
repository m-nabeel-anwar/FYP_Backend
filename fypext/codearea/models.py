from django.db import models

# Create your models here.

from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo,DateProperty,Relationship,FloatProperty

# Create your models here.


class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)



class SubBus(StructuredNode):
    uid = UniqueIdProperty()
    Name = StringProperty(unique_index=True)
    NumberPlate = StringProperty(unique_index=True)
    Status = StringProperty(default="Unassign")
    Speed=FloatProperty(default=0.0)
    Lat=FloatProperty(default=0.0)
    Lng=FloatProperty(default=0.0)



class BusDriver(StructuredNode):
    uid = UniqueIdProperty()
    Name = StringProperty(unique_index=True)
    Email = StringProperty(required=True)
    Password = StringProperty(required=True)
    Contact = StringProperty(index=True, default=0)
    Cnic = StringProperty(unique_index=True)
    Address=StringProperty(required=True)
    Status = StringProperty(default="Unassign")
    Deviceid=StringProperty(default="0")

    drives=RelationshipTo(SubBus,'Drives')



class Admin(StructuredNode):
    uid = UniqueIdProperty()
    admin_name = StringProperty(unique_index=True)
    admin_email = StringProperty(required=True)
    admin_password = StringProperty(required=True)
    admin_contact = StringProperty(index=True, default=0)
    admin_cnic = StringProperty(unique_index=True)
    address=StringProperty(required=True)

# for user
class History(StructuredNode):
    uid=UniqueIdProperty()
    To=StringProperty(required=True)
    From=StringProperty(required=True)
    Date=StringProperty()
    
class Feedback(StructuredNode):
    uid=UniqueIdProperty()
    Name=StringProperty(unique_index=True)
    Subject=StringProperty(required=True)
    Feedback=StringProperty(required=True)
    Date=StringProperty()

class User(StructuredNode):
        uid = UniqueIdProperty()
        Name = StringProperty(unique_index=True)
        Email = StringProperty(required=True)
        Password = StringProperty(required=True)
        Contact = StringProperty(index=True, default=0)
        Cnic = StringProperty(unique_index=True)

        Deviceid=StringProperty(default="0")
    # Reltations:
        history= RelationshipTo(History,'MAINTAIN')

class Station(StructuredNode):
    Name=StringProperty(required=True)
    # Lat=StringProperty()
    Lat=FloatProperty(default=0.0)
    Lng=StringProperty(default=0.0)
    # Lng=StringProperty()


class Bus(StructuredNode):
    Name=StringProperty()
    Fare=IntegerProperty()
    
    name=StringProperty()
    Fare=IntegerProperty(default=0.0) # add kea hay int

    stopat=Relationship(Station,'STOPAT')

    # def std()
    # {
    #     return a;
    # }

