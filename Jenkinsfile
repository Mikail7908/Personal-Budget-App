pipeline {
    agent any

    environment {
        // Define environment variables here if needed
        BACKEND_DIR = "backend"
        FRONTEND_DIR = "frontend"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the repository
                checkout scm
            }
        }

        stage('Backend Build and Test') {
            steps {
                dir("${BACKEND_DIR}") {
                    // Install dependencies
                    sh 'pip install -r requirements.txt'

                    // Run backend tests
                    sh 'pytest'
                }
            }
        }

        stage('Frontend Build and Test') {
            steps {
                dir("${FRONTEND_DIR}") {
                    // Install dependencies
                    sh 'npm install'

                    // Build the frontend
                    sh 'npm run build'

                    // Run frontend tests
                    sh 'npm test'
                }
            }
        }

        stage('Deploy') {
            steps {
                // Add deployment steps here
                echo "Deploying application..."
                // Example: sh './deploy.sh'
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
        success {
            echo 'Pipeline has successfully completed!'
        }
        failure {
            echo 'Pipeline has failed!'
        }
    }
}
