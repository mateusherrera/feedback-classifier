pipeline {
  agent any

  environment {
    REPO_OWNER    = 'mateusherrera'
    REPO_NAME     = 'feedback-classifier'
    BRANCH        = 'main'
    WORKFLOW_NAME = 'CI - Pytest'
  }

  stages {
    stage('Dispatch & Wait') {
      steps {
        // injeta GITHUB_TOKEN de forma segura
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          script {
            def workflowId = sh(
              script: '''curl -s -H "Authorization: token $GITHUB_TOKEN" \
                -H "Accept: application/vnd.github.v3+json" \
                https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows \
                | jq -r '.workflows[] | select(.name=="'"$WORKFLOW_NAME"'") | .id''',
              returnStdout: true
            ).trim()

            def lastRunId = sh(
              script: '''curl -s -H "Authorization: token $GITHUB_TOKEN" \
                "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/$workflowId/runs?branch=$BRANCH&per_page=1" \
                | jq -r '.workflow_runs[0].id // empty''',
              returnStdout: true
            ).trim()

            echo "Workflow ID = ${workflowId}, Last run = ${lastRunId ?: 'nenhum'}"

            sh '''curl -X POST \
              -H "Authorization: token $GITHUB_TOKEN" \
              -H "Accept: application/vnd.github.v3+json" \
              https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/$workflowId/dispatches \
              -d '{"ref":"'"$BRANCH"'"}'''

            def newRunId = ''
            def status   = ''
            def conclusion = ''

            for (int i = 0; i < 30; i++) {
              def out = sh(
                script: '''curl -s -H "Authorization: token $GITHUB_TOKEN" \
                  "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/$workflowId/runs?branch=$BRANCH&per_page=1" \
                  | jq -r '.workflow_runs[0] | [.id, .status, .conclusion] | @tsv''',
                returnStdout: true
              ).trim()

              def parts = out.tokenize('\t')
              newRunId   = parts[0]
              status     = parts[1]
              conclusion = parts.size() > 2 ? parts[2] : ''

              if (newRunId != lastRunId && status == 'completed') {
                echo "→ Run ${newRunId} completed (${conclusion})"
                break
              }
              echo "→ Waiting for new run… current = ${newRunId}"
              sleep time: 10, unit: 'SECONDS'
            }

            if (status == 'completed' && conclusion == 'success') {
              echo "✅ Workflow succeeded (run ${newRunId})"
            } else {
              error "❌ Workflow failed: status=${status}, conclusion=${conclusion}"
            }
          }
        }
      }
    }
  }
}
