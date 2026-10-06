pipeline {
    agent any
    environment {
        DOCKER_IMG = "/opt/dockerimg/"
        PORT_STOR  = "/opt/cicd/current-port.txt"
      }
    stages {
        stage('select') {
        steps {
          sh '''
           KEEP=$(ls -t /opt/dockerimg/*.tar | sed -n '2p')
           cd "${DOCKER_IMG}"
           docker load -i $KEEP
           docker rm -f $(docker ps -aq --filter "name=myapp")
           docker run -d \
            --name myapp-test \
            -p 9000:8000 \
            myapp:build-41
            
           echo "8000" > "${PORT_STOR}"
           
           '''
        }
      }
  }
