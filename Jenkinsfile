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
            sh '''
              PORT=$(cat ${PORT_STOR})
              if [ "$PORT" = "8000" ]; then WORKINGPORT=8001; OLDPORT=8000; else WORKINGPORT=8000; OLDPORT=8001; fi
            '''
          }
        }
      stage('RUn') {
         steps{
            sh ''' 
            git clone "${REPO_URL}"

            cd jenkins-101/myapp
            docker build -t ${APP_NAME}:build-${BUILD_NUMBER} .
            docker save -o /opt/dockerimg/${APP_NAME}:${BUILD_NUMBER}.tar ${APP_NAME}:${BUILD_NUMBER}
            echo $BUILD_NUMBER > ${BUILD_INFO}

            docker run -d \
                        --name ${APP_NAME}-${BUILD_NUMBER} \
                        --restart unless-stopped \
                        -p ${PORT}:8000 \
                        ${APP_NAME}:build-${BUILD_NUMBER}
            cd ../.. 
            rm -rf jenkins-101
            '''
          } 
        }
      stage('cheak and deploy') {
          steps{
              sh ''' 
              CHECK=$(curl -sf http://localhost:${WORKINGPORT}${HRALTH} > /dev/null; echo $?)
              if [ $CHECK = 0 ]; then
                echo 'upstream app_backend { server 127.0.0.1:$PORT; keepalive 32; }' > /etc/nginx/upstreams/app_backend.conf
                nginx -t 
                nginx -s reload
                echo $PORT > ${PORT_STOR}
                docker rm -f ${APP_NAME}-${OLDPORT} 2>/dev/null || true
              else
                docker rm -f ${APP_NAME}-${WORKINGPORT} 2>/dev/null || true
              fi
              '''
            }
        }
    }
}
