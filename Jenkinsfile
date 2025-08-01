pipeline {
  agent any

  environment {
    GITHUB_TOKEN = credentials('github-token')
    REPO_OWNER    = 'mateusherrera'
    REPO_NAME     = 'flask-llm-api'
  }

  stages {
    stage('Trigger GitHub Actions CI') {
      steps {
        echo "Disparando CI para ${env.REPO_OWNER}/${env.REPO_NAME}"
        sh """
          set -xe
          curl -X POST \
            -H \"Authorization: token ${env.GITHUB_TOKEN}\" \
            -H \"Accept: application/vnd.github.v3+json\" \
            https://api.github.com/repos/${env.REPO_OWNER}/${env.REPO_NAME}/dispatches \
            -d \"{\"event_type\":\"ci-pipeline\"}\"
        """
      }
    }
  }
}
