# flask_graphene_mongo/database.py
from mongoengine import connect

from models import Users, Point_records, Work_time

connect('tecnosystem', host='mongodb://localhost', alias='default')


def init_db():
    None
