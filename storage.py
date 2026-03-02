from abc import ABC,abstractmethod 
import json
import os 
class GenericStorage(ABC):
    @abstractmethod
    def add(self,obj):
        pass 

    @abstractmethod 
    def delete(self,id):
        pass 

    @abstractmethod
    def update(self,id,update):
        pass 
    
    @abstractmethod
    def list(self,status):
        pass 
    
class JSONFileStorage(GenericStorage):
   
    def __init__(self):
        self.path = "storage.json"
        if not os.path.exists(self.path):
            with open(self.path,"w") as f:
                res = { "obj_list" : []}
                print(res)
                f.write(json.dumps(res))
    def add(self,obj):
         with open(self.path,"r+") as f:
              res = json.load(f)
              obj_list = res["obj_list"]
              obj_list.append(obj.__dict__)
              res = {"obj_list":obj_list}
              f.seek(0)
              json.dump(res,f)

    def update(self,id, update):
         with open(self.path,"r") as f:
             res = json.load(f)
             obj_list = res["obj_list"]
             for idx,obj in enumerate(obj_list):
                 if obj["id"] == id:
                     obj_list[idx] = {**obj,**update} 
                     res = {"obj_list":obj_list}
                     with open(self.path,"w") as f:
                        json.dump(res,f)
                     return True 
             return False 
        
    def delete(self,id):
         with open(self.path,"r") as f:
             res = json.load(f)
             obj_list = res["obj_list"]
             for idx,obj in enumerate(obj_list):
                 if obj["id"] == id:
                     obj_list.pop(idx)
                     res = {"obj_list":obj_list}
                     with open(self.path,"w") as f:
                         json.dump(res,f)
                     return True 
             return False 

    def list(self,status=None):
         with open(self.path,"r") as f:
             res = json.load(f)
             obj_list = res["obj_list"]
             if status:
                 return list(filter(lambda x : x['status']==status , obj_list))
             return obj_list

