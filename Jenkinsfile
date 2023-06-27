pipeline {
  agent any
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
    parameters {
    base64File 'yamlFile'
    }
    stages {
      stage('Example') {
        steps {
          withFileParameter('yamlFile') {
            def configVal = readYaml file: yamlFile
          }
        }
      }
    }
    // stage('print') {
    //   steps {
    //     sh 'python3 new_script.py'
    //   }
    // }
  }
}