from mongoengine import connect
from models import Users
from models import Users_records
from models import Users_Worked_time
import pprint as p
from bson import json_util
import json
from datetime import datetime


connect('tecnosystem')




class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)






class Query_Mongo:
    
    
    
    def Set_point_records_report(self,user_id,report):
        pipelinne=[
                {"$match":{"registration":user_id}},
                {"$project":{"_id":0,"lastElement":{"$arrayElemAt":["$point_records",-1] }}}
                
                ]
        
        result = list( Users.objects.aggregate(*pipelinne))
        if 'point_entry_time'in result[0]['lastElement']:
            point_entry_time = result[0]['lastElement']['point_entry_time']
            Users.objects(registration=user_id,point_records__point_entry_time=point_entry_time).update_one(set__point_records__S__report=report  )
            result = None
        else:
            result = "Error! There is no point entry registered"
        return result



    def Set_point_records_leave_time(self,user_id,point_leave_time):
        pipelinne=[
                {"$match":{"registration":user_id}},
                {"$project":{"_id":0,"lastElement":{"$arrayElemAt":["$point_records",-1] }}}
                
                ]
        
        result= list( Users.objects.aggregate(*pipelinne))
        if 'report'in result[0]['lastElement']:
            point_entry_time = result[0]['lastElement']['point_entry_time']
            #point_leave_time = datetime.strptime(point_leave_time,'%Y-%m-%dT%H:%M:%S')
            worked_time_seconds = (point_leave_time - point_entry_time).seconds
        #print((worked_time))
        #print(str(worked_time))
        # worked_time_list = json.dumps(worked_time_list,sort_keys=True,default=json_util.default)
       # raw_query =  {"$set": { "point_records.$[elem].worked_time_seconds" :worked_time_seconds }},{ "arrayFilters": [ { "elem.point_entry_time": point_entry_time} ] } 
            result =  Users.objects(registration=user_id,point_records__point_entry_time=point_entry_time).update_one(set__point_records__S__point_leave_time=point_leave_time,set__point_records__S__point_worked_time_seconds=worked_time_seconds  )
        #result =  list(Users.objects(__raw__=raw_query))
        #print(result)
        
            msg = None

        else:
            msg = "Error! Send the your report before registration out "
        
        return msg




    def Set_point_records_entry_time(self,user_id,point_entry_time):
        
        pipelinne=[
                {"$match":{"registration":user_id}},
                {"$project":{"_id":0,"lastElement":{"$arrayElemAt":["$point_records",-1] }}}
                
                ]
        result = list( Users.objects.aggregate(*pipelinne))
        
    
        
        if len(result[0]['lastElement']) != 1 :
            payload = { "point_entry_time":point_entry_time }
            Users.objects(registration=user_id).update_one(push__point_records=payload)
            result = None
        
        else:
           result =  "Error! There is a pendent entry time "
        
        return result
        

    def Get_User_worked_time_month(self,month,year,reg=None):

        if reg:
            pipelinne = [ {"$match":{"registration":reg}},{"$project":{"name":1,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{ "$eq": [{"$month":"$$p_r.point_entry_time"},month] }, { "$eq": [{"$year":"$$p_r.point_entry_time"},year] } ] } }}}},{"$project":{"name":1,"_id":0,"worked_time_month":{"$sum":"$point_records.point_worked_time_seconds"}}} ]

        else:

            pipelinne = [ {"$project":{"name":1,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{ "$eq": [{"$month":"$$p_r.point_entry_time"},month] }, { "$eq": [{"$year":"$$p_r.point_entry_time"},year] } ] } }}}},{"$project":{"name":1,"_id":0,"worked_time_month":{"$sum":"$point_records.point_worked_time_seconds"}}} ]
        
        
        worked_time_list = list(( Users.objects.aggregate(*pipelinne)))
        worked_time_list = json.dumps(worked_time_list,sort_keys=True,default=json_util.default)
        worked_time_list  = Users_Worked_time.objects.from_json(worked_time_list)
        
        return  (worked_time_list)

    

        
    def Get_Relatory_Point_Records_month_year(self,month,year):

        pipelinne = [ 

            {"$match":{"registration":{"$exists":"true"}}},

            {"$project":{"_id":0,"name":1,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month  ] },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]}  ]}}}}}
  
            ]
        users_records = list(( Users.objects.aggregate(*pipelinne)))
        users_records = json.dumps(users_records,sort_keys=True,default=json_util.default)
        users_records = Users_records.objects.from_json(users_records)
        
        return  (users_records)


     
        
    def Get_Point_Records_by_registration_month_year(self,month,year,reg=None,day=None):
 


        if day and reg:
            pipelinne = [ 

            {"$match":{"registration":reg}},

            {"$project":{"_id":0,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month  ] },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]},{"$eq":[{"$dayOfMonth":"$$p_r.point_entry_time"},day ]  }  ]}}}}}
  
            ]
        if  (not day) and reg:
            pipelinne = [ 

            {"$match":{"registration":reg}},

            {"$project":{"_id":0,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month ]  },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]}  ]}}}}}
  
            ]

        users = list(( Users.objects.aggregate(*pipelinne)))
        users = json.dumps(users,sort_keys=True,default=json_util.default)
        users = Users.objects.from_json(users)
        return (users[0]['point_records'])
        

#q = Query_Mongo()
#result = q.Set_point_records_leave_time(5,"2052-05-17T20:00:00")
#result = q.Set_point_records_entry_time(5,"2061-05-17T13:00:00")





