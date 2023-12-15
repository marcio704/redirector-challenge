import logging

from flask import Flask, request, abort, redirect

from .constants import DOMAIN_POOL_ID_FIELD
from .utils import get_tracking_data_from_request, clean_querystring, get_suitable_domain, save_tracking_data

logger = logging.getLogger(__name__)


app = Flask(__name__)

# For production environment, this should be deployed as an AWS Lambda Funtion. We should release it in all different
# regions worldwide in other to reduce latency and have a short response time all around the globe.
# See the architectural diagram on README.md file.
# I'd recommend using Terraform together with Zappa or AWS SAM for the release.
# Zappa:
#  - https://github.com/zappa/Zappa
# AWS SAM:
#  - https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html

# We should be careful with the following things to keep our Lambda Function light and fast to deploy,
# also reducing warmup times:
# 1) Keep less dependencies as possible to make our Lambda .zip file small;
# 2) Use Lambda Layers to make dependencies re-usable and reduce warmup time:
#   - https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html
# 3) Set Lambda provisioned concurrency to reduce warmup time:
#   - https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html


@app.route("/ping/", methods=["GET"])
def ping():
    return f"ok!", 200


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>',  methods=['GET'])
def redirector(path):
    domain_pool_id = request.args.get(DOMAIN_POOL_ID_FIELD)
    if not domain_pool_id:
        abort(400, "Param domain_pool_id not provided in the URL")

    tracking_data = get_tracking_data_from_request(request)
    querystring = clean_querystring(request.query_string.decode())
    uri = f'{path}?{querystring}'
    domain = get_suitable_domain(int(domain_pool_id))
    redirect_url = f"{domain}/{uri}"

    logger.info(f'Saving tracking_data for {redirect_url}: {tracking_data}')
    save_tracking_data(tracking_data)

    logger.info(f'Redirecting to {redirect_url}')
    return redirect(redirect_url, code=302)
