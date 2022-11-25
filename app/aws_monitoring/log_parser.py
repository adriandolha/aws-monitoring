import re

# gunicton access logs format - %(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s %(D)s %(f)s %(a)s
# from time import strptime
import datetime


def parse(log: str):
    # print(log)
    return parse_gunicorn_access_log(log) or parse_app_log(log) or None


def find_groups(log, pattern, group_no):
    match = re.match(pattern, log)
    if not match:
        # print(f'no match {pattern}')
        return None
    groups = match.groups()
    if len(groups) != group_no:
        # print(f'group # mismatch {pattern}')
        return None
    return groups


def parse_app_log(log: str) -> dict:
    pattern = '(.*)\.\d*Z\s(DEBUG|INFO|ERROR)\:(.*)'
    groups = find_groups(log, pattern, 3)
    if not groups:
        return None
    result = {'date': datetime.datetime.strptime(groups[0], '%Y-%m-%d %H:%M:%S').isoformat(),
              'level': groups[1],
              'text': groups[2]}
    return result


def parse_gunicorn_access_log(log: str) -> dict:
    pattern = '(?P<spurce_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s.*\s.*\s' \
              '\[(?P<date>.*)\]\s' \
              "'(?P<http_path>.*)'\s" \
              '(?P<http_code>\d{3})'
    groups = find_groups(log, pattern, 4)
    if not groups:
        return None
    path_parts = groups[2].split(' ')

    result = {
        'source_ip': groups[0],
        'date': datetime.datetime.strptime(groups[1], '%d/%b/%Y:%H:%M:%S %z').isoformat(),
        'http_method': path_parts[0],
        'http_path': path_parts[1],
        'http_code': groups[3]
    }

    return result
