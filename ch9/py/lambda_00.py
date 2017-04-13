def lambda_handler(event, context):
    # TODO implement
    return 'Hello from Lambda'

# var AWS = require('aws-sdk');
# var s3 = new AWS.S3();

# exports.handler = function(event, context) {
#     //console.log(JSON.stringify(event, null, 2));
#     var s3 = new AWS.S3();
#     var param = {Bucket: 'flow-logs', Key: 'test-lambda-x', Body: 'me me me'};
#     console.log("s3");
#     s3.upload(param, function(err, data) {
#         if (err) console.log(err, err.stack); // an error occurred
#         else console.log(data);           // successful response

#         console.log('actually done!');
#         context.done();
#     });

# };



from __future__ import print_function

import json
import urllib
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print("--- Ras le bol de ces conneries!")
    # print("Received event: " + json.dumps(event, indent=2))
    logger.info('got event {}'.format(event['Records'][0]))
    # logger.error('something went wrong')
    # get info on data that was uploaded to s3
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    print("Key: {0} in {1}".format(key, bucket) )

    return "Key: {0} in {1}".format(key, bucket) 

    # # Get the object from the event and show its content type
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    # try:
    #     response = s3.get_object(Bucket=bucket, Key=key)
    #     print("CONTENT TYPE: " + response['ContentType'])
    #     return response['ContentType']
    # except Exception as e:
    #     print(e)
    #     print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
    #     raise e



