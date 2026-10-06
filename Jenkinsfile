pipeline {
    agent any

    environment {
        APP_NAME = "myapp"
        REPO_URL = "https://github.com/1herandom/jenkins-101.git"
        PORT_STOR = "/opt/cicd/current-port.txt"
        BUILD_INFO = "/opt/cicd/biuild-info.txt"
        HRALTH = '/health'
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
                    }
                    else {
                        env.WORKINGPORT = "8000"
                        env.OLDPORT     = "8001"
                    }
                    echo "PORT=${PORT} WORKINGPORT=${env.WORKINGPORT} OLDPORT=${env.OLDPORT}"
                }
            }
        }
        stage('RUn') {
            steps {
                sh '''
                rm -rf jenkins-101
                git clone "${REPO_URL}"

                cd jenkins-101/myapp
                docker build -t ${APP_NAME}:build-${BUILD_NUMBER} .
                docker save -o /opt/dockerimg/${APP_NAME}:${BUILD_NUMBER}.tar ${APP_NAME}:build-${BUILD_NUMBER}
                echo $BUILD_NUMBER > ${BUILD_INFO}

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
        stage('cheak and deploy') {
            steps {
                sh '''
                CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${WORKINGPORT}${HRALTH})
                if [ "$CHECK" = "200" ]; then
                  echo "upstream app_backend { server 127.0.0.1:${WORKINGPORT}; keepalive 32; }" > /etc/nginx/upstreams/app_backend.conf
                  nginx -t
                  nginx -s reload
                  echo ${WORKINGPORT} > ${PORT_STOR}
                  docker rm -f ${APP_NAME}-${OLDPORT} 2>/dev/null || true
                else
                  docker rm -f ${APP_NAME}-${WORKINGPORT} 2>/dev/null || true
                fi
                '''
            }
        }
    }
}
