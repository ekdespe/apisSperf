# flask_graphene_mongo/schema_bk.py
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Users as UsersModel
from models import Point_records as Point_recordsModel
from models import Work_time as Work_timeModel
from querysMongo import Query_Mongo
from graphql import GraphQLError as gError


class Day_of_Works(graphene.Enum):
    Domingo   =   'Domingo'
    Segunda   =   'Segunda'
    Terca     =   'Terça'
    Quarta    =   'Quarta'
    Quinta    =   'Quinta'
    Sexta     =   'Sexta'
    Sabado    =   'Sábado'
    

    @property
    def description(self):
        if self == Day_of_Works.Domingo:
            return ' Domingo | 1º Dia da Semana'
        if self == Day_of_Works.Segunda:
            return 'Segunda-Feira | 2º Dia da Semana'
        if self == Day_of_Works.Terca:
            return 'Terça Feira | 3º Dia da Semana'
        if self == Day_of_Works.Quarta:
            return 'Quarta-Feira| 4º Dia da Semana'
        if self == Day_of_Works.Quinta:
            return 'Quinta-Feira | 5º Dia da Semana'
        if self == Day_of_Works.Sexta:
            return 'Sexta-Feira | 6º Dia da Semana'
        if self == Day_of_Works.Sabado:
            return 'Sábado | Dia de Descanso '

class Point_records(MongoengineObjectType):
    class Meta:
        model = Point_recordsModel
        interfaces= (Node,)


    


class User_records(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
    name              = graphene.String()
    point_records = graphene.List(Point_records)

class User_records_connection(graphene.Connection):
    class Meta:
        node = User_records

class User_worked_time(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
         
    name              = graphene.String()
    worked_time_month = graphene.Int()

class User_worked_time_connection(graphene.Connection):
    class Meta:
        node = User_worked_time

class Point_recordInput(graphene.InputObjectType):
    point_entry_time  = graphene.DateTime()
    point_leave_time  = graphene.DateTime()
    report            = graphene.String()
    point_worked_time_seconds = graphene.Int()

class Work_time(MongoengineObjectType):

    class Meta:
        model = Work_timeModel
        interfaces= (Node,)


class Work_timeInput(graphene.InputObjectType):
    day_of_week = graphene.Field(Day_of_Works)
    entry_time  = graphene.String()
    leave_time  = graphene.String()
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

class UpdateUserInput(graphene.InputObjectType):
        
    name            = graphene.String()
    id_image        = graphene.Int()
    user_name       = graphene.String()
    user_password   = graphene.String()
    image           = graphene.String()
    registration    = graphene.Int(unique=True)
    email           = graphene.String()
    telephone       = graphene.String()



class Set_Point_record_report(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        report = graphene.String()
    point_records = graphene.Field(Point_records)
    @staticmethod
    def mutate(root,info,user_id,report):
            
        point_records = Point_records(
               report = report
               ) 

        q = Query_Mongo();
       
        result = q.Set_point_records_report(user_id,report)
        if result:
            raise gError(result)
        

            
        return CreatePoint_Record(point_records=point_records)



class Set_Point_record_leave_time(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        point_leave_time = graphene.DateTime()
    point_records = graphene.Field(Point_records)
    @staticmethod
    def mutate(root,info,user_id,point_leave_time):
            
        point_records = Point_records(
              
               point_leave_time = point_leave_time
               
               ) 

        q = Query_Mongo();
       
        result = q.Set_point_records_leave_time(user_id,point_leave_time)
        if result:
            raise gError(result)
        

            
        return CreatePoint_Record(point_records=point_records)



class Set_Work_Time(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        day_of_week = Day_of_Works()
        entry_time  = graphene.Time()
        leave_time  = graphene.Time()
        work_day_id = graphene.Int()
    work_time = graphene.Field(Work_time)
    @staticmethod
    def mutate(root,info,user_id,work_day_id,day_of_week=None,entry_time=None,leave_time=None):
            
        work_time = Work_time(
                day_of_week = day_of_week,
                entry_time = entry_time,
                leave_time = leave_time
              
                ) 


        q = Query_Mongo();
       
        result = q.Set_work_time(user_id,work_day_id,day_of_week=day_of_week,entry_time=entry_time,leave_time=leave_time)
        if result:
            raise gError(result)

            
        return Set_Work_Time(work_time = work_time)

class DeleteWork_Time(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        work_day_id = graphene.Int()
    work_time = graphene.Field(Work_time)
    @staticmethod
    def mutate(root,info,user_id,work_day_id):
            
        work_time = Work_time(
                work_day_id = work_day_id

                ) 


        q = Query_Mongo();
       
        result = q.Delete_work_time(user_id,work_day_id)
        if result:
            raise gError(result)

            
        return DeleteWork_Time(work_time = work_time)

class CreateWork_Time(graphene.Mutation):

    class Arguments:
        user_id = graphene.Int()
        day_of_week = Day_of_Works()
        entry_time  = graphene.Time()
        leave_time  = graphene.Time()
        work_day_id = graphene.Int()

    work_time = graphene.Field(Work_time)
    @staticmethod
    def mutate(root,info,user_id,day_of_week,entry_time,leave_time):
            
        work_time = Work_time(
                day_of_week = day_of_week,
                entry_time = entry_time,
                leave_time = leave_time

                ) 


        q = Query_Mongo();
       
        result = q.Create_work_time(user_id,day_of_week,entry_time,leave_time)
        if result:
            raise gError(result)

            
        return CreateWork_Time(work_time = work_time)



class CreatePoint_Record(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        point_entry_time = graphene.DateTime()

    point_records = graphene.Field(Point_records)
    @staticmethod
    def mutate(root,info,user_id,point_entry_time):
            
        point_records = Point_records(
               point_entry_time = point_entry_time
               ) 


        q = Query_Mongo();
       
        result = q.Set_point_records_entry_time(user_id,point_entry_time)
        if result:
            raise gError(result)

            
        return CreatePoint_Record(point_records=point_records)


class DeleteUser(graphene.Mutation):
    class Arguments:
        registration = graphene.Int()
    user = graphene.Field(Users)
    @staticmethod
    def mutate(root,info,registration):
        user_response = user = UsersModel.objects.get(registration=registration)
        user_response.delete()
        return DeleteUser(user=user)



class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UpdateUserInput(required=True)
        registration = graphene.Int()


    user = graphene.Field(Users)
    @staticmethod
    def mutate(root,info,registration,user_data=None):
        UsersModel.objects(registration=registration).update(**user_data)
        user = Users(
               
                name            = user_data.name,
                id_image        = user_data.id_image,
                user_name       = user_data.user_name,
                user_password   = user_data.user_password,
                image           = user_data.image,
                registration    = user_data.registration,
                email           = user_data.email,
                telephone       = user_data.telephone
    
                )
               
        return UpdateUser(user=user)

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
    create_point_record_set_entry_time = CreatePoint_Record.Field()
    set_point_record_leave_time = Set_Point_record_leave_time.Field()
    set_point_record_report = Set_Point_record_report.Field()
    create_work_time = CreateWork_Time.Field()
    set_work_time = Set_Work_Time.Field()
    delete_work_time =DeleteWork_Time.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()


class Query(graphene.ObjectType):
     
    node =  Node.Field()
    user = MongoengineConnectionField(Users)
    user_records = graphene.relay.ConnectionField(User_records_connection, first=graphene.Int(),last=graphene.Int(),month=graphene.Int(),year=graphene.Int())
    user_worked_time = graphene.relay.ConnectionField(User_worked_time_connection, first=graphene.Int(),last=graphene.Int(),reg=graphene.Int(),month=graphene.Int(),year=graphene.Int())
    user_point_records =MongoengineConnectionField( Point_records,first=graphene.Int(),last=graphene.Int(),reg=graphene.Int(),month=graphene.Int(),year=graphene.Int(),day=graphene.Int())
    
    
    
    def resolve_user_point_records(self,info,month,year,reg,day=None,first=None,last=None):
        q = Query_Mongo();
        return list(q.Get_Point_Records_by_registration_month_year(month,year,reg,day))
    
    def resolve_user_records(self,info,month,year,first=None,last=None):
        q = Query_Mongo();
        return list(q.Get_Relatory_Point_Records_month_year(month,year))

    def resolve_user_worked_time(self,info,month,year,reg=None,first=None,last=None):
        q = Query_Mongo();
        return list(q.Get_User_worked_time_month(month,year,reg))
     
    def resolve_users(self,info):
        return list(UsersModel.objects.all())
     
        
        
schema = graphene.Schema(query=Query, types=[Users,Point_records ,Work_time ],mutation=Mutations)
