import json
import logging
import random
from typing import Iterator

import pytz

from datetime import datetime
from urllib.parse import parse_qs, urlencode

from flask import request as Request

from .constants import DATE_FORMAT, QUERYSTRING_BLACKLIST
from .decorators import timeit

logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    return request.remote_addr.strip() if request.remote_addr else ''


def get_user_agent(request: Request) -> str:
    return request.headers.get('User-Agent', '')


def get_request_referer(request: Request) -> str:
    return request.headers.get('Referer', '')


def get_tracking_data_from_request(request: Request, domain_name: str) -> dict:
    return {
        'domain_name': domain_name,
        'user_agent': get_user_agent(request),
        'referer': get_request_referer(request),
        'ip': get_client_ip(request),
        'redirect_date': datetime.now(tz=pytz.UTC).strftime(DATE_FORMAT),
    }


@timeit
def save_tracking_data(tracking_data: dict) -> None:
    """
    This would save the tracking_data on a distributed DynamoDB which would trigger an async event to a global SQS queue
    consumed by our Django backend (we could use Celery for that).
    See the architectural diagram on README.md file.
    Further reading: https://medium.com/swlh/aws-dynamodb-triggers-event-driven-architecture-61dea6336efb
    :param tracking_data:
    :return:
    """
    pass


def clean_querystring(querystring: str) -> str:
    parsed_qs = parse_qs(querystring, keep_blank_values=True)

    for key_to_remove in QUERYSTRING_BLACKLIST:
        parsed_qs.pop(key_to_remove, None)

    return urlencode(parsed_qs, doseq=True)


def get_available_domains_for_pool(domain_pool_id: int, source_file: str = None) -> Iterator:
    """
    This is fetching the domain_data from a local .jsonl file for the sake of simplicity.
    For production environment, it would be getting the domain data from a distributed DynamoDB instead.
    This data is generated by the Backend ETL process everytime a Domain is saved.
    See the architectural diagram on README.md file.
    :param domain_pool_id:
    :param source_file:
    :return:
    """
    source_file = source_file or "../domains.jsonl"
    with open(source_file, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                domain = json.loads(line.strip())
                if int(domain["domain_pool_id"]) == domain_pool_id:  # This would be a DynamoDB query filtering by key
                    yield domain
            except json.JSONDecodeError:
                logger.exception(f"Error decoding JSON. Skipping line: {line.strip()}")


def get_domain_randomly(domains: Iterator) -> str:
    domains_list = []
    for domain in domains:
        domains_list += [domain["domain_name"]] * domain["domain_weight"]

    return random.choice(domains_list)


@timeit
def get_suitable_domain(domain_pool_id: int):
    domains = get_available_domains_for_pool(domain_pool_id)
    return get_domain_randomly(domains)
