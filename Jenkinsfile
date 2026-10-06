pipeline {
    agent any

    environment {
        APP_NAME = "myapp"
    }

    stages {
        stage('Check and Deploy') {
            steps {
                sh '''
                    set +e

                    RUNNING=$(docker ps --filter "name=${APP_NAME}-" --filter "status=running" -q)

                    if [ -z "$RUNNING" ]; then
                        TARGET=8000

                    else
                        if curl -sf http://localhost:8000/health > /dev/null; then
                            docker rm -f ${APP_NAME}-8001 2>/dev/null
                            TARGET=8001

                        elif curl -sf http://localhost:8001/health > /dev/null; then
                            docker rm -f ${APP_NAME}-8000 2>/dev/null
                            TARGET=8000

                        else
                            docker rm -f ${APP_NAME}-8000 ${APP_NAME}-8001 2>/dev/null
                            TARGET=8000
                        fi
                    fi
                    cd /jenkins-101/myapp 
                    docker build -t ${APP_NAME}:build-${BUILD_NUMBER} .
                    docker run -d \
                        --name ${APP_NAME}-${TARGET} \
                        --restart unless-stopped \
                        -p ${TARGET}:8000 \
                        ${APP_NAME}:build-${BUILD_NUMBER}

                    cd ../../
                    rm -rf jenkins-101
                '''
            }
        }
    }
}
