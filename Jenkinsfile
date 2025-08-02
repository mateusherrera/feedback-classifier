pipeline {
  agent any

  environment {
    REPO_OWNER = 'mateusherrera'
    REPO_NAME  = 'feedback-classifier'
  }

  stages {
    stage('Disparar GitHub Actions') {
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
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
    }

    stage('Aguardar Resultado') {
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          script {
            echo "Aguardando workflow na branch 'main'..."
            def run_id = ''
            def max_tries = 30
            def tries = 0

            while (run_id == '' && tries < max_tries) {
              sleep time: 10, unit: 'SECONDS'
              def output = sh(
                script: """
                  curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                    https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs?branch=main
                """,
                returnStdout: true
              ).trim()

              run_id = output.readLines()
                .findAll { it.contains('"name": "CI - Pytest"') }
                .withIndex()
                .find { it[1] + 1 < output.readLines().size() }
                ?.with { output.readLines()[it[1] + 1] }
                ?.findAll(/\d+/)?.join('')

              tries++
            }

            if (!run_id) {
              error 'Workflow não encontrado ou não iniciado a tempo.'
            }

            echo "Workflow ID encontrado: ${run_id}"
            echo "Aguardando conclusão..."

            def conclusion = ''
            while (conclusion == '') {
              sleep time: 10, unit: 'SECONDS'
              def run_data = sh(
                script: """
                  curl -s -H "Authorization: token $GITHUB_TOKEN" \\
                    https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs/$run_id
                """,
                returnStdout: true
              ).trim()

              conclusion = run_data.readLines().find { it.contains('"conclusion"') }?.split(':')?.last()?.replaceAll(/[",]/, '')?.trim()
              echo "Status atual: ${conclusion ?: 'em execução...'}"
            }

            if (conclusion != 'success') {
              error "Workflow falhou com status: ${conclusion}"
            } else {
              echo 'Workflow do GitHub Actions finalizado com sucesso!'
            }
          }
        }
      }
    }
  }
}
