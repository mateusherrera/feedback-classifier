pipeline {
  agent any
  environment {
    REPO_OWNER    = 'mateusherrera'
    REPO_NAME     = 'feedback-classifier'
    BRANCH        = 'main'
    WORKFLOW_NAME = 'CI - Pytest'
    GITHUB_TOKEN  = credentials('github-token')
  }

  stages {
    stage('Dispatch & Wait') {
      steps {
        script {
          // 1) Captura workflow ID
          def workflowId = sh(script: """
            curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                 -H "Accept: application/vnd.github.v3+json" \\
                 https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows \\
              | jq -r '.workflows[] | select(.name=="${WORKFLOW_NAME}") | .id'
          """, returnStdout: true).trim()

          // 2) Captura último run antes do dispatch
          def lastRunId = sh(script: """
            curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                 "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/${workflowId}/runs?branch=$BRANCH&per_page=1" \\
              | jq -r '.workflow_runs[0].id // empty'
          """, returnStdout: true).trim()

          echo "Workflow ID = ${workflowId}, LastRun = ${lastRunId ?: 'nenhum'}"

          // 3) Dispara o workflow
          sh """
            curl -X POST \\
              -H "Authorization: token $GITHUB_TOKEN" \\
              -H "Accept: application/vnd.github.v3+json" \\
              https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/${workflowId}/dispatches \\
              -d '{"ref":"${BRANCH}"}'
          """

          // 4) Polling até encontrar um novo run concluído
          def newRunId = ''
          def status   = ''
          def conclusion = ''

          for (int i = 0; i < 30; i++) {
            def out = sh(script: """
              curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/${workflowId}/runs?branch=$BRANCH&per_page=1" \\
                | jq -r '.workflow_runs[0] | [.id, .status, .conclusion] | @tsv'
            """, returnStdout: true).trim()

            def parts = out.tokenize('\\t')
            newRunId   = parts[0]
            status     = parts[1]
            conclusion = parts[2] ?: ''

            if (newRunId != lastRunId && status == 'completed') {
              echo "→ Encontrei run ${newRunId}: status=${status}, conclusion=${conclusion}"
              break
            }

            echo "→ Aguardando novo run (ainda ${newRunId})"
            sleep time: 10, unit: 'SECONDS'
          }

          // 5) Validar sucesso/falha
          if (status == 'completed' && conclusion == 'success') {
            echo "✅ Workflow finalizado com sucesso (run ${newRunId})"
          } else {
            error("❌ Workflow falhou ou não concluiu: status=${status}, conclusion=${conclusion}")
          }
        }
      }
    }
  }
}
