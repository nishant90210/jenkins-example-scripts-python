pipeline {
  agent any
  parameters {
    string defaultValue: 'qa', description: 'environment to Run', name: 'env', trim: true
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
    stage('print') {
      steps {
        sh 'python3 new_script.py' + params.env
      }
    }
  }
}