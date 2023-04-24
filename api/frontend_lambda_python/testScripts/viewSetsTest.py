import json
from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned
classEvent = {
    'queryStringParameters' : {
        'user' : 'backend_test_user1',
        'class_name' : 'testClassroomName',
        'request_name' : 'viewProbSetsUnitTest',
        'request_type' : 'view_problems',
        'request_no' : '31',
        'testFlag' : 1,
        'problem_set' : 'test-problems'
    },
    'body' : ''
}

print("Test view_problems event: ")
print(classEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

print("*If testing locally ignore the error from boto3*\n")

response = api(classEvent, context)
print('\nresponse returned from API:')
print(response)

