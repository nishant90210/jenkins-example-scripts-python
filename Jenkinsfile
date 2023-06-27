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
    stages {
       stage('File path') {
            steps {
                echo "${env.WORKSPACE}"
            }
        }
    }
    stage('print') {
      steps {
        sh 'python3 new_script.py'
      }
    }
  }
}