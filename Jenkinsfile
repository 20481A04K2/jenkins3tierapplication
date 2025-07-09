pipeline {
  agent any

  environment {
    PROJECT_ID = 'sylvan-hydra-464904-d9'
    REGION = 'us-central1'
    REPOSITORY = 'flask-app-repo'
    IMAGE_NAME = 'flask-app'
    IMAGE_TAG = 'latest'
    AR_URL = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"
    SONAR_SCANNER_HOME = tool 'Default Sonar Scanner'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
          withSonarQubeEnv('My SonarQube Server') {
            sh """
              ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                -Dsonar.projectKey=$IMAGE_NAME \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://34.63.76.155:9000 \
                -Dsonar.login=$SONAR_TOKEN
            """
          }
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t $AR_URL ."
      }
    }

    stage('Push to Artifact Registry') {
      steps {
        sh """
          gcloud config set project $PROJECT_ID
          gcloud auth configure-docker $REGION-docker.pkg.dev --quiet
          docker push $AR_URL
        """
      }
    }

    stage('Deploy to Cloud Run') {
      steps {
        sh """
          gcloud run deploy $IMAGE_NAME \
            --image $AR_URL \
            --platform=managed \
            --region=$REGION \
            --allow-unauthenticated
        """
      }
    }
  }
}
