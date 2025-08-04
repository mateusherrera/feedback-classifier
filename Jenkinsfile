pipeline {
  agent any

  environment {
    REPO         = 'mateusherrera/feedback-classifier'
    REF          = 'main'
    GITHUB_TOKEN = credentials('github-token')
  }

  stages {
    stage('Run All Tests') {
      steps {
        // aqui ativamos o wrapper ANSI só para este bloco
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            // seu laço de testes (unit + integration)
            runOnGitHub('unit-tests.yml', 'test_classifier.py')
            runOnGitHub('integration-tests.yml', 'test_integration.py')
          }
        }
      }
    }
  }
}

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

  def conclusion = sh(
    script: """
      curl -s -H "Authorization: token $GITHUB_TOKEN" \\
        https://api.github.com/repos/$REPO/actions/workflows/$workflowFile/runs?per_page=1 \\
      | jq -r '.workflow_runs[0].conclusion'
    """,
    returnStdout: true
  ).trim()

  if (conclusion == 'success') {
    // ✔️ é o Heavy Check Mark com emoji-variant (verde)
    echo "✔️  ${testFile} executado com sucesso"
  } else {
    // ❌ é o Cross Mark emoji (vermelho)
    error "❌  ${workflowFile}[${testFile}] retornou: ${conclusion}"
  }
}
