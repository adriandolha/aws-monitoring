import gzip
import json

import boto3


def put_records(*records, stream_name, kinesis_client):
    for record in records:
        if record:
            print(f'Send log to firehose {record}...')
            response = kinesis_client.put_record(
                DeliveryStreamName=stream_name,
                Record={'Data': json.dumps(record).strip().encode('utf-8')})
            print(response)
