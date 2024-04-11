class jsonEnum():  
    def getfield(self, jsn, field, field_result = ""):
            if field in jsn:
                return [jsn[field], f'jsn{field_result}.get("{field}", None)']
            else:
                for key in jsn:
                    if isinstance(jsn[key], dict) and not jsn[key] == {}:
                        if self.getfield(jsn[key], field) != None:
                            return self.getfield(jsn[key], field, field_result=field_result+ f'.get("{key}", {{}})')
                    elif not isinstance(jsn[key], list):
                        continue
                    else:
                        for index in range(0 ,len(jsn[key])):
                            if isinstance(jsn[key][index], list) or isinstance(jsn[key][index], dict):
                                if self.getfield(jsn[key][index], field) != None:
                                    return self.getfield(jsn[key][index], field, field_result= field_result+f'.get("{key}", {{}})[{str(index)}]')
                                else:
                                    continue
        
    def getfields(self, jsn, parent = "", array = False, fields= []):
        if isinstance(jsn, dict):
            for key in jsn:
                if array == True:
                    parent_key = f"{parent}[*]{key}"
                else:
                    parent_key = f"{parent}.{key}"
                if {"field_name" :key, "JSONfield": "", "parent": parent} not in fields and parent == "":
                    fields.append({"field_name" :key, "JSONfield" :f"{parent}{key}", "parent": parent})
                elif {"field_name" :key, "JSONfield": f"{parent}.{key}", "parent": parent} not in fields and parent != "":
                    fields.append({"field_name" :key, "parent": parent, "JSONfield" :parent_key})
                    if isinstance(jsn[key], dict):
                        self.getfields(jsn[key], key, fields)
                elif isinstance(jsn[key], list):
                    for index in range(0, len(jsn[key])):
                        self.getfields(jsn[key][index], key, True,fields)
        return fields
