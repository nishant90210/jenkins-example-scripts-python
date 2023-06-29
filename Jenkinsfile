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
                        def filePath = new hudson.FilePath(null, env.WORKSPACE + '/file/' + fileItem.getName())
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
    file(name: 'Input CSV File', description: 'Membership Ids file')
    choice(choices: ['qa','prod'], description: 'Environment', name: 'env')
  }
  stages {
    stage('Launch file uploader') {
        steps {
            echo "Running image pipelines-cs-file-uploader"
            script {
                def filename = getFileParamFromWorkspace('inputFile')
            }
        }
    }
    stage('Build') {
      steps {
        sh 'python3 new_script.py'
      }
    }
  }
}