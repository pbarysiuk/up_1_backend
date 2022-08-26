#!/bin/bash

for file in $FILES;do

module=`echo $file | awk -F '/' '{print $2}'`
if [[ $module != "3dplot" ]];then
func=`echo $file | awk -F '/' '{print $3}'`

chmod 777 $file

zip -j backend-$module-$func-$COMMITID.zip $file

cp backend-$module-$func-$COMMITID.zip backend-$module-$func-latest.zip

aws s3 cp backend-$module-$func-$COMMITID.zip s3://prepaire-$ENV-lambda-artifact-us1/
aws s3 cp backend-$module-$func-latest.zip s3://prepaire-$ENV-lambda-artifact-us1/latest/

aws lambda update-function-code --function-name prepaire-$ENV-backend-$module-$func --s3-bucket prepaire-$ENV-lambda-artifact-us1 --s3-key backend-$module-$func-$COMMITID.zip

else

chmod 777 $file

zip -j backend-$module-$COMMITID.zip $file

cp backend-$module-$COMMITID.zip backend-$module-latest.zip

aws s3 cp backend-$module-$COMMITID.zip s3://prepaire-$ENV-lambda-artifact-us1/
aws s3 cp backend-$module-latest.zip s3://prepaire-$ENV-lambda-artifact-us1/latest/

aws lambda update-function-code --function-name prepaire-$ENV-backend-$module --s3-bucket prepaire-$ENV-lambda-artifact-us1 --s3-key backend-$module-$COMMITID.zip

fi

done

aws ssm put-parameter --overwrite --name lambda_last_commit_id_$ENV --value $COMMITID
