import os
from functools import lru_cache

import pytest


@pytest.fixture()
def config_valid():
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


@pytest.fixture()
def kinesis_records_valid():
    return {'Records': [{'kinesis': {'kinesisSchemaVersion': '1.0', 'partitionKey': 'da743eba7740c339b6fcd003e0a91aa9',
                                     'sequenceNumber': '49635480795315813972214905381821711856630117573081432066',
                                     'data': 'H4sIAAAAAAAAAK2T207bQBCGX2XlGy6K7dnZc+44mICA0Cqu1DaKKuNsEquOHdkGhBDvzji0UlWCFKC2LNuzs7Pf/PvvQ7DybZstfHq/9sEgOD5ID35eJuPxwTAJ9oP6rvINhTkIUKCsExIpXNaLYVPfrGlkWc/qJvR5GyZH44vf8fD822Wdjs6vTtLD78/5467x2YomUOpmTptnZVEt4ucC2XodS6NlNjcerpWUKGbOyLkV3JuZn3ubayrU3ly3eVOsu6KuToqy800bDCZBdteu6qro6oYqhrTaon+PXySHOC9P67I5K7+czYPpBiy59VXXV3kIihnxCYOopbNWO644OkX/wmmnldZKCC6Qayut01oqpC8UBCtFL0tXkJhdtiJduNYOnXA0jHz/j8hUfoKAGHIeomQcB1INJLJPQNeUTRw9x8nh1+GUDZOUxcHj/seoxI5UW6AiSvnBzkYnV4Ojpc9/kaKsvW87v2JLn5XdMoqi7XxGKKelNsop6TRaKw1aZSQIvlleo6OXRArC63z4Nx+HCCIeScNCuico41F9G/fUg39F3Nsox07T9HPMI77HEIBZxsEiTU0uDsPTDf6mKd/EGMGH2+A7trHr5h+VddvrnddV5fPevxHbAmloi4BwhLSKLCEcGAOOGkXJQXGrpQGNinNrLJf2NUgF4n869G1UbkeqbQ6llHc4lPjoFgiOQha0MwB9RFmO1rj+cNHRAW6ssnS6XueTLxyKEcL7Leqot90d+rY2zI5tfMyh08cnD8W9RVAGAAA=',
                                     'approximateArrivalTimestamp': 1669293942.703}, 'eventSource': 'aws:kinesis',
                         'eventVersion': '1.0',
                         'eventID': 'shardId-000000000000:49635480795315813972214905381821711856630117573081432066',
                         'eventName': 'aws:kinesis:record',
                         'invokeIdentityArn': 'arn:aws:iam::103050589342:role/awsmonitoring-logging-LogParserFunctionRole-1T5DYA667S2V',
                         'awsRegion': 'eu-central-1',
                         'eventSourceARN': 'arn:aws:kinesis:eu-central-1:103050589342:stream/LogKinesisStream'}]}
