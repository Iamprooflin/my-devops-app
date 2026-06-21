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

        stage('Update Helm Chart') {
            steps {
                // values.yaml ke andar purana tag dhundo aur naye se replace karo
                sh "sed -i 's|tag:.*|tag: \"${IMAGE_TAG}\"|' myapp-chart/values.yaml"

                withCredentials([usernamePassword(
                    credentialsId: 'github-credentials',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh """
                        git config user.email "jenkins@local.com"
                        git config user.name "Jenkins"
                        git add myapp-chart/values.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}"
                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/Iamprooflin/my-devops-app.git HEAD:main
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline complete! New tag: ${IMAGE_TAG} — ArgoCD will auto-deploy"
        }
        failure {
            echo "Pipeline failed — check logs above"
        }
    }
}