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
    stage('print') {
      steps {
        sh 'python3 new_script.py'
      }
    }
  }
}