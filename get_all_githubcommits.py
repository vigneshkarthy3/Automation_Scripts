import requests,os,json
import sqlite3
from sqlite3 import Error

# Response function
def getUrlResponse(url,userName,tokenId):
    formatData=requests.get(url,auth=(userName,tokenId)).json()

    return formatData

# Fetching all commits from the repo and inserting into sqlite db
def migrateGithubAllCommitsUntilDate(commitUrl,branchName,count,startDate,userName,tokenId,result,conn):
    while result != []:
        count=count+1
        result=getUrlResponse(commitUrl+"?/sha="+branchName+"&page="+str(count)+"&since="+startDate,userName,tokenId)
        if result != []:
            for i in range(0,len(result)):
                tempSha=result[i]["sha"]
                print("sha:"+tempSha)
                tempDate=result[i]["commit"]["author"]["date"]
                print("date:"+tempDate)
                try:
                    tempAuthor=result[i]["author"]["login"]
                    print("author:"+tempAuthor)
                except (TypeError,KeyError):
                    tempAuthor=""
                    print("author:"+tempAuthor)
                tempMessage=result[i]["commit"]["message"]
                print("commit message:"+tempMessage)
                # if tempAuthor in bsEmployeeList:
                #     tempIsExternal=0
                #     # print("is_external:"+str(tempIsExternal))
                # else:
                #     tempIsExternal=1
                #     # print("is_external:"+str(tempIsExternal))
                sql='''INSERT INTO commits(sha,date,author,message) VALUES (?,?,?,?)'''
                allCommits=(tempSha,tempDate,tempAuthor,tempMessage)
                conn.cursor().execute(sql,allCommits)
                conn.commit()
    


if __name__ == "__main__":

    # Variables

    userName="vigneshkarthy3"
    tokenId="" # I have provided my token id empty for security reasons mentioned in our requirement, it's your github access token.
    GithubUrl="https://api.github.com/repos/vigneshkarthy3/Exp_Docker"
    shaId="{/sha}"
    brValue="{/branch}"
    startDate="2020-08-08T00:00:00Z"
    count=0
    result=None
    bsEmployeeList=[]
    branchList=[]
    dbFile="github.db"

    # Saving the employeeList in bsEmployeeList
    #with open('assets/members.json') as internalFile:
    #    internalData = json.load(internalFile)
    #for i in range(0,len(internalData)):
    #    bsEmployeeList.append(internalData[i]["login"])

    # Resource data passed inside resourceData
    resourceData=getUrlResponse(GithubUrl,userName,tokenId)
    commitUrl,branchesUrl=resourceData["commits_url"],resourceData["branches_url"]

    # To remove the extra words of shaId from the resource value
    branchesUrl,commitUrl=branchesUrl[:-len(brValue)],commitUrl[:-len(shaId)]

    # Creating the database connection
    conn = sqlite3.connect(dbFile)
    conn.cursor().execute('''CREATE TABLE allcommits (sha TEXT, date TEXT, author TEXT, message TEXT)''')

    # To get all the branchNames
    branchData=getUrlResponse(branchesUrl,userName,tokenId)
    for i in range(0,len(branchData)):
        branchList.append(branchData[i]["name"])
    # print(branchList)
    for branch in branchList:
        print(branch)
        migrateGithubAllCommitsUntilDate(commitUrl,branch,count,startDate,userName,tokenId,result,conn)

    print("Successfully migrated all the commits as per the requirement to sqlite db")
