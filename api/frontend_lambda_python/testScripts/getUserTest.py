import json
from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned
classEvent = {
    'queryStringParameters' : {
        'user' : 'sampleUser',
        'request_name' : 'getUserUnitTest',
        'request_type' : 'get_user',
        'request_no' : '21',
        #'request_no' : '4'
        'testFlag' : 1,
    },
    'body' : ''
}

print("Test get_user event: ")
print(classEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

print("*If testing locally ignore the error from boto3*\n")

response = api(classEvent, context)
print('\nresponse returned from API:')
print(response)

