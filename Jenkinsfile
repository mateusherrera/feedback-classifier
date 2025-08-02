pipeline {
  agent any

  environment {
    GITHUB_TOKEN  = credentials('github-token')  // PAT com repo+workflow
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

    stage('Aguardar resultado do GitHub Actions') {
      steps {
        script {
          echo "Aguardando resultado do workflow '${WORKFLOW_NAME}' na branch '${BRANCH}'..."

          def maxRetries = 30
          def sleepSeconds = 10
          def workflowRunId = null

          for (int i = 0; i < maxRetries; i++) {
            def response = sh(
              script: """
                curl -s -H "Authorization: token $GITHUB_TOKEN" \
                  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs?branch=$BRANCH&event=repository_dispatch
              """,
              returnStdout: true
            ).trim()

            def json = readJSON text: response
            def latestRun = json.workflow_runs?.find { it.name == WORKFLOW_NAME }

            if (latestRun) {
              workflowRunId = latestRun.id
              echo "Workflow iniciado. ID: ${workflowRunId}"
              break
            }

            echo "Aguardando início do workflow..."
            sleep time: sleepSeconds, unit: 'SECONDS'
          }

          if (!workflowRunId) {
            error "Timeout: workflow '${WORKFLOW_NAME}' não foi iniciado."
          }

          // Agora espera até terminar
          def status = ''
          def conclusion = ''
          for (int i = 0; i < maxRetries; i++) {
            def runResponse = sh(
              script: """
                curl -s -H "Authorization: token $GITHUB_TOKEN" \
                  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs/${workflowRunId}
              """,
              returnStdout: true
            ).trim()

            def runJson = readJSON text: runResponse
            status = runJson.status
            conclusion = runJson.conclusion

            echo "Status: ${status}, Conclusion: ${conclusion ?: 'em andamento...'}"

            if (status == 'completed') {
              break
            }

            sleep time: sleepSeconds, unit: 'SECONDS'
          }

          if (conclusion != 'success') {
            error "GitHub Actions falhou com status: ${conclusion}"
          }

          echo "GitHub Actions finalizou com sucesso!"
        }
      }
    }
  }
}
