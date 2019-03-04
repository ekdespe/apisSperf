# flask_graphene_mong/models.py
from datetime import datetime
from mongoengine import (Document,EmbeddedDocument)
from mongoengine.fields import (
    DateTimeField, ReferenceField, StringField,IntField,ListField,EmailField,EmbeddedDocumentListField,DynamicField
)



class Work_time(EmbeddedDocument):
    day_of_week = StringField()
    entry_time  = DateTimeField()
    leave_time  = DateTimeField()
    work_day_id = IntField()

class Point_records(EmbeddedDocument):
    point_entry_time  = DateTimeField()
    point_leave_time  = DateTimeField()
    report            = StringField()
    point_worked_time_seconds = IntField()
    

class Users(Document):
    meta            = {'collection': 'users'}
    name            = StringField()
    id_image        = IntField()
    user_name       = StringField()
    user_password   = StringField()
    image           = StringField()
    registration    = IntField(unique=True)
    email           = EmailField()
    telephone       = StringField()
    work_time       = EmbeddedDocumentListField(Work_time)
    point_records   = EmbeddedDocumentListField(Point_records)
    
class Users_records(Document):
    name            = StringField()
    point_records   = EmbeddedDocumentListField(Point_records)
    

class Users_Worked_time(Document):
    name                     = StringField()
    worked_time_month        = IntField()


