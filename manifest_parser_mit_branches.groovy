#!/usr/bin/env groovy
def environmentNameList = ['',''] /// Environment list
def envChoices = environmentNameList.join("\n")
def kafkaClusterChoices = kafkaClusterList.join("\n")

properties([buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '5')), [$class: 'JobRestrictionProperty'],
	parameters([
			choice(choices: envChoices, description: 'Environment', name: 'deploymentEnvironment'),
			string(defaultValue: 'null', description: 'Github Org where you want to make changes', name: 'githubOrg'),
			string(defaultValue: 'null', description: 'Release Manifest that needs to be validated', name: 'releaseManifest'),
		])])

def releaseManifestFileName = releaseManifest.trim()
List release_branches = []
node('master')
{
	timestamps
	{
		stage('Prepare') 
		{
		sh "rm -rf *" /// Clearing checkout
                        checkout([$class           : 'GitSCM',
                                  branches         : [[name: "master"]],
                                  extensions       : [[$class: 'WipeWorkspace']], /// this also wipes out the spaces
                                  userRemoteConfigs: [[url: 'git@github.com:username/repo']]
                        ])
						echo("######################################################################")
                        echo("deploymentEnvironment: ${deploymentEnvironment}")
						echo("githubOrg: ${githubOrg}")
						echo("Manifest: ${releaseManifestFileName}")
						echo("######################################################################")
		}

		stage('Finding the branch name')
		{
            def releaseManifestFile = "release-"+releaseManifestFileName+".json"
			if(fileExists(releaseManifestFile))
			{
				def releaseFile = readFile(releaseManifestFile)
				releaseInfo = jsonParse(releaseFile)
				if(releaseInfo['microservices']!=null)
				{
					def keys=jsonParse(releaseFile)['microservices'].keySet()
					echo("######################################################################")
					// echo("Release Info is: ${releaseInfo}")
					echo("Microservices : ${keys}")
					for (i = 0; i < keys.size(); i++)
					{
						if(keys[i].trim() != null)
						{
							service_key = keys[i].trim()
							echo("Each Microservice : ${service_key}")
							// def value = releaseInfo['microservices'][service_key] //This also gets the key value
							// echo("Value of ${service_key} is ${value}")
							def content = jsonParse(releaseFile)['microservices'].get(service_key)
							echo("Value of ${service_key} is ${content}")
							def app_name = content.find{ it.key == "app_name" }?.value
							def app_version = content.find{ it.key == "app_version" }?.value
							def app_prefix = content.find{ it.key == "app_prefix" }?.value
							if(app_name != null || app_version != null || app_prefix != null)
							{
								def branch_name = app_prefix + "-" +app_name + "-" + app_version
								echo(" Branch name is ${branch_name}")
								release_branches.add(branch_name)
							}
							else
							{
								echo(" App_version : ${app_version} - App_name : ${app_name} - App_prefix : ${app_prefix} has invalid value")
								error "Please provide proper application variables"
							}
						}
					}
				}
				echo("Release branches are ${release_branches}")
			}
			else
			{
				error "Manifest file not found"
			}
		}
		stage('Checkout another github repo')
		{
			dir("Andere Repo")
				{
					checkout([$class           : 'GitSCM',
                              branches         : [[name: "master"]],
                              extensions       : [[$class: 'WipeWorkspace']],
                              userRemoteConfigs: [[url: 'git@github.com:username/repo']]
                    ])
					echo("Checkout another repo completed")
					for(i = 0; i < release_branches.size(); i++)
					{
						def branch_name = release_branches[i]
						echo("Current branch name is ${branch_name}")
						sh """
							pwd
							git checkout ${branch_name}
						"""
					}
				}
		}
	}
}

@NonCPS
def jsonParse(def json) 
{
    new groovy.json.JsonSlurperClassic().parseText(json)
}
