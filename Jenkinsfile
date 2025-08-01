pipeline {
  agent any

  environment {
    GITHUB_TOKEN = credentials('github-token')
  }

  stages {
    stage('Load .env') {
      steps {
        script {
          def props = readProperties file: '.env'
          env.REPO_OWNER = props['REPO_OWNER']
          env.REPO_NAME  = props['REPO_NAME']
          echo "Variáveis carregadas: REPO_OWNER=${env.REPO_OWNER}, REPO_NAME=${env.REPO_NAME}"
        }
      }
    }

    stage('Trigger GitHub Actions CI') {
      steps {
        echo "Disparando CI no GitHub Actions para ${env.REPO_OWNER}/${env.REPO_NAME}"
        sh '''
          curl -X POST \
            -H "Authorization: token ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/${env.REPO_OWNER}/${env.REPO_NAME}/dispatches \
            -d '{"event_type":"ci-pipeline"}'
        '''
      }
    }
  }
}
