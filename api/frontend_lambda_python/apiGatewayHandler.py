import json
import base64
import boto3


#from cognito import lambda_handler as cog_verify_func
from frontend.backendCaller import get_classroom_list as getClassList
from frontend.backendCaller import get_single_classroom as getClassroom
from frontend.backendCaller import get_problem_set_list as getProbSetList
from frontend.backendCaller import get_problem_data as getProb
from frontend.backendCaller import get_user_data as getUser
from frontend.backendCaller import get_user_role as getUserRole
from frontend.submitCode import submit_code_handler as submit_code
from frontend.submitCode import check_build
from frontend.backendCaller import test_add_build
from frontend.backendCaller import test_classroom
from frontend.backendCaller import test_user
from frontend.backendCaller import test_problems
from frontend.backendCaller import get_problem_grade as getGrade
from frontend.backendCaller import get_contest_leaderboard as getLeaderboard
from frontend.cognitoHandler import login_test as login_test
from frontend.cognitoHandler import check_username as whoami



def lambda_handler(event, context):
    #prod flag when set will disable experimental API features still in testing
    #helps test in AWS environment without disrupting work of other components
    prod = 1

    print('event recieved by API:')
    print(event)
    # Parse out request parameters
    request = event['queryStringParameters']
    user = ''
    if 'user' in request:
        user = request['user']
    request_no = request['request_no']
    request_type = request['request_type']

    # CloudWatch outputs for debugging
    print('user: '+user+' made a request: '+request_type+' with request number: '+str(request_no)+'\n')

    
    #generate black-hole response
    #for testing with the docker version of frontend uncomment the localhost header
    errResponse = {}
    errResponse['statusCode'] = 201
    errResponse['headers'] = {
        "Access-Control-Allow-Headers" : "application/json",
        'Access-Control-Allow-Origin' : 'https://codekarin.com',
        # 'Access-Control-Allow-Origin' : 'http://localhost:60443',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    errResponse['headers']['Content-Type'] = 'application/json'
    errResponse['body'] = "BEGONE"

    
    #TODO associate user's role with list of valid requests
    reqs = ['','login','logout','view_classrooms','get_classroom','view_problems','get_problem','get_problem_set','submit_code','add_problem', 'add_professor', 'add_student', 'add_classroom', 'add_classroom_student', 'add_problem_set', 'view_problem_sets']
    
    # check db for role associated with a user
    if 'testFlag' in request and 'user' in request and not prod:
        # assuming since the user exists in cognito and passed the authorizer they exist in the user table
        getRoleResponse = getUserRole(event, context)
        userScope = getRoleResponse['user_group']
        print('found user: '+user+' to have role: '+userScope)
        
    

    #change call to backend on request number
    #TODO secondary check against a user's role
    print('forwarding request to backendCaller')
    reqNum = int(request_no)
    if reqNum == 1000:
        #print("disabled during demo")
        ret = login_test(event, context)
    elif reqNum == 1:
        ret = whoami(event, context)
    elif reqNum == 3:
        ret = submit_code(event, context)
    elif reqNum == 4:
        ret = check_build(event, context)
    elif reqNum == 10:
        ret = 'add_class request disabled'
    elif reqNum == 11:
        ret = getClassroom(event, context)
    elif reqNum == 12:
        ret = 'delete_classroom request disabled'
    elif reqNum == 20:
        ret = 'add_user request disabled'
    elif reqNum == 21:
        ret = getUser(event, context)
    elif reqNum == 22:
        ret = 'delete_user request disabled'
    elif reqNum == 23:
        ret = 'add_user_list request disabled'
    elif reqNum == 24:
        ret = 'delete_user_list disabled'
    elif reqNum == 25:
        ret = 'get_user_list DEPRECATED'
    elif reqNum == 30:
        ret = 'add_problem_set disabled'
    elif reqNum == 31:
        ret = getProbSetList(event, context)
    elif reqNum == 32:
        ret = 'delete_problem_set disabled'
    elif reqNum == 33:
        ret = getProb(event, context)
    elif reqNum == 43:
        ret = getGrade(event, context)
    elif reqNum == 44:
        ret = getLeaderboard(event, context)
    elif reqNum == 103:
        ret = test_add_build(event, context)
    elif reqNum == 110:
        ret = test_classroom(event, context)
    elif reqNum == 120:
        ret = test_user(event, context)
    elif reqNum == 130:
        ret = test_problems(event, context)


    #for testing with the docker version of frontend uncomment the localhost header
    return {
        'statusCode' : 200,
        'headers' : {
            "Access-Control-Allow-Headers" : "application/json",
            'Access-Control-Allow-Origin' : 'https://codekarin.com',
            # 'Access-Control-Allow-Origin' : 'http://localhost:60443',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body' : json.dumps(ret)
    }
