import json
from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned
classEvent = {
  "queryStringParameters": {
    "path":"tests",
    "user":"testUser",
    "problem_id":"test-problems/test-0",
    "classroom_id":"testClassroom",
    #"testFlag":"local",
    "request_no":"4",
    "request_type":"check_build",
    "request_name":"checkCodeTest"
  }
}
#working link as of 3/27: https://api.codekarin.com/prod/%7Bproxy+%7D?path=tests&user=testUser&problem_id=test-0&classroom_id=testClassroom&testFlag=local&request_no=3&request_type=submit_code&request_name=submitCodeTest

print("Test submit_code event: ")
print(classEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

response = api(classEvent, context)
print('\nresponse returned from API:')
print(response)

