import json
from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned
classEvent = {
    'queryStringParameters' : {
        'user' : 'sampleUser',
        'class_name' : 'testClassroomName',
        'request_name' : 'getClassroomUnitTest',
        'request_type' : 'get_classroom',
        'request_no' : '11',
        'testFlag' : 1,
    },
    'body' : ''
}

print("Test get_classroom event: ")
print(classEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

print("*If testing locally ignore the error from boto3*\n")

response = api(classEvent, context)
print('\nresponse returned from API:')
print(response)

