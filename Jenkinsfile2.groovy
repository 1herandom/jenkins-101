pipeline {
    agent any
    environment {
        APP_NAME   = "myapp"
        DOCKER_IMG = "/opt/dockerimg"
        PORT_STOR  = "/opt/cicd/current-port.txt"
        TAG_FILE   = "/opt/cicd/build-info.txt"
        WORKING_BUILD = "/opt/cicd/working_build_info.txt"
        WORKINGPORT = "8000"
    }
    stages {
        stage('select') {
            steps {
                sh '''
                    set -e

                    TAG=$(cat ${WORKING_BUILD})

                    echo "TAG=$TAG"

                    docker rm -f ${APP_NAME}-${WORKINGPORT} 2>/dev/null || true
                    docker run -d \
                    --name ${APP_NAME}-${WORKINGPORT} \
                    --restart unless-stopped \
                    -p ${WORKINGPORT}:8000 \
                    ${APP_NAME}:build-$TAG

                    echo "8000" > "$PORT_STOR"

                    docker ps --filter "name=^myapp-test$"
                '''
            }
        }
    }
}
