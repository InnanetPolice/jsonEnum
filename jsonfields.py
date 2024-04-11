import json
f = open('./users_1.7m.json', 'r')
jsn = json.load(f)

def getfield(jsn, field, field_result = ""):
         if field in jsn:
             return [jsn[field], f'jsn{field_result}.get("{field}", None)']
         else:
             for key in jsn:

                 if isinstance(jsn[key], dict) and not jsn[key] == {}:
                     if getfield(jsn[key], field) != None:
                         return getfield(jsn[key], field, field_result=field_result+ f'.get("{key}", {{}})')
                 elif not isinstance(jsn[key], list):
                     continue
                 else:
                     for index in range(0 ,len(jsn[key])):
                         if isinstance(jsn[key][index], list) or isinstance(jsn[key][index], dict):
                             if getfield(jsn[key][index], field) != None:
                                 return getfield(jsn[key][index], field, field_result= field_result+f'.get("{key}", {{}})[{str(index)}]')
                             else:
                                 continue
def getfields(jsn, parent = "root", fields= []):
    if isinstance(jsn, dict):
        for key in jsn:
            if {"JSONfield" :key, "parent": parent} not in fields:
                fields.append({"JSONfield" :key, "parent": parent})
            if isinstance(jsn[key], dict):
                getfields(jsn[key], key, fields)
            elif isinstance(jsn[key], list):
                for index in range(0, len(jsn[key])):
                    getfields(jsn[key][index], key,fields)
    return fields

print(getfields(jsn[0]))