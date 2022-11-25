#!/bin/bash
APP_REGION="eu-central-1"
MY_IP=${1}
echo $MY_IP
aws cloudformation update-stack --stack-name awsmonitoring-opensearch \
    --template-body file://opensearch.yml \
    --capabilities CAPABILITY_IAM \
    --region $APP_REGION \
    --parameters ParameterKey=MyIp,ParameterValue="$MY_IP"

