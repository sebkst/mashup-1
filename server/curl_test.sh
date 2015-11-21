#!/bin/bash
for i in {1..50}
do
   curl -H "Content-Type: application/json" -X POST -d '{"comment": "this is the program number '$i'","name": "Myprogram'$i'","pdata": [{"volume": "10","flowrate": "10","repetitions": "1","timeout": "1"},{"volume": "5","flowrate": "1", "repetitions": "2","timeout": "2"},{"volume": "7","flowrate": "100","repetitions": "3","timeout": "1"}]}' http://192.168.2.137:80/api/v1/programs >/dev/null 2>&1
   #echo '{"name": "Myprogram'$i'"}'
done



#curl -H "Content-Type: application/json" -X POST -d '{"jobsequence": ["programs:1","programs:2"]}' http://192.168.2.137:80/api/v1/jobsequence
#curl -H "Content-Type: application/json" -X GET http://192.168.2.137:80/api/v1/jobsequence

curl -H "Content-Type: application/json" -X GET http://192.168.2.137:80/api/v1/programs




#curl -H "Content-Type: application/json" -X POST http://192.168.2.137:80/api/v1/start
