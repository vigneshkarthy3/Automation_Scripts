import os
import yaml,glob
os.chdir(r'testing')
resultdir="result"
files = glob.glob("*.yaml")
for file in files:
    resultfile=resultdir+"\\"+file
    new_dict={}
    with open(file) as f:
        docs=yaml.load(f, Loader=yaml.FullLoader)
    for each in docs["applications"]:
        try:
            new_dict["appname"]=each["name"]
            new_dict["memory"]=each["memory"]
            new_dict["instance"]=each["instances"]
        except KeyError:
            print("Key-error ",file)
    with open(resultfile,'w') as newfile:
        data = yaml.dump(new_dict, newfile,default_flow_style=False, sort_keys=False)