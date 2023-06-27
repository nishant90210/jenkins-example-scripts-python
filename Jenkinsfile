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
    stage('Install Dependencies Numpy') {
      steps {
        sh 'pip3 install numpy'
      }
    }
    stage('print') {
      steps {
        sh 'python3 new_script.py'
      }
    }
  }
}