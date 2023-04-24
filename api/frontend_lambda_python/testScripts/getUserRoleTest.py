import json
from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned
classEvent = {
    'queryStringParameters' : {
        'user' : 'sampleUser',
        'request_name' : 'getUserRoleUnitTest',
        'request_type' : 'get_user',
        'request_no' : '21',
        'testFlag' : 1,
    },
    'body' : ''
}

print("Test get_user_role event sent to API: ")
print(classEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

print("*If testing locally ignore the error from boto3*\n")

response = api(classEvent, context)
print('\nresponse returned from API:')
print(response)

