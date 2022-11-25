import base64
import gzip
import json
import logging
import os

import boto3

from aws_monitoring import log_parser, opensearch
from aws_monitoring import kinesis

logging.basicConfig(format='%(name)s %(asctime)s.%(msecs)03dZ %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger('billy')
LOGGER.setLevel(os.getenv('log_level', default='DEBUG'))


def get_logs(event) -> list:
    logs = []
    if not event.get('Records'):
        return logs
    for record in event['Records']:
        message = json.loads(gzip.decompress(base64.b64decode(record["kinesis"]["data"])).decode('utf-8'))
        logs.extend([log_event['message'] for log_event in message['logEvents']])
    return logs


def parse_logs(event, context):
    LOGGER.info('Parsing logs...')
    LOGGER.info(event)
    LOGGER.info(context)

    logs = [log_parser.parse(log) for log in get_logs(event)]

    # opensearch.add_documents(*[log for log in logs if log is not None], os_client=opensearch.client())
    kinesis.put_records(*logs, stream_name=os.environ['firehose_stream'], kinesis_client=boto3.client('firehose'))
    return {
        "statusCode": 200,
        "body": json.dumps('OK'),
    }
