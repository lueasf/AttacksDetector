#!/bin/bash

IMAGE_NAME="attakx"
CONTAINER_NAME="attakx_container"
PORT=8080

docker build -t $IMAGE_NAME .

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker rm -f $CONTAINER_NAME
fi

docker run -d --name $CONTAINER_NAME -p $PORT:8080 $IMAGE_NAME
sleep 5

curl http://localhost:$PORT/
curl -X POST http://localhost:$PORT/predict \
     -H "Content-Type: application/json" \
     -d '{
           "duration": 0,
           "protocol_type": "tcp",
           "flag": "SF",
           "src_bytes": 181,
           "dst_bytes": 5450,
           "land": 0,
           "wrong_fragment": 0,
           "urgent": 0,
           "hot": 0,
           "num_failed_logins": 0,
           "logged_in": 1,
           "num_compromised": 0,
           "root_shell": 0,
           "su_attempted": 0,
           "num_file_creations": 0,
           "num_shells": 0,
           "num_access_files": 0,
           "is_guest_login": 0,
           "count": 8,
           "srv_count": 8,
           "serror_rate": 0.0,
           "rerror_rate": 0.0,
           "same_srv_rate": 1.0,
           "diff_srv_rate": 0.0,
           "srv_diff_host_rate": 0.0,
           "dst_host_count": 9,
           "dst_host_srv_count": 9,
           "dst_host_same_srv_rate": 1.0,
           "dst_host_diff_srv_rate": 0.0,
           "dst_host_same_src_port_rate": 0.11,
           "dst_host_srv_diff_host_rate": 0.0,
           "time": 1617656527
         }'
echo -e "\n"