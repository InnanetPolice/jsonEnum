class jsonEnum():  
    def getfield(self, jsn, field):
        result = []
        if field in jsn:
            result.append(jsn[field])
        for key in jsn:
            if isinstance(jsn[key], dict) and not jsn[key] == {}:
                result += self.getfield(jsn[key], field)
            elif not isinstance(jsn[key], list):
                continue
            else:
                for index in range(0 ,len(jsn[key])):
                    if isinstance(jsn[key][index], list) or isinstance(jsn[key][index], dict):
                        result += self.getfield(jsn[key][index], field)
        return result
    
    def getfieldpath(self,jsn, field, field_result = ""):
        result = []
        if field in jsn:
            result.append(f'jsn{field_result}.get("{field}", {{}})')
        for key in jsn:
            if isinstance(jsn[key], dict) and not jsn[key] == {}:
                result += self.getfieldpath(jsn[key], field, field_result=field_result+ f'.get("{key}", {{}})')
            elif not isinstance(jsn[key], list):
                continue
            else:
                for index in range(0 ,len(jsn[key])):
                    if isinstance(jsn[key][index], list) or isinstance(jsn[key][index], dict):
                        result += self.getfieldpath(jsn[key][index], field, field_result= field_result+f'.get("{key}", {{}})[{str(index)}]')
        return result
     #use to pull all keys from a JSON object spits each field_name their path's as JSONField and their parent's JSONField if applicable
    def getfields(self, jsn, parent = "", array = False, fields= []):
        if isinstance(jsn, dict):
            for key in jsn:
                if array == True:
                    parent_key = f"{parent}[*]{key}"
                else:
                    if not parent == "":
                        parent_key = f"{parent}.{key}"
                    else:
                        parent_key = key
                if {"field_name" :key, "JSONfield": "", "parent": parent} not in fields :
                    fields.append({"field_name" :key, "JSONfield" :f"{parent_key}", "parent": parent})
                elif {"field_name" :key, "JSONfield": f"{parent_key}", "parent": parent} not in fields and parent != "":
                    fields.append({"field_name" :key, "JSONfield" :parent_key, "parent": parent})
                if isinstance(jsn[key], dict):
                    self.getfields(jsn[key], parent_key, False, fields)
                elif isinstance(jsn[key], list):
                    for index in range(0, len(jsn[key])): 
                        self.getfields(jsn[key][index], parent_key, True,fields)
        return fields