import re
import time
import json
import boto3
import string
import datetime

from backend.codebuild_handler import assemble_build as assembly_handler
from backend.codebuild_handler import execute_build as exec_handler
from backend.codebuild_handler import clean_build as clean_handler
from backend.codebuild_handler import add_build as add_build

from backend.problem_handler import lambda_handler as problem_handler
from backend.user_handler import lambda_handler as user_handler
from backend.class_handler import lambda_handler as classroom_handler
from backend.grades_handler import lambda_handler as grades_handler

# load codebuild client
cb_client = boto3.client('codebuild')
# load s3 client
sss_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
dynamo_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    ''' this lambda_handler implements a workflow for the Karin Virtual Classroom Codebuild testing framework '''
    
    response = event
    
    print(event)
    
    if 'Records' in event:
       response = s3_interface(event, context)
    
    else:
        req = event['request_no']
        
        if 'statusCode' in response:
            event = response['body']
    
    # codebuild interfaces
        if req == 0:
            response = assembly_interface(event, context)    
        elif req == 1:
            response = exec_handler(event, context)
        elif req == 2:
            response = clean_handler(event, context)
        elif req == 3:
            response = add_build_interface(event, context)
        
        
    # class interfaces
        elif req == 10:
            # add class
            response = classroom_handler(event, context)
        elif req == 11:
            # get class by id
            response = classroom_handler(event, context)
        elif req == 12:
            # delete class by id
            response = classroom_handler(event, context)


    # user interfaces
        elif req == 20:
            # add user
            response = user_handler(event, context)
        elif req == 21:
            # get user
            response = user_handler(event, context)
        elif req == 22:
            # delete user
            resource = user_handler(event, context)
        elif req == 23:
            # add user list
            resource = user_handler(event, context)
        elif req == 24:
            # delete user list
            resource = user_handler(event, context)
        elif req == 25:
            # get user list
            resource = user_handler(event, context)


    # problem interfaces
        elif req == 30:
            # add problems
            response = problem_handler(event, context)
        elif req == 31:
            # get problems
            response = problem_handler(event, context)
        elif req == 32:
            # delete problems
            response = problem_handler(event, context)
        elif req == 33:
            # get problem by id
            response = problem_handler(event, context)
            
    # grade interfaces
        elif req == 40:
            # add grade
            response = grades_handler(event, context)
        elif req == 41:
            # get grade by id
            response = grades_handler(event, context)
        elif req == 42:
            # delete grade by id
            response = grades_handler(event, context)
        elif req == 43:
            # get grade list
            response = grades_handler(event, context)
        elif  req == 44:
            response = grades_handler(event, context)
            

# tests (test number = 100 + prev req number)
        elif req == 103:
            response = test_add_build(event, context)
        elif req == 110:
            response = test_classroom(event, context)
        elif req == 120:
            response = test_user(event, context)
        elif req == 130:
            response = test_problems(event, context)
            
        else:
            return{
                'statusCode': 404,
                'body': 'request does not exist',
                'event': event
            }
            
        return {
            'statusCode': 200,
            'body': json.dumps(response, default=str)
        }


def s3_interface(event, context):
     for record in event['Records']:
        filename = record['s3']['object']['key']
        if('out/main.Tester.txt' in record['s3']['object']['key']):
            event.pop('Records')
            event['request_no'] = 3
            event['status'] = 'COMPLETE'
            filepath = record['s3']['object']['key'].split('/')
            event['user_id'] = filepath[0]
            event['problem_id'] = filepath[1] + '/' + filepath[2]
            event['user_type'] = 'student'
            event['problem_name'] = filepath[1] + '/' + filepath[2]
            event['build_id'] = event['user_id'] + '/' + event['problem_id']
            obj = s3_resource.Object('karin-output-staging-bucket', record['s3']['object']['key'])
            data = obj.get()['Body'].read()
            loaded_string = str(data)
            event['build_body'] = data
            response = lambda_handler(event, context)
            
            time_filename = record['s3']['object']['key'].replace("out/main.Tester.txt", "lambda_exec_output/exec_response.json")
            obj = s3_resource.Object('karin-output-staging-bucket', time_filename)
            loaded_time = json.loads(obj.get()['Body'].read())['start_time']
            start_time = datetime.datetime.strptime(str(loaded_time), "%m/%d/%Y, %H:%M:%S")
            
            grade = 0
        # call grades interface
            if('-----' in loaded_string):
                tmp = loaded_string
                list_to_remove = string.punctuation + string.ascii_letters  + ' '
                list_to_remove = list_to_remove.replace(',', '')
                list_to_remove = list_to_remove.replace('.', '')
                tmp = tmp.translate({ord(i): None for i in list_to_remove})
                tmp = tmp[1:-1]
                print(tmp)
                grade_list = tmp.split(',')
                grade = int(grade_list[0]) - int(grade_list[1]) - int(grade_list[2]) - int(grade_list[3])
                time = str(grade_list[4])
            
            event['request_no'] = 33
            print(event)
            get_problem_response = lambda_handler(event, context)
            print(get_problem_response)
            lod = json.loads(get_problem_response['body'])
            print(lod)
            event['end_time'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            event['grade'] = grade
            event['student_id'] = event['user_id']
            event['classroom_id'] = lod['problem_get_response']['class_id']
            event['professor_id'] = lod['problem_get_response']['professor_id']
            event['start_time'] = start_time
            event['run_time'] = time
            event['request_no'] = 40
            response = lambda_handler(event, context)
            return {
                'statusCode': 200,
                'body': response
            }

def assembly_interface(event, context):
    response = assembly_handler(event, context)
    body = response['body']
    obj = s3_resource.Object('karin-longterm-storage-bucket', body['s3_input_path'] + "/description.json")
    data = obj.get()['Body'].read().decode('utf-8')
    json_content = json.loads(data)
    body['build_body'] = json.dumps(json_content)
    if(response['statusCode'] == 200):
        body['request_no'] = 3
        body['status'] = 'IN_PROGRESS'
        response = lambda_handler(body, context)
    else:
        body['request_no'] = 3
        body['status'] = 'NOT_STARTED'
        response = lambda_handler(body, context)

    return response

def add_build_interface(event, context):
    status = event['status']
    response = add_build(event, context)
    if(response['statusCode'] == 200):
        if 'status' in response['body']:
            body = response['body']
            status = body['status']
            if status == "NOT_STARTED":
                if("{" in body['build_body']):
                    return{
                        "statusCode": 404,
                        "body": body
                    }
                else:
                    body['request_no'] = 0
                    response = lambda_handler(body, context)
                
            elif status == "IN_PROGRESS":
                body['request_no'] = 1
                response = lambda_handler(body, context)
                
            elif status == "COMPLETE" or status =="CHECK":
                if(status == "CHECK"):
                    return {
                        'statusCode': 200,
                        'body': {
                            'body': body['body'],
                            'status': body['ret_stats']
                        }
                    }
                return {
                    'statusCode': 200,
                    'body': body
                }
                
            elif body['status'] == "READ":
                body['request_no'] = 2
                response = lambda_handler(body, context)
    
    else:
        return {
            'statusCode': 500,
            'body': response
        }
    return response

def test_add_build(event, context):
    user_id = "backend_test_user1"
    problem_id = "test-problems/test-0"
    problem_name = "test-problems/test-0"
    user_type = "student"
    build_body = ""
    input_bucket = "karin-web-staging-bucket"
    
    not_started_event={
        'user_id': user_id,
        'problem_id': problem_id,
        'build_type': user_type,
        'user_type': user_type,
        'problem_name': problem_name,
        'build_body': build_body,
        'input_bucket': input_bucket,
        'status': "NOT_STARTED"
    }
    response = add_build(not_started_event, context)
    
    if not (response['statusCode'] == 200):
        return {
            'statusCode': 500,
            'body': json.dumps(response)
        } 


def test_classroom(event, context):
    class_test_response = []
    
    add_class = {
      "request_no": 10,
      "user_id": "backend_test_user1",
      "new_class_id":"backend_test_user1--class1",
      "end_date":"04-22-2022",
      "problem_sets":["test-problems"],
      "contest_sets":["test-problems"],
      "students":["backend_test_user2"]
    }
    response = classroom_handler(add_class, context)
    class_test_response.append(response)

    get_class = {
      "request_no": 11,
      "user_id": "backend_test_user1",
      "cid_to_get": "backend_test_user1--class1"
    }
    response = classroom_handler(get_class, context)
    class_test_response.append(response)
    
    delete_class = {
      "request_no": 12,
      "user_id":"backend_test_user1",
      "del_class_id":"backend_test_user1--class1"
    }
    response = classroom_handler(delete_class, context)
    class_test_response.append(response)
    
    return{
        "statusCode":200,
        "class_test_response":class_test_response
    }
    
def test_user(event, context):
    user_test_response = []
    # bootstrap admin user
    add_user = {
      "request_no": 20,
      "user_id":"backend_test_user1",
      "new_user_id":"backend_test_user1",
      "new_user_classrooms": ["backend_test_user1--class1", "backend_test_user1--class2"],
      "new_user_group":"admin",
      "new_user_email":"example@gmail.com",
      "is_test": True
    }
    response = user_handler(add_user, context)
    user_test_response.append(response)
    
    # create user individual
    add_user = {
      "request_no": 20,
      "user_id":"backend_test_user1",
      "new_user_id":"backend_test_user2",
      "new_user_classrooms": ["backend_test_user1--class1", "backend_test_user1--class2"],
      "new_user_group":"professor",
      "new_user_email":"example@gmail.com",
      "is_test": True
    }
    response = user_handler(add_user, context)
    user_test_response.append(response)
    
    # create user list
    add_user_list = {
      "request_no": 23,
      "user_id":"user1",
      "new_users":[
        {
          "new_user_id":"backend_test_user3",
          "new_user_classrooms": ["class1", "class2"],
          "new_user_group":"student",
          "new_user_email": "example2@gmail.com",
          "is_test" : True
        },
        {
          "new_user_id":"backend_test_user4",
          "new_user_classrooms": ["class1", "class2"],
          "new_user_group":"student",
          "new_user_email": "example3@gmail.com",
          "is_test" : True
        },
        {
          "new_user_id":"backend_test_user5",
          "new_user_classrooms": ["class1", "class2"],
          "new_user_group":"student",
          "new_user_email": "example4@gmail.com",
          "is_test" : True
        }
      ]
    }
    response = user_handler(add_user_list, context)
    user_test_response.append(response)
    
    # get user individual
    get_user = {
      "request_no": 21,
      "user_id":"backend_test_user1",
      "uid_to_get":"backend_test_user1"
    }
    response = user_handler(get_user, context)
    user_test_response.append(response)
    
    get_user_list = {
        "request_no": 25,
        "user_id":"backend_test_user1",
        "uids_to_get": ["backend_test_user2", "backend_test_user3", "backend_test_user4", "backend_test_user5"]
    }
    response = user_handler(get_user_list, context)
    user_test_response.append(response)
    
    # delete user individual
    delete_user = {
      "request_no": 22,
      "user_id":"backend_test_user1",
      "del_user_id":"backend_test_user2",
      "del_cog_id":"example_tmp"
    }
    response = user_handler(delete_user, context)
    user_test_response.append(response)
    
    # delete user list
    delete_user_list = {
      "request_no": 24,
      "user_id":"user1",
      "del_users":[
        {
          "del_user_id":"backend_test_user3",
          "del_cog_id":"example_tmp"
        },
        {
          "del_user_id":"backend_test_user4",
          "del_cog_id":"example_tmp"
        },
        {
          "del_user_id":"backend_test_user5",
          "del_cog_id":"example_tmp"
        }
      ]
    }
    response = user_handler(delete_user_list, context)
    user_test_response.append(response)
    
    # delete bootstrap user
    delete_user = {
      "request_no": 22,
      "user_id":"backend_test_user1",
      "del_user_id":"backend_test_user1",
      "del_cog_id":"example_tmp"
    }
    response = user_handler(delete_user, context)
    user_test_response.append(response)
    
    return{
        "statusCode":200,
        "user_test_response":user_test_response
    }
    
    
def test_problems(event, context):
    problems_test_response = []
    add_problem_set = {
      "request_no": 30,
      "user_id":"backend_test_user1",
      "problem_set": "test-problems"
    }
    response = problem_handler(add_problem_set, context)
    problems_test_response.append(response)
    
    get_problem_set = {
      "request_no": 31,
      "user_id":"backend_test_user1",
      "problem_set":"test-problems"
    }
    response = problem_handler(get_problem_set, context)
    problems_test_response.append(response)
    
    delete_problem_set = {
      "request_no": 32,
      "user_id": "backend_test_user1",
      "problem_set": "test-problems"
    }
    response = problem_handler(delete_problem_set, context)
    problems_test_response.append(response)
    
    return{
        "statusCode":200,
        "problems_test_response":problems_test_response
    }