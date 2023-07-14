import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dbTable = 'recomendation'
db_obj = boto3.resource('dynamodb')
table = db_obj.Table(dbTable)

routes = '/articles'
get = 'GET'
post = 'POST'
patch = 'PATCH'

# getter method 
def get_articles(domain):
    try:
        response = table.get_item(
            Key = {
                'client_id':domain
            }
            )
        if 'Item' in response:
            return build_response(200, response['Item'])
        else:
            return build_response(404, 'Domain %s not found ' % domain)
    except:
        logger.exception('Unable to connect DB')
        
# insert a row in DB
def push_data(data):
    try:
        table.put_item(Item=data)
        body = {
            'Operation' : 'Insert',
            'Message' : 'Successful',
            'Item' : data
        }
        return build_response(200, body)
    except:
        logger.exception('Unable to push in DB')

# update a row
def update_data(data):
    pass

# the name of this fun should be exactly the same as lambda handler name at aws console
def lambda_handler(event, context):
    logger.info(event)
    
    path = event['path']
    httpMethod = event['httpMethod']
    
    if path == routes:
        if httpMethod == get:
            params = event['queryStringParameters']['client_id']
            print(params)
            response = get_articles(params)
        elif httpMethod == post:
            response = push_data(json.loads(event['body']))
        elif httpMethod == patch:
            response = update_data(json.loads(event['body']))
        else:
            response = build_response(404, 'Invalid httpRequestMethod !')
    else:
        response = build_response(404, 'Not Found !')     
    return response
    
def build_response(status, body=None):
    response = {
        'statusCode' : status,
        'body' : json.dumps(body)
    }
    return response
