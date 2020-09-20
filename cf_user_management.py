import os
import sys
import cf_api
import json
import subprocess

def get_space_details(name_type,name):
    req=cc.request(name_type).set_query(q='name:'+ name)
    res=req.get()
    #print(str(res.response.status_code) + ' ' + res.response.reason)
    if res.has_error:
        print(str(res.error_code) + ': '+ str(res.error_messae))
        sys.exit(1)
    name_url=res.resource.spaces_url
    req=cc.request(name_url)
    name_list=cc.get_all_resources(req)
    return name_list

def get_devuser_details(name_type,name):
    req=cc.request(name_type).set_query(q='name:'+ name)
    res=req.get()
    #print(str(res.response.status_code) + ' ' + res.response.reason)
    if res.has_error:
        print(str(res.error_code) + ': '+ str(res.error_messae))
        sys.exit(1)
    name_url=res.resource.developers_url
    req=cc.request(name_url)
    name_list=cc.get_all_resources(req)
    return name_list

def get_manageruser_details(name_type,name):
    req=cc.request(name_type).set_query(q='name:'+ name)
    res=req.get()
    #print(str(res.response.status_code) + ' ' + res.response.reason)
    if res.has_error:
        print(str(res.error_code) + ': '+ str(res.error_messae))
        sys.exit(1)
    name_url=res.resource.managers_url
    req=cc.request(name_url)
    name_list=cc.get_all_resources(req)
    return name_list

def get_auditoruser_details(name_type,name):
    req=cc.request(name_type).set_query(q='name:'+ name)
    res=req.get()
    #print(str(res.response.status_code) + ' ' + res.response.reason)
    if res.has_error:
        print(str(res.error_code) + ': '+ str(res.error_messae))
        sys.exit(1)
    name_url=res.resource.auditors_url
    req=cc.request(name_url)
    name_list=cc.get_all_resources(req)
    return name_list

def get_orgmanager_details(name_type,name):
    req=cc.request(name_type).set_query(q='name:'+ name)
    res=req.get()
    #print(str(res.response.status_code) + ' ' + res.response.reason)
    if res.has_error:
        print(str(res.error_code) + ': '+ str(res.error_messae))
        sys.exit(1)
    name_url=res.resource.managers_url
    req=cc.request(name_url)
    name_list=cc.get_all_resources(req)
    return name_list

def get_orgauditors_details(name_type,name):
    req=cc.request(name_type).set_query(q='name:'+ name)
    res=req.get()
    #print(str(res.response.status_code) + ' ' + res.response.reason)
    if res.has_error:
        print(str(res.error_code) + ': '+ str(res.error_messae))
        sys.exit(1)
    name_url=res.resource.auditors_url
    req=cc.request(name_url)
    name_list=cc.get_all_resources(req)
    return name_list


if __name__ == "__main__":

    cf_api_list=[''] ### You will provide the list of api's of entire cloud foundry we use

    for api in cf_api_list:
        cloud_controller = api
        org_list=[]
        space_dict={}
        org_user_dict={}
        space_users_dict={}
        d_users=str(sys.argv[2])
        d_user_list=d_users.split(",")
        cc = cf_api.new_cloud_controller(
            cloud_controller,
            client_id='cf',
            client_secret='',
            username='username',
            password=str(sys.argv[1]),
        )
        org_req = cc.organizations()
        org_res = org_req.get()
        orgs = org_res.resources
        for r in orgs:
            org_list.append(str(r.name))
        for org in org_list:
            all_spaces_list=get_space_details('organizations',org)
            all_orgmanager_list=get_orgmanager_details('organizations',org)
            all_orgauditors_list=get_orgauditors_details('organizations',org)

        for manager in all_orgmanager_list:
            if d_user == str(manager.username):
                print(str(manager.username),"OrgManager",d_user,org)
        for auditor in all_orgauditors_list:
            if d_user == str(auditor.username):
                print(str(auditor.username),"OrgAuditor",d_user,org)

            for space in all_spaces_list:
                space_dev_users=get_devuser_details('spaces',str(space.name))
                space_manager_users=get_manageruser_details('spaces',str(space.name))
                space_auditor_users=get_auditoruser_details('spaces',str(space.name))
                print(space_dev_users)
                for developer in space_dev_users:
                    for d_user in d_user_list:
                        if d_user == str(developer.username):
                            print(str(space.name),"SpaceDeveloper",d_user,org)
                            args=["cf","unset-space-role",d_user,org,str(space.name),"SpaceDeveloper"]
                            cf_user_del = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            out,err = cf_user_del.communicate()
                            print(out,err)
                            print("cf unset-space-role "+d_user+" "+org+" "+str(space.name)+" SpaceDeveloper")
                for manager in space_manager_users:
                    for d_user in d_user_list:
                        if d_user == str(manager.username):
                            print(str(space.name),"SpaceManager",d_user,org)
                            args=["cf","unset-space-role",d_user,org,str(space.name),"SpaceManager"]
                            cf_user_del = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            out,err = cf_user_del.communicate()
                            print(out,err)
                            print("cf unset-space-role "+d_user+" "+org+" "+str(space.name)+" SpaceManager")

                for auditor in space_auditor_users:
                    for d_user in d_user_list:
                        if d_user == str(auditor.username):
                            print(str(space.name),"SpaceAuditor",d_user,org)
                            args=["cf","unset-space-role",d_user,org,str(space.name),"SpaceAuditor"]
                            cf_user_del = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            out,err = cf_user_del.communicate()
                            print(out,err)
                            print("cf unset-space-role "+d_user+" "+org+" "+str(space.name)+" SpaceAuditor")