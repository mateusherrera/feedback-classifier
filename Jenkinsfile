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
              
              def workflowsResponse = httpRequest(
                httpMode: 'GET',
                url: "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows",
                customHeaders: [
                  [name: 'Authorization', value: "token ${GITHUB_TOKEN}"],
                  [name: 'Accept', value: 'application/vnd.github.v3+json']
                ],
                consoleLogResponseBody: false
              )

              def workflows = readJSON text: workflowsResponse.content
              def targetWorkflow = workflows.workflows.find { it.name == WORKFLOW_NAME }
              
              if (!targetWorkflow) {
                error "❌ Workflow '${WORKFLOW_NAME}' not found in repository"
              }
              
              def workflowId = targetWorkflow.id
              echo "✅ Found workflow ID: ${workflowId}"

              // 2) Obter último run ID antes do dispatch
              echo "📋 Getting latest run ID..."
              
              def runsResponse = httpRequest(
                httpMode: 'GET',
                url: "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflowId}/runs?branch=${BRANCH}&per_page=1",
                customHeaders: [
                  [name: 'Authorization', value: "token ${GITHUB_TOKEN}"],
                  [name: 'Accept', value: 'application/vnd.github.v3+json']
                ],
                consoleLogResponseBody: false
              )

              def runs = readJSON text: runsResponse.content
              def lastRunId = runs.workflow_runs.size() > 0 ? runs.workflow_runs[0].id : null
              
              echo "Last run ID: ${lastRunId ?: 'none'}"

              // 3) Disparar workflow
              echo "🚀 Dispatching workflow..."
              
              def dispatchResponse = httpRequest(
                httpMode: 'POST',
                url: "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflowId}/dispatches",
                customHeaders: [
                  [name: 'Authorization', value: "token ${GITHUB_TOKEN}"],
                  [name: 'Accept', value: 'application/vnd.github.v3+json'],
                  [name: 'Content-Type', value: 'application/json']
                ],
                requestBody: """{"ref":"${BRANCH}"}""",
                consoleLogResponseBody: false
              )

              if (dispatchResponse.status != 204) {
                error "❌ Failed to dispatch workflow. Status: ${dispatchResponse.status}"
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
                  def currentRunsResponse = httpRequest(
                    httpMode: 'GET',
                    url: "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflowId}/runs?branch=${BRANCH}&per_page=1",
                    customHeaders: [
                      [name: 'Authorization', value: "token ${GITHUB_TOKEN}"],
                      [name: 'Accept', value: 'application/vnd.github.v3+json']
                    ],
                    consoleLogResponseBody: false
                  )

                  def currentRuns = readJSON text: currentRunsResponse.content
                  
                  if (currentRuns.workflow_runs.size() == 0) {
                    echo "→ Attempt ${attempt}/${maxAttempts}: No runs found yet"
                    sleep time: 10, unit: 'SECONDS'
                    continue
                  }

                  def latestRun = currentRuns.workflow_runs[0]
                  newRunId = latestRun.id
                  finalStatus = latestRun.status
                  finalConclusion = latestRun.conclusion

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
