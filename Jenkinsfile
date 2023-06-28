@Library('deploy-pipeline-shared-libraries')_
import java.text.SimpleDateFormat
pipeline {
  agent any
  parameters {
    choice(choices: ['qa','prod'], description: 'Environment', name: 'env')
  }
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('pip version') {
      steps {
        sh 'pip3 --version'
      }
    }
    stage('File path') {
        steps {
            echo "${env.WORKSPACE}"
        }
    }
    stage('print env') {
      steps {
        echo "${params.env}"
      }
    }
    stage('Launch file uploader') {
        steps {
            echo "Running image pipelines-cs-file-uploader"
            script {
                def filename = getFileParamFromWorkspace('inputFile')
                def timestamp= System.currentTimeMillis()
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd-HH:mm:ss:SSS")
                String formattedTimestamp = sdf.format(timestamp)
                echo "your file will be stored in /${artifactId}/${version}/${formattedTimestamp}/data-${userId}.csv"
                echo "to use as input file: ${artifactId}/${version}/${formattedTimestamp}"


                if ("${environment}" == "test") {
                    image = "eu.gcr.io/edo-test-resources/pipelines-cs-input-uploader:1.2.2-qa"
                } else if ("${environment}" == "prod") {
                    image = "eu.gcr.io/edo-prod-resources/pipelines-cs-input-uploader:1.2.2-prod"
                }
                setServiceAccountFile("edo-${environment}-gcp")
                sh "rm -f /home/centos/.docker/config.json"
                sh "docker login -u _json_key --password-stdin https://eu.gcr.io < ${WORKSPACE}/.config/google-cloud/service_account.json"
                sh "docker run -v ${WORKSPACE}/${filename}:/opt/input.csv  -e ARTIFACT_ID=${artifactId} -e TIMESTAMP=${timestamp} -e VERSION=${version} -e USER_NAME=${userId} -e ENVIRONMENT=${environment} ${image}"
            }
        }
    }
    def createFilePath(path) {
        if (env['NODE_NAME'] == null) {
            error "envvar NODE_NAME is not set, probably not inside an node {} or running an older version of Jenkins!";
        } else if (env['NODE_NAME'].equals("master")) {
            return new hudson.FilePath(null, path)
        } else {
            return new hudson.FilePath(jenkins.model.Jenkins.instance.getComputer(env['NODE_NAME']).getChannel(), path)
        }
    }

    def getFileParamFromWorkspace(fileParamName) {
        def paramsAction = currentBuild.rawBuild.getAction(ParametersAction.class);
        if (paramsAction != null) {
            for (param in paramsAction.getParameters()) {
                if (param instanceof FileParameterValue) {
                    def fileParameterValue = (FileParameterValue)param
                    if (fileParamName.equals(fileParameterValue.getName())) {
                        def fileItem = fileParameterValue.getFile()
                        if (fileItem instanceof org.apache.commons.fileupload.disk.DiskFileItem) {
                            def diskFileItem = (org.apache.commons.fileupload.disk.DiskFileItem)fileParameterValue.getFile()
                            def filePath = createFilePath(env.WORKSPACE + '/fileparam/' + fileItem.getName())
                            def destFolder = filePath.getParent()
                            destFolder.mkdirs()
                            filePath.copyFrom(diskFileItem)
                            return 'fileparam/' + fileItem.getName()
                        }
                    }
                }
            }
        }
        return ''
    }
    stage('print') {
      steps {
        sh 'python3 new_script.py'
      }
    }
  }
}