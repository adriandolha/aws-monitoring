from app import get_logs, parse_logs
from aws_monitoring import log_parser


class TestLogParser:
    def test_log_app_debug(self):
        result = log_parser.parse(
            "2022-11-24 08:36:59.347Z DEBUG:Required permissions: [<Permissions.USERS_PROFILE: 'users:profile'>]")
        print(result)
        assert result['date'] == '2022-11-24T08:36:59'
        assert result['level'] == 'DEBUG'
        assert str(result['text']).startswith('Required permissions:')

    def test_log_app_error(self):
        result = log_parser.parse(
            "2022-11-24 08:36:59.347Z ERROR:Required permissions: [<Permissions.USERS_PROFILE: 'users:profile'>]")
        print(result)
        assert result['date'] == '2022-11-24T08:36:59'
        assert result['level'] == 'ERROR'
        assert str(result['text']).startswith('Required permissions:')

    def test_log_app_info(self):
        result = log_parser.parse(
            "2022-11-24 08:36:59.347Z INFO:Required permissions: [<Permissions.USERS_PROFILE: 'users:profile'>]")
        print(result)
        assert result['date'] == '2022-11-24T08:36:59'
        assert result['level'] == 'INFO'
        assert str(result['text']).startswith('Required permissions:')

    def test_log_gunicorn(self):
        result = log_parser.parse(
            "10.1.0.1 - - [24/Nov/2022:08:19:37 +0000] 'GET /health HTTP/1.1' 200 8 1607 - kube-probe/1.24")
        assert result['source_ip'] == '10.1.0.1'
        assert result['date'] == '2022-11-24T08:19:37+00:00'
        assert result['http_method'] == 'GET'
        assert result['http_path'] == '/health'
        assert result['http_code'] == '200'

    def test_log_gunicorn_invalid(self):
        result = log_parser.parse_gunicorn_access_log(
            "2022-11-24 08:36:59.347Z DEBUG:Required permissions: [<Permissions.USERS_PROFILE: 'users:profile'>]")
        assert result is None

    def test_log_gunicorn_failed_login(self):
        result = log_parser.parse(
            "10.0.2.207 - test_user21 [25/Nov/2022:11:23:04 +0000] 'GET /api/signin HTTP/1.1' "
            "401 31 4027 - python/gevent-http-client-2.0.8")
        assert result['source_ip'] == '10.0.2.207'
        assert result['date'] == '2022-11-25T11:23:04+00:00'
        assert result['http_method'] == 'GET'
        assert result['http_path'] == '/api/signin'
        assert result['http_code'] == '401'

    def test_app_log_invalid(self):
        result = log_parser.parse_app_log(
            "10.1.0.1 - - [24/Nov/2022:08:19:37 +0000] 'GET /health HTTP/1.1' 200 8 1607 - kube-probe/1.24")
        assert result is None

    def test_kinesis_records(self, kinesis_records_valid):
        logs = get_logs(kinesis_records_valid)
        print(logs)
        parsed_logs = [log_parser.parse(log) for log in logs]
        print(parsed_logs)
        assert len(logs) == 8

    # def test_opensearch(self, kinesis_records_valid, config_valid):
    #     parse_logs(kinesis_records_valid, {})
