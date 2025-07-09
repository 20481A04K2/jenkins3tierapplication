pipeline {
  agent any

  environment {
    // GCP configuration
    PROJECT_ID = 'sylvan-hydra-464904-d9'
    REGION = 'us-central1'
    REPOSITORY = 'flask-app-repo'
    IMAGE_NAME = 'flask-app'
    IMAGE_TAG = 'latest'
    AR_URL = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"

    // SonarQube configuration (Jenkins "Tools" config name)
    SONAR_SCANNER_HOME = tool 'Default Sonar Scanner'
  }

  stages {
    stage('Checkout') {
      steps {
        echo '🔁 Checking out source code...'
        checkout scm
      }
    }

    stage('SonarQube Analysis') {
      steps {
        echo '🔍 Running SonarQube static code analysis...'
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

    stage('Quality Gate Check') {
      steps {
        echo '🚦 Waiting for SonarQube quality gate result...'
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        echo '🐳 Building Docker image...'
        sh "docker build -t $AR_URL ."
      }
    }

    stage('Push to Artifact Registry') {
      steps {
        echo '📦 Pushing image to Artifact Registry...'
        sh """
          gcloud config set project $PROJECT_ID
          gcloud auth configure-docker $REGION-docker.pkg.dev --quiet
          docker push $AR_URL
        """
      }
    }

    stage('Deploy to Cloud Run') {
      steps {
        echo '🚀 Deploying to Cloud Run...'
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

  post {
    success {
      echo '✅ Deployment completed successfully!'
    }
    failure {
      echo '❌ Build failed. Check logs above for more details.'
    }
  }
}
