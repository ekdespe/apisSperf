from mongoengine import connect
from models import Users
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
    def Get_Point_Records_by_registration_month_year(self,month,year,reg,day):
 

        print(reg)
        print(day)
        print(month) 
        print(year)



        if day and reg:
            pipelinne = [ 

            {"$match":{"registration":reg}},

            {"$project":{"_id":0,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month  ] },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]},{"$eq":[{"$dayOfMonth":"$$p_r.point_entry_time"},day ]  }  ]}}}}}
  
            ]
        if  (not day) and reg:
            pipelinne = [ 

            {"$match":{"registration":kwargs[reg]}},

            {"$project":{"_id":0,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month ]  },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]}  ]}}}}}
  
            ]
        if (not reg) and day:
            pipelinne = [ 

            #{"$match":{"registration":kwargs[reg]}},

            {"$project":{"_id":0,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month]   },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]},{"$eq":[{"$dayOfMonth":"$$p_r.point_entry_time"},day ]  }  ]}}}}}
  
            ]

        if (not reg) and (not day):
            pipelinne = [ 

 #           {"$match":{"registration":kwargs[reg]}},

            {"$project":{"_id":0,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month  ] },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]}  ]}}}}}
  
            ]



        users = list(( Users.objects.aggregate(*pipelinne)))
        users = json.dumps(users,sort_keys=True,default=json_util.default)
        users = Users.objects.from_json(users)
        
        return (users[0]['point_records'])
        

#q = Query_Mongo()
#p.pprint(type((q.Get_Point_Records_by_registration_month_year(5,5,2016))))

