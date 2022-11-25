import os
from functools import lru_cache
from uuid import uuid4

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3

INDEX_NAME = 'hodor-logs'


@lru_cache
def load_config():
    import json
    local_config_path = f"{os.path.expanduser('~')}/.cloud-projects/awsmonitoring.json"
    if os.path.exists(local_config_path):
        with open(local_config_path, "r") as _file:
            json = dict(json.load(_file))
            print(json)
            for k, v in json.items():
                os.environ[k] = str(v)
            os.environ['db_setup'] = 'False'
    return os.environ


def client():
    config = load_config()
    host = config['host']
    region = config['region']

    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region)

    _client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return _client


def search(index_name, query):
    response = client().search(
        body=query,
        index=index_name
    )

    print('\nSearch results:')
    print(response)


def create_index(index_name):
    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 1
            }
        }
    }

    response = client().indices.create(index_name, body=index_body)
    print(response)


def add_documents(*docs: dict, os_client: OpenSearch):
    for doc in docs:
        response = os_client.index(
            index=INDEX_NAME,
            body=doc,
            id=str(uuid4()),
            refresh=True
        )
        print(response)


if __name__ == "__main__":
    # create_index(INDEX_NAME)

    query = {
        'size': 5,
        'query': {
            'term': {
                'level': 'INFO'
            }
        }
    }
    search(INDEX_NAME, query)
