import base64
import logging
import json
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

print('Loading Lambda function')

runtime=boto3.Session().client('sagemaker-runtime')
endpoint_Name='pytorch-inference-2025-04-13-07-44-25-598'

def lambda_handler(event, context):
    
    response=runtime.invoke_endpoint(
        EndpointName=endpoint_Name,
        ContentType="application/json",
        Accept='application/json',
        Body=json.dumps(event)
    )
    
    result=response['Body'].read().decode('utf-8')
    json_object=json.loads(result)
    # body = json_object['body']
    # label = np.argmax(body, 1).item()
    
    return {
        'statusCode': 200,
        'headers' : { 'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*' },
        'type-result':str(type(result)),
        'COntent-Type-In':str(context),
        'body' : json.dumps(json_object)
    }
