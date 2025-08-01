pipeline {
  agent any

  environment {
    GITHUB_TOKEN  = credentials('github-token')
    REPO_OWNER    = 'mateusherrera'
    REPO_NAME     = 'flask-llm-api'
  }

  stages {
    stage('Trigger GitHub Actions CI') {
      steps {
        echo "Disparando CI para ${env.REPO_OWNER}/${env.REPO_NAME}"
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            set -xe
            curl -X POST \
              -H "Authorization: token $GITHUB_TOKEN" \
              -H "Accept: application/vnd.github.v3+json" \
              https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/dispatches \
              -d '{"event_type":"ci-pipeline"}'
          '''
        }
      }
    }
  }
}
