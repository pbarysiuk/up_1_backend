#!/bin/bash

for file in $FILES;do

module=`echo $file | awk -F '/' '{print $2}'`
func=`echo $file | awk -F '/' '{print $3}'`

chmod 777 $file

zip -j backend-$module-$func-$COMMITID.zip $file

cp backend-$module-$func-$COMMITID.zip backend-$module-$func-latest.zip

aws s3 cp backend-$module-$func-$COMMITID.zip s3://prepaire-$ENV-lambda-artifact-us/
aws s3 cp backend-$module-$func-latest.zip s3://prepaire-$ENV-lambda-artifact-us/latest/

aws lambda update-function-code --function-name prepaire-$ENV-backend-$module-$func --s3-bucket prepaire-$ENV-lambda-artifact-us --s3-key backend-$module-$func-$COMMITID.zip

done

aws ssm put-parameter --overwrite --name lambda_last_commit_id_$ENV --value $COMMITID
