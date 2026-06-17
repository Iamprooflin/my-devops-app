pipeline {
    agent any  // kisi bhi available Jenkins machine pe chalo

    environment {
        // Yeh variables pure pipeline mein use honge
        ECR_REPO = "407291110113.dkr.ecr.us-east-1.amazonaws.com/my-devops-app"
        AWS_REGION = "us-east-1"
        IMAGE_TAG = "v${BUILD_NUMBER}"  // har build ka alag tag (v1, v2, v3...)
    }

    stages {

        stage('Checkout Code') {
            steps {
                // GitHub se latest code utha lo
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                // Dockerfile use karke image banao
                bat "docker build -t myapp:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                // AWS credentials use karke ECR mein login + push
                withCredentials([usernamePassword(
                    credentialsId: 'aws-ecr-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    bat """
                        aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %ECR_REPO%
                        docker tag myapp:%IMAGE_TAG% %ECR_REPO%:%IMAGE_TAG%
                        docker push %ECR_REPO%:%IMAGE_TAG%
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