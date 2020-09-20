import os
import json
import sys,re
import subprocess
import glob
import itertools
from operator import itemgetter
from packaging import version

###########     Function to validate the json file format

def validate_json(release):
    global read_json_files
    global invalid_json_files
    global error_message
    global app_json_files
    error_message = []
    read_json_files = []
    invalid_json_files = []
    app_json_files = []
    files = glob.glob(pattern)
    files.sort(key=os.path.getmtime)
    for file in files:
        with open(file) as json_file:
            try:
                json.load(json_file)
                read_json_files.append(file)
            except ValueError as e:
                invalid_json_files.append(file)
                error_message.append(e)
    read_json_files=[i for i in read_json_files if not ('merge'.lower() in i.lower())]
    
    if app_type.lower() == "sometype":
        read_json_files=[i for i in read_json_files if not ('demo' in i.lower() or 'pre' in i.lower() or 'restart' in i.lower() or 'roll' in i.lower() or 'sync' in i.lower())]
    else:
        read_json_files=[i for i in read_json_files if (app_type.lower() in i.lower())]
    for i in exception_files_list:
        for j in read_json_files:
            if str(i) in str(j):
                read_json_files.remove(str(j))

    read_json_files.sort(key=version.parse)
    if invalid_json_files == []:
        return True
    else:
        return False

###########     Function to merge the json files

def merged_service_dict(main_service,exclusion,dict_file):
        for file in read_json_files:
            try:
                f= open(file,"r")
                data=json.loads(f.read(),encoding='utf-8')
                for each in data[main_service]:
                    if str(each) != '' and str(each) != exclusion:
                        service=data[main_service][each]
                        version=str(service["app_version"])
                        dict_file[str(each)]=eval(json.dumps(service))
                    else:
                        print(file,"- Invalid/Null value in file")
            except KeyError as e:
                print(e,"Invalid/Null value in file ",file)
        return dict_file


if __name__ == "__main__":

#### Variables
    try:
        release=str(sys.argv[1])
        app_type=str(sys.argv[2])
        exception_files=str(sys.argv[3])
        exception_files_list=exception_files.split(",")
    except IndexError as e:
        exception_files=''
        exception_files_list=''
    pattern="*-R"+release+"*.json"
    clone_url=""
    result_file="release-"+release+"x-"+app_type+"-MERGED.json"
    main_dict={}
    ms_dict={}
    nms_dict={}
    count=0



###########     Main function

    if validate_json(release) == True:
        print("The manifest files used are "+', '.join(read_json_files))
        if read_json_files == []:
            print("ERROR: "+app_type+" did not match with the release version "+release)
        merged_service_dict("microservices","non_microservices",ms_dict)
        merged_service_dict("non_microservices","microservices",nms_dict)

        main_dict["comments"]=', '.join(read_json_files)
        main_dict["microservices"]=ms_dict
        main_dict["non_microservices"]=nms_dict

###########    Saving the json file after filtering the invalid files in main_dict

        with open(result_file,'w') as fp:
                json.dump(main_dict,fp,sort_keys=True,indent=4)

    else:
        for e,filename in zip(error_message,invalid_json_files):
          print("Error ==> ", e)
          print("File name ==> ", filename)
        print("Please commit the file with proper JSON format")


