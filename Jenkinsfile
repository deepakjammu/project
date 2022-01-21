pipeline {
    agent {
        environment {
            registry = "392085940295.dkr.ecr.us-east-1.amazonaws.com/training"
        }
    }
    stages {
        stage ('SCM') {
            steps {
                sh 'https://github.com/deepakjammu/project.git'
            }
        }
        stage ('docker build') {
            steps {
                sh 'docker build -t . nginx'
            }
        }
        stage ('docker run') {
            steps {
                sh 'docker run -d -p 8000:80 nginx'
            }
        }    
        stage ('docker push') {
            steps {
                sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 392085940295.dkr.ecr.us-east-1.amazonaws.com'
                sh 'docker push 392085940295.dkr.ecr.us-east-1.amazonaws.com/training:latest'
            }
        }
        
    }
}
