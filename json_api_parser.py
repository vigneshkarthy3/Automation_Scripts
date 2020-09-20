import requests
import json
import sys,re
import subprocess

def loadapi(api_url,list_name,value):
    r = requests.get(api_url)
    dashboard_json=r.json()
    dashboard_str=json.dumps(dashboard_json)
    jsondata=json.loads(dashboard_str)
    list_name=jsondata[value]
    return list_name

# def region_check(region):
#     if len(region) > 3 and 'd' in region:
#         region=re.sub('d','-',region)
#     else:
#         region=region
#     return region
    

if __name__ == "__main__":
    #variables
    entries=[]
    region_entries=[]
    packager = None
    source_ip = None
    multicast_ip = None
    ports = None
    api_url='api_url'
    entries=loadapi(vops_api,entries,"entries")