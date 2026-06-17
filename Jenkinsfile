pipeline {
    agent any

    environment {
        ECR_REPO = "407291110113.dkr.ecr.us-east-1.amazonaws.com/my-devops-app"
        AWS_REGION = "us-east-1"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                // bat ki jagah sh use kiya - kyunki Jenkins Linux container mein hai
                sh "docker build -t myapp:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-ecr-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                        docker tag myapp:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG}
                        docker push ${ECR_REPO}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline complete! Image pushed: ${ECR_REPO}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed — check logs above"
        }
    }
}