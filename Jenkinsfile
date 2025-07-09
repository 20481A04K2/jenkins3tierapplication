pipeline {
  agent any

  environment {
    PROJECT_ID = 'your-gcp-project-id'      // 🔁 Change this
    IMAGE_NAME = 'flask-app'
    REGION = 'us-central1'
    SONAR_SCANNER_HOME = '/opt/sonar-scanner'
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
        sh """
          docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME .
        """
      }
    }

    stage('Authenticate & Push to Artifact Registry') {
      steps {
        sh """
          gcloud config set project $PROJECT_ID
          gcloud auth configure-docker --quiet
          docker push gcr.io/$PROJECT_ID/$IMAGE_NAME
        """
      }
    }

    stage('Deploy to Cloud Run') {
      steps {
        sh """
          gcloud run deploy $IMAGE_NAME \
            --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
            --platform=managed \
            --region=$REGION \
            --allow-unauthenticated \
            --set-env-vars DB_USER=root,DB_PASS=password,DB_HOST=xxx.xxx.xxx.xxx,DB_NAME=mydb
        """
      }
    }
  }
}
