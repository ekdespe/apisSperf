from mongoengine import connect
from models import Users
from models import Users_records
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
    def Get_Relatory_Point_Records_month_year(self,month,year):

        pipelinne = [ 

            {"$match":{"registration":{"$exists":"true"}}},

            {"$project":{"_id":0,"name":1,"point_records":{"$filter":{"input":"$point_records","as":"p_r","cond": { "$and":[{  "$eq": [{"$month":"$$p_r.point_entry_time"},month  ] },   { "$eq": [{"$year":"$$p_r.point_entry_time"},year]}  ]}}}}}
  
            ]
        users = list(( Users.objects.aggregate(*pipelinne)))
        users = json.dumps(users,sort_keys=True,default=json_util.default)
        users = Users_records.objects.from_json(users)
        #print('tamanho ->',len(users[0][0]))
        #for k in users:
        #    print(k)
        #    print('----------')
        #print('conteudo ->',users[0][0])
        #print(users)
        #print(type(users[0]))
        
        return  (users)
        #return (users[0]['point_records'])


     
        
    def Get_Point_Records_by_registration_month_year(self,month,year,reg=None,day=None):
 

        print('reg -> ',reg)
        print('day -> ',day)
        print('month -> ',month)
        print('year -> ',year)


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
        #print('tamanho ->',len(users))
        #print(users)
        return (users[0]['point_records'])
        

q = Query_Mongo()
result = q.Get_Relatory_Point_Records_month_year(5,2016)


#print(result)



