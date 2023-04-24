import json
from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned
classEvent = {
    'queryStringParameters' : {
        'user' : 'sampleUser',
        'class_name' : 'testClassroomName',
        'request_name' : 'getProbSetUnitTest',
        'request_type' : 'get_problem',
        'request_no' : '33',
        #'request_no' : '4'
        'testFlag' : 1,
        'problem_set' : 'test-problems'
    },
    'body' : ''
}

print("Test get_problem event: ")
print(classEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

print("*If testing locally ignore the error from boto3*\n")

response = api(classEvent, context)
print('\nresponse returned from API:')
print(response)

