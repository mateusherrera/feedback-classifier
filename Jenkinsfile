pipeline {
  agent any

  environment {
    REPO_OWNER     = 'mateusherrera'
    REPO_NAME      = 'feedback-classifier'
    BRANCH         = 'main'
    WORKFLOW_NAME  = 'CI - Pytest'

    // carrega o token como variável de ambiente em todo o pipeline
    GITHUB_TOKEN   = credentials('github-token')
  }

  stages {
    stage('1. Obter workflow ID') {
      steps {
        script {
          env.WORKFLOW_ID = sh(
            script: '''
              curl -s -H "Authorization: token $GITHUB_TOKEN" \
                   -H "Accept: application/vnd.github.v3+json" \
                   https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows \
                | jq -r '.workflows[] | select(.name=="'"$WORKFLOW_NAME"'") | .id'
            ''',
            returnStdout: true
          ).trim()
          echo "Workflow ID = $WORKFLOW_ID"
        }
      }
    }

    stage('2. Capture último run antes do dispatch') {
      steps {
        script {
          env.LAST_RUN_ID = sh(
            script: '''
              curl -s -H "Authorization: token $GITHUB_TOKEN" \
                   "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/$WORKFLOW_ID/runs?branch=$BRANCH&per_page=1" \
                | jq -r '.workflow_runs[0].id'
            ''',
            returnStdout: true
          ).trim()
          echo "Último run antes do dispatch = $LAST_RUN_ID"
        }
      }
    }

    stage('3. Disparar GitHub Actions') {
      steps {
        sh '''
          curl -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/$WORKFLOW_ID/dispatches \
            -d '{"ref":"'"$BRANCH"'"}'
        '''
      }
    }

    stage('4. Aguardar o novo run completar') {
      steps {
        script {
          def maxRetries = 30
          def retryCount = 0
          def newRunId = ''
          def status   = ''
          def conclusion = ''

          echo "Aguardando o run novo do workflow '${WORKFLOW_NAME}'..."

          while (retryCount < maxRetries) {
            // busca o run mais recente
            def output = sh(
              script: """
                curl -s -H "Authorization: token \$GITHUB_TOKEN" \
                  "https://api.github.com/repos/\$REPO_OWNER/\$REPO_NAME/actions/workflows/\$WORKFLOW_ID/runs?branch=\$BRANCH&per_page=1" \
                  | jq -r '.workflow_runs[0] | [.id, .status, .conclusion] | @tsv'
              """,
              returnStdout: true
            ).trim()

            if (output) {
              def parts = output.split('\\t')
              newRunId   = parts[0]
              status     = parts[1]
              conclusion = parts[2] ?: ''

              // só passa adiante quando for o run disparado agora
              if (newRunId != $LAST_RUN_ID) {
                echo "Found run ${newRunId}: status=${status}, conclusion=${conclusion}"
                if (status == 'completed') {
                  break
                }
              } else {
                echo "Run ainda não mudou (continua ${newRunId}), aguardando..."
              }
            }

            sleep(time: 10, unit: 'SECONDS')
            retryCount++
          }

          if (status == 'completed' && conclusion == 'success') {
            echo "✅ GitHub Actions finalizou com sucesso (run ${newRunId})"
          } else {
            error "❌ Workflow falhou ou não concluiu: status=${status}, conclusion=${conclusion}"
          }
        }
      }
    }
  }
}
