import java.text.SimpleDateFormat

def createFilePath(path) {
    if (env['NODE_NAME'] == null) {
        error "envvar NODE_NAME is not set, probably not inside an node {} or running an older version of Jenkins!";
    } else if (env['NODE_NAME'].equals("built-in")) {
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
                        def filePath = new hudson.FilePath(env.WORKSPACE + '/fileparam/' + fileItem.getName())
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

pipeline {
  agent any
  parameters {
    file(name: 'inputFile', description: 'Input file in format: artifactId/version/timestamp')
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
            }
        }
    }
    // stage('Build') {
    //   steps {
    //     sh 'python3 new_script.py'
    //   }
    // }
  }
}