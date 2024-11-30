import json

lux_values = [10.2143214512, 30.1343344512, 201.120031209, 26.444129900, 38.11003187320]
msg_origin = "address"
payload =  {
                    "lux": lux_values,
                    "from": msg_origin,
                    "notify": True    
               } 
print(json.dumps(payload, indent=2))