pipeline {
  agent any

  environment {
    REPO_OWNER    = 'mateusherrera'
    REPO_NAME     = 'feedback-classifier'
    BRANCH        = 'main'
    WORKFLOW_NAME = 'CI - Pytest'
  }

  stages {
    stage('Dispatch GitHub Actions Workflow') {
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          script {
            try {
              // 1) Buscar workflow ID
              echo "🔍 Searching for workflow '${WORKFLOW_NAME}'..."
              
              def workflowId = sh(
                returnStdout: true,
                script: """
                  curl -s -f -H "Authorization: Bearer ${GITHUB_TOKEN}" \\
                       -H "Accept: application/vnd.github.v3+json" \\
                       "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows" \\
                       | jq -r '.workflows[] | select(.name=="${WORKFLOW_NAME}") | .id'
                """
              ).trim()
              if (!workflowId || workflowId == 'null' || workflowId == '') {
                error "❌ Workflow '${WORKFLOW_NAME}' not found in repository"
              }
              
              echo "✅ Found workflow ID: ${workflowId}"

              // 2) Obter último run ID antes do dispatch
              echo "📋 Getting latest run ID..."
              
              def lastRunId = sh(
                returnStdout: true,
                script: """
                  curl -s -f -H "Authorization: Bearer ${GITHUB_TOKEN}" \\
                       -H "Accept: application/vnd.github.v3+json" \\
                       "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflowId}/runs?branch=${BRANCH}&per_page=1" \\
                       | jq -r '.workflow_runs[0].id // "none"'
                """
              ).trim()
              
              echo "Last run ID: ${lastRunId}"

              // 3) Disparar workflow
              echo "🚀 Dispatching workflow..."
              
              def dispatchResult = sh(
                returnStatus: true,
                script: """
                  curl -s -f -X POST \\
                       -H "Authorization: Bearer ${GITHUB_TOKEN}" \\
                       -H "Accept: application/vnd.github.v3+json" \\
                       -H "Content-Type: application/json" \\
                       -d '{"ref":"${BRANCH}"}' \\
                       "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflowId}/dispatches"
                """
              )

              if (dispatchResult != 0) {
                error "❌ Failed to dispatch workflow"
              }
              
              echo "✅ Workflow dispatched successfully"

              // 4) Aguardar e monitorar execução
              echo "⏳ Waiting for workflow to start and complete..."
              
              def maxAttempts = 60  // 10 minutos total
              def newRunId = null
              def finalStatus = null
              def finalConclusion = null
              def found = false

              sleep time: 10, unit: 'SECONDS'  // Aguarda workflow aparecer

              for (int attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                  // Parse usando jq para obter id|status|conclusion
                  def runInfo = sh(
                    returnStdout: true,
                    script: """
                      curl -s -f -H "Authorization: Bearer ${GITHUB_TOKEN}" \\
                           -H "Accept: application/vnd.github.v3+json" \\
                           "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflowId}/runs?branch=${BRANCH}&per_page=1" \\
                           | jq -r '.workflow_runs[0] | if . != null then "\\(.id)|\\(.status)|\\(.conclusion // "null")" else "empty" end'
                    """
                  ).trim()
                  
                  if (runInfo == 'empty' || runInfo == 'null') {
                    echo "→ Attempt ${attempt}/${maxAttempts}: No runs found yet"
                    sleep time: 10, unit: 'SECONDS'
                    continue
                  }

                  def parts = runInfo.split('\\|')
                  if (parts.length < 2) {
                    echo "→ Attempt ${attempt}/${maxAttempts}: Invalid response format"
                    sleep time: 10, unit: 'SECONDS'
                    continue
                  }

                  newRunId = parts[0]
                  finalStatus = parts[1]
                  finalConclusion = parts.length > 2 ? parts[2] : 'null'

                  // Verificar se é um novo run
                  if (newRunId != lastRunId) {
                    if (finalStatus == 'completed') {
                      echo "✅ New run ${newRunId} completed with conclusion: ${finalConclusion}"
                      found = true
                      break
                    } else {
                      echo "→ Attempt ${attempt}/${maxAttempts}: Run ${newRunId} in progress (${finalStatus})"
                    }
                  } else {
                    echo "→ Attempt ${attempt}/${maxAttempts}: Waiting for new run to appear..."
                  }

                  sleep time: 10, unit: 'SECONDS'

                } catch (Exception e) {
                  echo "→ Attempt ${attempt}/${maxAttempts}: Error checking status - ${e.getMessage()}"
                  sleep time: 10, unit: 'SECONDS'
                }
              }

              // 5) Verificar resultado final
              if (!found) {
                error "❌ Timeout: Workflow did not complete within ${maxAttempts * 10} seconds"
              }

              switch (finalConclusion) {
                case 'success':
                  echo "🎉 Workflow completed successfully! (Run ID: ${newRunId})"
                  break
                case 'failure':
                  error "❌ Workflow failed (Run ID: ${newRunId})"
                  break
                case 'cancelled':
                  error "❌ Workflow was cancelled (Run ID: ${newRunId})"
                  break
                case 'timed_out':
                  error "❌ Workflow timed out (Run ID: ${newRunId})"
                  break
                default:
                  error "❌ Workflow completed with unexpected conclusion: ${finalConclusion} (Run ID: ${newRunId})"
              }

            } catch (Exception e) {
              echo "❌ Pipeline failed with error: ${e.getMessage()}"
              throw e
            }
          }
        }
      }
    }
  }

  post {
    always {
      echo "🔄 Pipeline execution completed"
    }
    success {
      echo "✅ Pipeline succeeded - GitHub Actions workflow completed successfully"
    }
    failure {
      echo "❌ Pipeline failed - Check logs for details"
    }
  }
}
