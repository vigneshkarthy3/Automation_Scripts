#!/usr/bin/env groovy

node('')
        {
            stage('checkout')
                    {
                        checkout([$class: 'GitSCM',
	                branches: [[name: "master"]],
    	                extensions: [[$class: 'WipeWorkspace']],
    	                userRemoteConfigs: [[url: 'git@github.com:vigneshkarthy3/scripts.git']]
				])
                    }
                                  
            stage('Script execution')
                    {
                        def version = "${release_version}"
                        def app_type = "${application_type}"
			def exclusion = "${exclusion_files}"
                        def release_version_final = input message: "Confirmation value  ${release_version}? ", ok: 'Yes', parameters: [string(defaultValue: '', description: '', name: 'Confirm release version')]
                        if (release_version_final != release_version) {
                            error 'The values do not match, provide crct value'
                        } else {
                            echo "confirmed : ${release_version}"
                        }


                        def errorCheck = sh(script: """python manifest_merger.py ${version} ${app_type} ${exclusion}| wc -l """, returnStdout: true).trim()
                        echo "${errorCheck}"
                        int errorCheckValue = (errorCheck) as Integer
                        if (errorCheckValue == 1) {
                            sh """ python manifest_merger.py ${version} ${app_type} ${exclusion}"""
                            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId:'slkjfalkjslkjkljkljlkjlk', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']	
                            ]){	
                                sh "git checkout master"
				                sh "git remote -v"
                                sh "git commit -m 'merging final release file under ${release_version}-${app_type}' || echo 'Seems, the file has no changes'"	/// To verify allow duplicate copies
                                sh "git push origin master"	
                            }
                        }
                        else {
                            sh """ python manifest_merger.py ${version} ${app_type} ${exclusion}"""
                            error "Resolve the above errors to get the merged json file"
                        }
                    }
        }
