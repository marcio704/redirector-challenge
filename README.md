# About this project

Create a performant service that allows for redirecting incoming HTTP traffic to a number of individual hosts/domains, while preserving the URL parameters and structure and maintaining robust logs.

## Architecture
![alt text](https://github.com/marcio704/redirector-challenge/blob/main/redirector.png?raw=true)

## Requirements
 - HTTP request made to the redirect service;
 - An ID of the domain pool is provided to the service in the HTTP request;
 - Redirect service should look up the pool, discover target domains inside of it (for example): `domain-a.xyz, weight 2` `domain-b.xyz, weight 1`;
 - Redirect service should choose a domain and force an HTTP redirect to it, picking `domain-a-xyz` should be twice as likely as `domain-b.xyz` , based on the input weights.
 - Redirect service should maintain queryable logs;
 - Configurability and a wide array of pools must be supported; further configuration options are welcome.

## Non-Functional Requirements
 - Availability — redirect service should be highly available (specific SLAs out of scope) 
 - Performance — The service will be evaluated by its performance; it needs to be as fast as possible (specific criteria are not given in the scope of this task) 
 - Scalability — Must be able to scale to process thousands or tens of thousands of QPS
 - Observability — if the service is down or if it has issues, it needs to generate an alert; all logs must be maintained and available for swift issue resolution

# Running locally

## Django Backend
 - Set home directory as `cd <PROJECT_PATH>`
 - `pipenv install && pipenv shell`
 - `python manage.py runserver`

## Flask redirector service
 - Set home directory as `cd <PROJECT_PATH>/lambda`
 - `pipenv install && pipenv shell`
 - `export FLASK_APP=views FLASK_ENV=development STAGE=local`
 - `flask run`

# Tests
 - `make test`

# Releases
 - Staging: merge your PR to branch `master`, this will trigger the Staging CI pipeline
 - Production: create a tag on latest master commit with prefix `release/`, for instance, `release/v1.0.0`, this will trigger the Production CI pipeline.
