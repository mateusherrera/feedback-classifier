pipeline {
  agent any

  environment {
    REPO_OWNER = 'mateusherrera'
    REPO_NAME  = 'feedback-classifier'
    BRANCH     = 'main'
  }

  stages {
    stage('Disparar GitHub Actions') {
      steps {
        echo "Disparando GitHub Actions para ${env.REPO_OWNER}/${env.REPO_NAME}"
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            curl -X POST \
              -H "Authorization: token $GITHUB_TOKEN" \
              -H "Accept: application/vnd.github.v3+json" \
              https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/dispatches \
              -d '{"event_type":"ci-pipeline"}'
          '''
        }
      }
    }

    stage('Aguardar Resultado') {
      steps {
        script {
          echo "Aguardando resultado do workflow 'CI - Pytest' na branch '${env.BRANCH}'..."
          withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
            def timeoutMin = 5
            def pollInterval = 10
            def waited = 0
            def runId = null
            def status = 'in_progress'

            while (status == 'in_progress' && waited < timeoutMin * 60) {
              sleep time: pollInterval, unit: 'SECONDS'
              waited += pollInterval

              def json = sh(
                script: """
                  curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                    https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs?branch=$BRANCH \\
                    | jq -r '.workflow_runs[] | select(.name=="CI - Pytest") | .id, .status, .conclusion' | head -n3
                """,
                returnStdout: true
              ).trim().split('\n')

              if (json.size() >= 3) {
                runId   = json[0]
                status  = json[1]
                result  = json[2]
              }

              echo "Status: ${status} | Resultado parcial: ${result}"
            }

            if (status != 'completed') {
              error "Tempo limite atingido aguardando o GitHub Actions"
            }

            if (result != 'success') {
              error "Workflow falhou: ${result}"
            }

            echo "Workflow finalizado com sucesso!"
          }
        }
      }
    }
  }
}
