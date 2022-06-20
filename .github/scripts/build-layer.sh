#!/bin/bash

echo $FILES

mkdir python
python -m pip install -r requirements.txt --target python
cp -rf src python/
zip -r backend-lambda-layer-$COMMITID.zip python/

aws s3 cp backend-lambda-layer-$COMMITID.zip s3://prepaire-$ENV-lambda-artifact-us/layers/

aws lambda publish-layer-version --layer-name backend-layer-$ENV --content S3Bucket=prepaire-$ENV-lambda-artifact-us,S3Key=layers/backend-lambda-layer-$COMMITID.zip --compatible-runtimes python3.9

layerArn=`aws lambda list-layer-versions --layer-name backend-layer-$ENV --region us-east-1 --query 'LayerVersions[0].LayerVersionArn' --output text`

echo $layerArn

#Update all lambda functions with this layer
if [[ $ENV == 'dev' ]]; then
lambdas="$(aws lambda list-functions --region us-east-1 --query 'Functions[?starts_with(FunctionName, `prepaire-dev-backend`) == `true`].FunctionName' --output text)"

elif [[ $ENV == 'prod' ]]; then
lambdas="$(aws lambda list-functions --region us-east-1 --query 'Functions[?starts_with(FunctionName, `prepaire-prod-backend`) == `true`].FunctionName' --output text)"

else
lambdas="$(aws lambda list-functions --region us-east-1 --query 'Functions[?starts_with(FunctionName, `prepaire-stage-backend`) == `true`].FunctionName' --output text)"
fi

for lamb in $lambdas; do
aws lambda update-function-configuration --function-name $lamb --layers $layerArn
done

aws ssm put-parameter --overwrite --name lambda_last_commit_id_$ENV --value $COMMITID
