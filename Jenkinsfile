pipeline {
  agent any

  options {
    // habilita cores ANSI no log
    ansiColor('xterm')
  }

  environment {
    REPO         = 'mateusherrera/feedback-classifier'
    REF          = 'main'
    GITHUB_TOKEN = credentials('github-token')
  }

  stages {
    stage('Run Unit Tests') {
      steps {
        script {
          def unitTests = ['test_classifier.py']
          for (file in unitTests) {
            runOnGitHub('unit-tests.yml', file)
          }
        }
      }
    }

    stage('Run Integration Tests') {
      steps {
        script {
          def intTests = [
            'test_auth_and_post_comentario.py',
            'test_comentario_list_and_export.py',
            'test_evals.py',
            'test_insights.py',
            'test_relatorio.py',
            'test_resumo_semanal.py'
          ]
          for (file in intTests) {
            runOnGitHub('integration-tests.yml', file)
          }
        }
      }
    }
  }

  post {
    always {
      echo '🏁 Pipeline finalizada.'
    }
  }
}

// função auxiliar
def runOnGitHub(workflowFile, testFile) {
  echo "▶ Disparando ${workflowFile} [${testFile}]…"
  sh """
    curl -s -X POST \\
      -H "Accept: application/vnd.github+json" \\
      -H "Authorization: token $GITHUB_TOKEN" \\
      https://api.github.com/repos/$REPO/actions/workflows/$workflowFile/dispatches \\
      -d '{ "ref":"$REF", "inputs":{"test_file":"$testFile"} }'
  """

  timeout(time: 5, unit: 'MINUTES') {
    waitUntil {
      def status = sh(
        script: """
          curl -s -H "Authorization: token $GITHUB_TOKEN" \\
            https://api.github.com/repos/$REPO/actions/workflows/$workflowFile/runs?per_page=1 \\
          | jq -r '.workflow_runs[0].status'
        """,
        returnStdout: true
      ).trim()
      return status == 'completed'
    }
  }

  // pega a conclusão
  def conclusion = sh(
    script: """
      curl -s -H "Authorization: token $GITHUB_TOKEN" \\
        https://api.github.com/repos/$REPO/actions/workflows/$workflowFile/runs?per_page=1 \\
      | jq -r '.workflow_runs[0].conclusion'
    """,
    returnStdout: true
  ).trim()

  if (conclusion == 'success') {
    echo "\u001B[32m✅  ${testFile} executado com sucesso\u001B[0m"
  } else {
    error("\u001B[31m❌  ${workflowFile}[${testFile}] retornou: ${conclusion}\u001B[0m")
  }
}
