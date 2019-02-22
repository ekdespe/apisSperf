# flask_graphene_mongo/schema_bk.py
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Users as UsersModel
from models import Work_time as Work_timeModel
from models import Point_records as Point_recordsModel
from querysMongo import Query_Mongo


class Point_records(MongoengineObjectType):
    class Meta:
        model = Point_recordsModel
        interfaces= (Node,)

class Point_recordInput(graphene.InputObjectType):
    point_entry_time  = graphene.DateTime()
    point_leave_time  = graphene.DateTime()
    point_worked_time = graphene.Time()
    report            = graphene.String()

class Work_time(MongoengineObjectType):

    class Meta:
        model = Work_timeModel
        interfaces= (Node,)


class Work_timeInput(graphene.InputObjectType):
    day_of_week = graphene.String()
    entry_time  = graphene.DateTime()
    leave_time  = graphene.DateTime()




class Users(MongoengineObjectType):
    class Meta:
        model = UsersModel
        interfaces= (Node,)
         



class UserInput(graphene.InputObjectType):
        
    name            = graphene.String()
    id_image        = graphene.Int()
    user_name       = graphene.String()
    user_password   = graphene.String()
    image           = graphene.String()
    registration    = graphene.Int(unique=True)
    email           = graphene.String()
    telephone       = graphene.String()
    work_time       = graphene.InputField(Work_timeInput)
    point_records   = graphene.InputField(Point_recordInput)

class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)



    user = graphene.Field(Users)
    @staticmethod
    def mutate(root,info,user_data=None):
        user = Users(
               
                name            = user_data.name,
                id_image        = user_data.id_image,
                user_name       = user_data.user_name,
                user_password   = user_data.user_password,
                image           = user_data.image,
                registration    = user_data.registration,
                email           = user_data.email,
                telephone       = user_data.telephone,
                work_time       = user_data.work_time,
                point_records   = user_data.point_records
    
                )
               
        
        UserSave = UsersModel(
                name            = user_data.name,
                id_image        = user_data.id_image,
                user_name       = user_data.user_name,
                user_password   = user_data.user_password,
                image           = user_data.image,
                registration    = user_data.registration,
                email           = user_data.email,
                telephone       = user_data.telephone,
                work_time       = user_data.work_time,
                point_records   = user_data.point_records
        

                ).save()

        return CreateUser(user=user)

      



    




class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
     
    node =  Node.Field()
    user = MongoengineConnectionField(Users)
     #point_records =( MongoengineConnectionField(Point_records,registration=graphene.Int(),month=graphene.Int(),year=graphene.Int()))
     
    
    #user_ point_records = graphene.List(Point_records,reg=graphene.Int(),month=graphene.Int(),year=graphene.Int())
    #user_point_records = MongoengineConnectionField(Point_records,reg=graphene.Int(),month=graphene.Int(),year=graphene.Int())
    user_point_records = graphene.List(Point_records,first=graphene.Int(),last=graphene.Int(),reg=graphene.Int(),month=graphene.Int(),year=graphene.Int())
    def resolve_user_point_records(self,info,reg,month,year,first=None,last=None,**kargs):
        q = Query_Mongo();
        return list(q.Get_Point_Records_by_registration_month_year(reg,month,year,first,last))
     
    def resolve_users(self,info):
        return list(UsersModel.objects.all())
     

schema = graphene.Schema(query=Query, types=[Users,Point_records ,Work_time ],mutation=Mutations)
