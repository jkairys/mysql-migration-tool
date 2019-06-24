pipeline {
  agent any
  stages {

    stage('build') {
      steps {
        // git credentialsId: 'bitbucket', url: 'https://jkairys@bitbucket.org/jkairys/dev.publicoutreachgroup.com.git', branch: 'bruce2-legacy'
        script {
          env.TAG = readFile "src/version.txt"
          env.TAG = env.TAG.trim()
          env.REPO = 'registry.k8s.doober.space'
          env.IMAGE = 'db-migration-tool'
          env.IMAGE_REMOTE = "${env.REPO}/${env.IMAGE}:${env.TAG}"
        }
        container('docker') {
          echo "Building ${env.IMAGE_REMOTE}"
          sh "docker build -t ${env.IMAGE_REMOTE} ."
        }
      }
    }

    stage('test') {
      steps {
        container('docker-compose') {
          sh "docker-compose -f docker-compose.test.yml up -d && docker wait ci-schema-migration && docker logs ci-schema-migration"
          // sh "cd tests && ./restore-database.sh"
          // sh "docker-compose exec newman newman run /opt/tests/bruce_v2.postman_collection.json --environment /opt/tests/test.postman_environment.json --iteration-count 1"
          // sh "docker rm -f bruce2 || true"
          // sh "docker run --name bruce2 -d ${env.IMAGE_REMOTE}-5.6"
          // sh "pwd"
          // sh "ls -la \$(pwd)/tests/api"
          // sh "docker run --link bruce2:bruce2 --rm -v \$(pwd)/tests/api:/etc/newman -t postman/newman:alpine run /etc/newman/bruce_v2.postman_collection.json --environment /etc/newman/test.postman_environment.json --iteration-count 1"
          // sh "docker stop bruce2 && docker rm -f bruce2"
        }
      }
    }

    stage('push') {
      steps {
        container('docker') {
          echo "Pushing ${env.IMAGE_REMOTE}"
          sh "docker push ${env.IMAGE_REMOTE}"
        }
      }
    }

  }
}
