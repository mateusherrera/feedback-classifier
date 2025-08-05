pipeline {
  agent any

  environment {
    REPO_OWNER = 'mateusherrera'
    REPO_NAME  = 'feedback-classifier'
    BRANCH     = 'main'
    WORKFLOW_NAME = 'CI - Pytest'
  }

  stages {
    stage('Disparar GitHub Actions') {
      steps {
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

    stage('Aguardar Resultado do GitHub Actions') {
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          script {
            echo "Aguardando resultado do workflow '$WORKFLOW_NAME' na branch '$BRANCH'..."

            def workflowRunId = ''
            def conclusion = ''
            def status = ''
            def maxRetries = 30
            def retryCount = 0

            while (retryCount < maxRetries) {
              def output = sh(
                script: '''
                  curl -s -H "Authorization: token $GITHUB_TOKEN" \
                    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs?branch=$BRANCH" \
                    | jq -r '.workflow_runs[] | select(.name=="'"$WORKFLOW_NAME"'") | [.id, .status, .conclusion] | @tsv' \
                    | head -n 1
                ''',
                returnStdout: true
              ).trim()

              if (output) {
                def parts = output.split('\t')
                if (parts.length == 3) {
                  workflowRunId = parts[0]
                  status = parts[1]
                  conclusion = parts[2]

                  echo "Status: $status | Conclusão: $conclusion"

                  if (status == 'completed') {
                    break
                  }
                }
              }

              sleep(time: 10, unit: 'SECONDS')
              retryCount++
            }

            if (conclusion == 'success') {
              echo "GitHub Actions finalizou com sucesso."
            } else {
              error("GitHub Actions falhou ou foi cancelado. Conclusão: ${conclusion}")
            }
          }
        }
      }
    }
  }
}
