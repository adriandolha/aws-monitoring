#!/bin/bash
APP_REGION="eu-central-1"

aws cloudformation create-stack --stack-name awsmonitoring-opensearch \
    --template-body file://opensearch.yml \
    --capabilities CAPABILITY_IAM \
    --region $APP_REGION

