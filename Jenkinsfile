pipeline {
    agent any

    environment {
        APP_NAME   = "myapp"
        REPO_URL   = "https://github.com/1herandom/jenkins-101.git"
        PORT_STOR  = "/opt/cicd/current-port.txt"
        BUILD_INFO = "/opt/cicd/build-info.txt"
        HRALTH     = "/health"
    }

    stages {
        stage('port-selection') {
            steps {
                script {
                    def PORT = sh(
                        script: "cat ${env.PORT_STOR} 2>/dev/null || echo 8000",
                        returnStdout: true
                    ).trim()

                    if (PORT == "8000") {
                        env.WORKINGPORT = "8001"
                        env.OLDPORT     = "8000"
                    } else {
                        env.WORKINGPORT = "8000"
                        env.OLDPORT     = "8001"
                    }
                    echo "PORT=${PORT} WORKINGPORT=${env.WORKINGPORT} OLDPORT=${env.OLDPORT}"
                }
            }
        }

        stage('Build and Run') {
            steps {
                sh '''
                rm -rf jenkins-101
                git clone "${REPO_URL}"

                cd jenkins-101/myapp
                docker build -t ${APP_NAME}:build-${BUILD_NUMBER} .
                docker save -o /opt/dockerimg/${APP_NAME}-${BUILD_NUMBER}.tar ${APP_NAME}:build-${BUILD_NUMBER}
                echo $BUILD_NUMBER > ${BUILD_INFO}

                docker rm -f ${APP_NAME}-${WORKINGPORT} 2>/dev/null || true
                docker run -d \
                            --name ${APP_NAME}-${WORKINGPORT} \
                            --restart unless-stopped \
                            -p ${WORKINGPORT}:8000 \
                            ${APP_NAME}:build-${BUILD_NUMBER}

                cd ../..
                rm -rf jenkins-101
                '''
            }
        }

        stage('Health Check and Deploy') {
            steps {
                sh '''
                set +e
                CHECK=000
                for i in $(seq 1 15); do
                    CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${WORKINGPORT}${HRALTH})
                    if [ "$CHECK" = "200" ]; then
                        echo "Health check passed on attempt $i"
                        break
                    fi
                    echo "Attempt $i: got $CHECK, retrying in 2s..."
                    sleep 2

                done

                if [ "$CHECK" = "200" ]; then
                    echo "upstream app_backend { server 127.0.0.1:${WORKINGPORT}; keepalive 32; }" > /etc/nginx/upstreams/app_backend.conf
                    nginx -t
                    nginx -s reload
                    echo ${WORKINGPORT} > ${PORT_STOR}
                    docker rm -f ${APP_NAME}-${OLDPORT} 2>/dev/null || true
                else
                    echo "Health check failed after retries (last code: $CHECK)"
                    docker rm -f ${APP_NAME}-${WORKINGPORT} 2>/dev/null || true
                    exit 1
                fi
                '''
            }
        }
    }

    post {
    success {
        sh '''
        ACTIVE=$(cat ${PORT_STOR} 2>/dev/null || echo "")
        if [ -n "$ACTIVE" ]; then
            echo "Active port: $ACTIVE"
            for name in $(docker ps -a --filter "name=${APP_NAME}-" --format '{{.Names}}'); do
                if [ "$name" != "${APP_NAME}-${ACTIVE}" ]; then
                    echo "Post-cleanup removing: $name"
                    docker rm -f "$name"
                fi
            done
        else
            echo "PORT_STOR is empty — skipping cleanup to avoid removing the live container"
        fi
        '''
    }
  }
}
