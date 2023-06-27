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
    stage('print') {
      steps {
        sh 'python3 new_script.py'
      }
    }
  }
}