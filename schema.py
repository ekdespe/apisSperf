# flask_graphene_mongo/schema_bk.py
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Users as UsersModel
from models import Point_records as Point_recordsModel
from models import Work_time as Work_timeModel
from querysMongo import Query_Mongo

class Point_records(MongoengineObjectType):
    class Meta:
        model = Point_recordsModel
        interfaces= (Node,)


class Test_records(graphene.ObjectType):
    user_name = graphene.String()
    


class User_records(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
    name              = graphene.String()
    point_records = graphene.List(Point_records)

class User_records_connection(graphene.Connection):
    class Meta:
        node = User_records

class Point_recordInput(graphene.InputObjectType):
    point_entry_time  = graphene.DateTime()
    point_leave_time  = graphene.DateTime()
    point_worked_time = graphene.DateTime()
    report            = graphene.String()

class Work_time(MongoengineObjectType):

    class Meta:
        model = Work_timeModel
        interfaces= (Node,)


class Work_timeInput(graphene.InputObjectType):
    day_of_week = graphene.String()
    entry_time  = graphene.DateTime()
    leave_time  = graphene.DateTime()
    work_day_id = graphene.Int()




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
    user_records = graphene.relay.ConnectionField(User_records_connection, first=graphene.Int(),last=graphene.Int(),month=graphene.Int(),year=graphene.Int())
    test_records = graphene.List(Test_records)
    user_point_records =MongoengineConnectionField( Point_records,first=graphene.Int(),last=graphene.Int(),reg=graphene.Int(),month=graphene.Int(),year=graphene.Int(),day=graphene.Int())
    
    
    
    def resolve_user_point_records(self,info,month,year,reg,day=None,first=None,last=None):
        q = Query_Mongo();
        return list(q.Get_Point_Records_by_registration_month_year(month,year,reg,day))
    
    def resolve_user_records(self,info,month,year,first=None,last=None):
        q = Query_Mongo();
        return list(q.Get_Relatory_Point_Records_month_year(month,year))

     
    def resolve_users(self,info):
        return list(UsersModel.objects.all())
     
    def resolve_test_records(self,info):
        nomes = [Test_records(user_name='erik'),Test_records(user_name='joao')]
        
        
        
        return nomes
schema = graphene.Schema(query=Query, types=[Users,Point_records ,Work_time,Test_records ],mutation=Mutations)
