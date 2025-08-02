pipeline {
  agent any

  environment {
    GITHUB_TOKEN  = credentials('github-token')
    REPO_OWNER    = 'mateusherrera'
    REPO_NAME     = 'feedback-classifier'
    WORKFLOW_NAME = 'CI - Pytest'
    BRANCH        = 'main'
  }

  stages {
    stage('Disparar GitHub Actions') {
      steps {
        echo "Disparando GitHub Actions para ${env.REPO_OWNER}/${env.REPO_NAME}"

        sh '''
          curl -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/dispatches \
            -d '{"event_type":"ci-pipeline"}'
        '''
      }
    }

    stage('Aguardar Resultado') {
      steps {
        script {
          echo "Aguardando workflow '${env.WORKFLOW_NAME}' na branch '${env.BRANCH}'..."

          def maxRetries = 30
          def sleepSeconds = 10
          def workflowRunId = ''

          for (int i = 0; i < maxRetries; i++) {
            def result = sh(
              script: """
                curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs?branch=$BRANCH&event=repository_dispatch | \\
                  jq -r '.workflow_runs[] | select(.name=="$WORKFLOW_NAME") | .id' | head -n1
              """,
              returnStdout: true
            ).trim()

            if (result) {
              workflowRunId = result
              echo "Workflow iniciado. ID: ${workflowRunId}"
              break
            }

            sleep time: sleepSeconds, unit: 'SECONDS'
          }

          if (!workflowRunId) {
            error "Timeout: workflow '${env.WORKFLOW_NAME}' não foi iniciado."
          }

          def status = ''
          def conclusion = ''
          for (int i = 0; i < maxRetries; i++) {
            def json = sh(
              script: """
                curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs/${workflowRunId}
              """,
              returnStdout: true
            ).trim()

            status = sh(script: "echo '${json}' | jq -r '.status'", returnStdout: true).trim()
            conclusion = sh(script: "echo '${json}' | jq -r '.conclusion'", returnStdout: true).trim()

            echo "Status: ${status}, Conclusion: ${conclusion}"

            if (status == 'completed') {
              break
            }

            sleep time: sleepSeconds, unit: 'SECONDS'
          }

          if (conclusion != 'success') {
            error "GitHub Actions falhou com status: ${conclusion}"
          }

          echo "GitHub Actions finalizou com sucesso."
        }
      }
    }
  }
}
