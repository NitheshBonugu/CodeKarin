import json
import base64
import sys

sampleRequestLogin = {
    'request_name' : 'testLoginRequest',
    'user' : 'testUser',
    'request_no' : '1000',
    'request_type' : 'login',
    'username' : 'sampleUsername',
    'password' : 'samplePassword',
    
}
sampleRequestViewClassrooms = {
    'request_name' : 'testViewClassRequest',
    'user' : 'testUser',
    'request_no' : '22',
    'request_type' : 'view_classrooms',
    'testFlag' : '1',
}
sampleRequestViewProblemSetList = {
    'request_name' : 'testViewProblems',
    'user' : 'testUser',
    'request_no' : '31',
    'request_type' : 'view_problems',
    'classroom_id' : 'testClassroomName',
    'problem_set' : 'test-problems',
    'testFlag' : '1'
}
sampleRequestGetProblemSet = {
    'request_name' : 'testGetProblemRequest',
    'user' : 'testUser',
    'request_no' : '33',
    'request_type' : 'get_problem',
    'testFlag' : '1',
    'problem_set' : 'test-problems'
}
sampleGetClassroom = {
    'user' : 'sampleUser',
    'class_name' : 'testClassroomName',
    'request_name' : 'getClassroomUnitTest',
    'request_type' : 'get_classroom',
    'request_no' : '11',
    'testFlag' : '1'
}
sampleGetUser = {
    'user' : 'sampleUser',
    'request_name' : 'getUserUnitTest',
    'request_type' : 'get_user',
    'request_no' : '21',
    'testFlag' : '1',
}
submitCode = {
    'problem_id' : 'test-0',
    'classroom_id' : 'testClassroom',
    'user' : 'testUser',
    'path' : 'tests',
    'body' : 'print("Hello world!");',
    'request_name' : 'testSubmitCode',
    'request_type' : 'submit_code',
    'request_no' : '3',
    'testFlag' : 'local'
}
genericRequest = {
    'request_name' : 'genericRequestTest',
    'request_type' : 'generic_request',
    'request_no' : '1000',
    'user' : 'testUser',
    'testFlag' : 1
}



sampleRequest = sampleRequestLogin
reqList = [sampleRequestLogin, sampleRequestViewClassrooms, sampleRequestViewProblemSetList, sampleRequestGetProblemSet, sampleGetClassroom, sampleGetUser, submitCode, genericRequest]

if len(sys.argv) > 1:
    ReqNum = int(sys.argv[1])
    sampleRequest = reqList[ReqNum-1]
else:
    print('error: missing request number. Allowed requests:')
    print('1: login')
    print('2: view_classrooms')
    print('3: view_problems')
    print('4: get_problem')
    print('5: get_classroom')
    print('6: get_user')
    print('7: submit_code')
    print('8: generic_request')
    exit()



#read inputs, can vary depending on which request is getting called
stringRequest = ''
for element in sampleRequest:
    stringRequest = stringRequest+'&'+str(element)+'='
    for val in sampleRequest[element]:
        stringRequest = stringRequest+str(val)
#chop off extra &
stringRequest = stringRequest[1:len(stringRequest)]
#debug output
#print('\nRequest as string from loop: '+stringRequest)

#base 64 encoding to be more "URL friendly"
#currently aws lambdas dont decode back to original query 
#server-side, it looks like extra data gets appended when passing through the API
#urlRequest = base64.urlsafe_b64encode(stringRequest)

#url for api in us-east-1
#urlToInvoke = 'https://g0dp3rzlwb.execute-api.us-east-1.amazonaws.com/FrontendGatewayTest/requests?'+stringRequest
urlToInvoke = 'https://api.codekarin.com/prod/%7Bproxy+%7D?'+stringRequest

print('\n------\n')
print('URL to call from browser: ')
print(str(urlToInvoke))
print('\n------\n')

