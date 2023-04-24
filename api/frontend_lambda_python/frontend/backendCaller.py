import datetime
import json
import boto3
import os

#from submitCode import submit_code_handler

def get_classroom_list(event, context):
    request = event['queryStringParameters']
    request_type = request['request_type']
    user = request['user']

    if request_type == "view_classrooms":
        if 'testFlag' in request:
            print('testing view_classrooms function...')
            testResponse = {
                'statusCode' : 200,
                'body' : {
                    'classrooms' : [
                        {
                            'classroom_name' : 'testClassroom',
                            'prof_name' : 'testProf',
                            'end_date' : '05-31-2022'
                        },

                        {
                            'classroom_name' : 'testClassroom2',
                            'prof_name' : 'testProf2',
                            'end_date' : '05-31-2023'
                        },

                        {
                            'classroom_name' : 'testClassroom3',
                            'prof_name' : 'testProf3',
                            'end_date' : '05-31-2024'
                        }
                    ]
                }
            }
            return testResponse    
        else:
            client = boto3.client('lambda')
            backendInput = request #forward request to backend
            print("forwarded view_classrooms request to backend for query")
            print(backendInput)
            backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendInput))
            print('backend response:')
            print(backendResponse)
            print('called backend handler')
            backendJson = json.loads(backendResponse['Payload'].read())
            print('backend JSON body:')
            print(backendJson)
            ret = {
                'statusCode': 200,
                'body' : {
                    'classrooms' : ''
                }
            }

            backend_classroom_list = backendJson['classroom_get_response']
            #formatted_classrooms = {[]}
            ret_list = []
            tmp_obj = {}
            for i in backend_classroom_list:
                tmp_obj['classroom_name'] = backend_classroom_list[i]['classroom_id']
                ret_list.append(tmp_obj)
            

            ret['body']['classrooms'] = ret_list
            return ret

def get_single_classroom(event, context):
    request = event['queryStringParameters']
    request_type = request['request_type']
    if request_type == "get_classroom":
        if 'testFlag' in request:
            print('testing getClassroom function...')
            testResponse = {
                'class_name' : 'testGetClassName',
                'prof_name' : 'testGetClassProfName',
                'end_date' : 'N/A',
                'student_list' : [
                    'sampleStudent',
                    'sampleStudent2',
                    'sampleStudent3'
                ],
                'prob_set_list' : [
                    'sampleProbSet',
                    'sampleProbSet2',
                    'sampleProbSet3'
                ]
            }
            return testResponse    
        else:
            client = boto3.client('lambda')
            print("forwarded getClass request to backend for query")
            cal = {
              "request_no": 11,
              "user_id" : request['user'],
              "cid_to_get":request['class_name']
            }

            backendClassResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(cal))
            print('backend response:')
            print(backendClassResponse)
            backendClassJson = json.loads(backendClassResponse['Payload'].read())
            print('backend JSON body from get_user:')
            print(backendClassJson)
            probinfolist = []
            templist = json.loads(backendClassJson['body'])
            print('templist to iterate:')
            print(templist['classroom_get_response']['problems'])
            print(templist['classroom_get_response']['contests'])
            iteratelist = {}
            if request['set_type'] == 'contest':
                iteratelist = templist['classroom_get_response']['contests']
                print('Iterating over contest list:')
                print(iteratelist)
            else:
                iteratelist = templist['classroom_get_response']['problems']
                print("Iterating over practice list:")
                print(iteratelist)
            for name in iteratelist:
                setrequest = {
                    "problem_set" : name,
                    "request_no" : 31,
                    "user_id" : request['user']
                }
                backendSetResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(setrequest))
                print('Backend get_set response:')
                print(backendSetResponse)
                backendSetJson = json.loads(backendSetResponse['Payload'].read())
                print('get_set payload read in frontend:')
                print(backendSetJson)
                tempbody = json.loads(backendSetJson['body'])
                cleanbody = {}
                print(tempbody['problem_set_get_response'])
                if len(tempbody['problem_set_get_response']) == 0:
                    return {
                        'statusCode' : 500,
                        'body' : 'length of problem set 0'
                    }
                cleanbody['num_probs'] = len(tempbody['problem_set_get_response'])
                cleanbody['set_name'] = name
                cleanbody['end_date'] = tempbody['problem_set_get_response'][0]['end_date']
                cleanbody['problem_list'] = tempbody['problem_set_get_response']
                probinfolist.append(cleanbody)
            if request['set_type'] == 'contest':
                templist['classroom_get_response']['prob_set_list'] = probinfolist
            else:
                templist['classroom_get_response']['prob_set_list'] = probinfolist
            
            return templist['classroom_get_response']

def get_problem_set_list(event, context):
    print('Get problem set list has been called')
    print('event recieved: ')
    print(event)
    request = event['queryStringParameters']
    request_type = request['request_type']
    if request_type == "view_problems":
        if 'testFlag' in request:
            print('test flag found')
            testResponse = {
                'class_name' : 'testClassName',
                'prof_name' : 'testProfName',
                'prob_set_list' : [
                    {
                    'set_name': 'pSet1',
                    'problem_name' : 'testProblemSet',
                    'end_date' : '06-30-2024',
                    'num_probs' : '8'
                    },
                    {
                    'set_name': 'pSet2',
                    'end_date' : '05-30-2025',
                    'num_probs' : '7'
                    },
                    {
                    'set_name': 'pSet3',
                    'end_date' : '07-20-2029',
                    'num_probs' : '4'
                    }
                ]
            }
            
            print('JSON payload to be passed to backend: ')
            print(event)
            print()
            return testResponse
        else:
            #TODO testbackend response
            client = boto3.client('lambda')
            print("forwarded getProblem request to backend for query")
            #TODO testbackend response
            client = boto3.client('lambda')
            print("forwarded getProblem request to backend for query")
            backendRequest = {
                "user_id" : request['user'],
                "problem_set" : request['problem_set'],
                "request_no" : 31
            }
            backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendRequest))
            print('backend response:')
            print(backendResponse)
            backendJson = json.loads(backendResponse['Payload'].read())
            print('backend JSON body:')
            tempbody = json.loads(backendJson['body'])
            returnList = []
            print(tempbody['problem_set_get_response'])
            #return tempbody['problem_set_get_response']
            for prob in tempbody['problem_set_get_response']:
                name = prob['problem_name']
                probRequest = {
                    "user_id" : request['user'],
                    "problem_id" : request['problem_set'] +'/'+ name,
                    "request_no" : 33
                }
                probResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(probRequest))
                print('backend response:')
                print(probResponse)
                probJson = json.loads(probResponse['Payload'].read())
                print('backend JSON body:')
                print(probJson)
                probbody = json.loads(probJson['body'])
                print('problem body')
                print(probbody['problem_get_response'])
                cleanresponse = {
                    'prob_name' : probRequest['problem_id'],
                    'description' : probbody['problem_get_response']['description']['description']
                }
                returnList.append(cleanresponse)
            return returnList

def get_problem_data(event, context):
    print('Get problem data has been called')
    print('event recieved: ')
    print(event)
    request = event['queryStringParameters']
    request_type = request['request_type']
    if request_type == "get_problem":
        #call back
        if 'testFlag' in request:
            testResponse = {
                'problems' : [
                    {
                    'prob_no' : '1',
                    'description' : 'print "hello world" to the console in java',
                    'tests' : [
                        'testCase1',
                        'testCase2',
                        'testCase3'
                    ],
                    'hints' : [
                        'hint1',
                        'hint2',
                        'hint3'
                    ],
                    "boilerplate": "package main;\npublic class Adder{\n\tpublic int add(int a, int b){\n\t/* your code goes here */\n\t}\n}"
                    },
                    {
                    'prob_no' : '2',
                    'description' : 'print "hello world 2" to the console in java',
                    'tests' : [
                        'testCase1',
                        'testCase2',
                        'testCase3'
                    ],
                    'hints' : [
                        'hint1',
                        'hint2',
                        'hint3'
                    ],
                    "boilerplate": "package main;\npublic class Adder{\n\tpublic int add(int a, int b){\n\t/* your code goes here */\n\t}\n}"
                    },
                    {
                    'prob_no' : '3',
                    'description' : 'print "hello world 3" to the console in java',
                    'tests' : [
                        'testCase1',
                        'testCase2',
                        'testCase3'
                    ],
                    'hints' : [
                        'hint1',
                        'hint2',
                        'hint3'
                    ],
                    "boilerplate": "package main;\npublic class Adder{\n\tpublic int add(int a, int b){\n\t/* your code goes here */\n\t}\n}"
                    }
                ]
            }
            return testResponse
        else:
            #TODO testbackend response
            client = boto3.client('lambda')
            print("forwarded getProblem request to backend for query")
            backendRequest = {
                "user_id" : request['user'],
                "problem_id" : request['problem_id'],
                "request_no" : 33
            }
            probResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendRequest))
            print('backend response:')
            print(probResponse)
            probJson = json.loads(probResponse['Payload'].read())
            print('backend JSON body:')
            print(probJson['body'])
            probbody = json.loads(probJson['body'])
            print('problem body')
            print(probbody['problem_get_response'])
            cleanresponse = {
                'problem_name' : backendRequest['problem_id'],
                'problem_get_response' : probbody['problem_get_response']
            }
            return cleanresponse
        
def add_problem_to_set(event, context):
    request = event['queryStringParameters']
    request_type = request['request_type']
    if request_type == "add_problem":
        #TODO double check user is part of professor group before sending to addProblemFunction
        
        if 'testFlag' in request:
            print("Something should go here eventually")
            return {
                'statusCode' : 200,
                'body' : 'How do i make dummy data for an add function?'
            }
        else:
            #TODO testbackend response
            client = boto3.client('lambda')
            print("forwarded addProblem request to backend for query")
            backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(request))
            print('backend response:')
            print(backendResponse)
            backendJson = json.loads(backendResponse['Payload'].read())
            print('backend JSON body:')
            print(backendJson)
            print('called backend handler')
            return {
                'statusCode' : 200,
                'body' : backendJson
            }

def get_user_role(event, context):
    request = event['queryStringParameters']
    if 'testFlag' in request:
        print('showing test data for get_user_role request')
        testResponse = {
            'user_group' : 'test-student'
        }
        return testResponse
    client = boto3.client('lambda')
    print("forwarded getUser request to backend for query, non-recursive")
    cal = {
        "request_no": 21,
        "user_id":request['user'],
        "uid_to_get":request['user']
    }
    backendUserResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(cal))
    print('backend response:')
    print(backendUserResponse)
    backendUserJson = json.loads(backendUserResponse['Payload'].read())
    print('backend JSON body from get_user:')
    print(backendUserJson)
    templist = json.loads(backendUserJson['body'])
    print(templist['user_get_response']['user_group'])
    group = templist['user_get_response']['user_group']
    return group


def get_user_data(event, context):
    request = event['queryStringParameters']
    request_type = request['request_type']
    if request_type == "get_user":
        if 'testFlag' in request:
            print('showing test data for get_user request')
            testResponse = {
                'statusCode' : 200,
                'body' : {
                    'classrooms' : [
                        {
                            'classroom_name' : 'testClassroom',
                            'prof_name' : 'testProf',
                            'end_date' : '05-31-2022'
                        },

                        {
                            'classroom_name' : 'testClassroom2',
                            'prof_name' : 'testProf2',
                            'end_date' : '05-31-2023'
                        },

                        {
                            'classroom_name' : 'testClassroom3',
                            'prof_name' : 'testProf3',
                            'end_date' : '05-31-2024'
                        }
                    ]
                }
            }
            return testResponse
        else:
            client = boto3.client('lambda')
            print("forwarded getUser request to backend for query")
            cal = {
              "request_no": 21,
              "user_id":request['user'],
              "uid_to_get":request['user']
            }

            backendUserResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(cal))
            print('backend response:')
            print(backendUserResponse)
            backendUserJson = json.loads(backendUserResponse['Payload'].read())
            print('backend JSON body from get_user:')
            print(backendUserJson)
            classinfolist = []
            templist = json.loads(backendUserJson['body'])
            print('templist to iterate:')
            print(templist['user_get_response']['classrooms'])
            for name in templist['user_get_response']['classrooms']:
                classrequest = {
                    "cid_to_get" : name,
                    "request_no" : 11,
                    "user_id" : templist['user_get_response']['user_id']
                }
                backendClassResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(classrequest))
                print('Backend get_class response:')
                print(backendClassResponse)
                backendClassJson = json.loads(backendClassResponse['Payload'].read())
                print('get_class payload read in frontend:')
                print(backendClassJson['body'])
                tempbody = json.loads(backendClassJson['body'])
                print(tempbody['classroom_get_response'])
                classinfolist.append(tempbody['classroom_get_response'])
            templist['user_get_response']['classrooms'] = classinfolist
            return templist
            
                
                
            
def submit_code(event, context):
    #scrape params
    request = event['queryStringParameters']
    #append body
    request['body'] = event['body']
    if 'testFlag' in request:
        codeResponse = submit_code_handler(request, context)
        return codeResponse
    else:
        return {
        'statusCode' : 200,
        'body' : 'submit_code needs testFlag'
        }
        
def test_add_build(event, context):
    client = boto3.client('lambda')
    print("forwarded getUser request to backend for query")
    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(event))
    print('backend response:')
    print(backendResponse)
    backendJson = json.loads(backendResponse['Payload'].read())
    print('backend JSON body:')
    print(backendJson)
    print('called backend handler')
    return {
        'statusCode' : 200,
        'body' : backendJson
    }
def test_user(event, context):
    client = boto3.client('lambda')
    print("forwarded getUser request to backend for query")
    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(event))
    print('backend response:')
    print(backendResponse)
    backendJson = json.loads(backendResponse['Payload'].read())
    print('backend JSON body:')
    print(backendJson)
    print('called backend handler')
    return {
        'statusCode' : 200,
        'body' : backendJson
    }
def test_problems(event, context):
    client = boto3.client('lambda')
    print("forwarded getUser request to backend for query")
    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(event))
    print('backend response:')
    print(backendResponse)
    backendJson = json.loads(backendResponse['Payload'].read())
    print('backend JSON body:')
    print(backendJson)
    print('called backend handler')
    return {
        'statusCode' : 200,
        'body' : backendJson
    }
def test_classroom(event, context):
    client = boto3.client('lambda')
    print("forwarded getUser request to backend for query")
    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(event))
    print('backend response:')
    print(backendResponse)
    backendJson = json.loads(backendResponse['Payload'].read())
    print('backend JSON body:')
    print(backendJson)
    print('called backend handler')
    return {
        'statusCode' : 200,
        'body' : backendJson
    }
def get_problem_grade(event, context):
    request = event['queryStringParameters']
    client = boto3.client('lambda')
    print("forwarded grade request to backendCaller")
    #cal = {
    #  "request_no": 21,
    #  "professor_id"
    #  "user_id":request['user'],
    #  "classroom_id":request['classroom_id']
    #}
    user_id = request['user']
    class_id = request['classroom_id']
    
    classrequest = {
        "cid_to_get" : class_id,
        "request_no" : 11,
        "user_id" : user_id
    }
    print("calling backend get_classroom_by_id with request:")
    print(classrequest)
    backendClassResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(classrequest))
    print('Backend get_class response:')
    print(backendClassResponse)
    backendClassJson = json.loads(backendClassResponse['Payload'].read())
    print('get_class payload read in frontend:')
    print(backendClassJson['body'])
    tempbody = json.loads(backendClassJson['body'])
    print(tempbody['classroom_get_response'])
    userlist = tempbody['classroom_get_response']['students']
    
    #take request no 43, prof_id, user_id, classroom_id and send to backend for classroom
    #call get_classroom from backend
    #for each user in class call request 43, build a list of usernames and grades and send list to frontend
    
    gradelist = []
    for student in userlist:
        cal = {
          "request_no": 43,
          "professor_id" : tempbody['classroom_get_response']['professor_id'],
          "user_id" : student,
          "classroom_id" : class_id
        }
        print('Calling to backend with student name:')
        print(cal['user_id'])
        backendGradeResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(cal))
        backendGradeJson = json.loads(backendGradeResponse['Payload'].read())
        print('backend grade response:')
        print(json.loads(backendGradeJson['body'])['grade_list_get_response'])
        grade = json.loads(backendGradeJson['body'])['grade_list_get_response']
        graderesponse = {}
        graderesponse['user_id'] = grade['user_id']
        graderesponse['grade_aggregate'] = int(grade['grade_aggregate'])
        gradelist.append(graderesponse)
        
        
    print("The list before sorting:")
    print(gradelist)
    print ("The list printed sorted by grade aggregate: ")
    #print(sorted(gradelist, key=grade_aggregate))
    gradelist.sort(reverse=True, key = lambda x:x["grade_aggregate"])
    print(gradelist)
    #print(gradelist.sort(key = lambda x:x['grade_aggregate']))
    return gradelist





def get_contest_leaderboard(event, context):
    request = event['queryStringParameters']
    client = boto3.client('lambda')
    print("forwarded grade request to backendCaller")
    #cal = {
    #  "request_no": 21,
    #  "professor_id"
    #  "user_id":request['user'],
    #  "classroom_id":request['classroom_id']
    #}
    user_id = request['user']
    class_id = request['classroom_id']
    prob_set = request['problem_set']
    #prob_set = prob_set[0:prob_set.index('/')]
    #print(prob_set)

    classrequest = {
        "cid_to_get" : class_id,
        "request_no" : 11,
        "user_id" : user_id,
    }
    print("calling backend get_classroom_by_id with request:")
    print(classrequest)
    backendClassResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(classrequest))
    print('Backend get_class response:')
    print(backendClassResponse)
    backendClassJson = json.loads(backendClassResponse['Payload'].read())
    print('get_class payload read in frontend:')
    print(backendClassJson['body'])
    tempbody = json.loads(backendClassJson['body'])
    print(tempbody['classroom_get_response'])
    userlist = tempbody['classroom_get_response']['students']
    
    #remove problems from the leaderboard if it is not part of the contest's problem set
    #sort the finalized list be time before returning
    
    gradelist = []
    for student in userlist:
        cal = {
          "request_no": 44,
          "professor_id" : tempbody['classroom_get_response']['professor_id'],
          "user_id" : student,
          "classroom_id" : class_id,
          "problem_set" : prob_set
        }
        print('Calling to backend with student name:')
        print(cal['user_id'])
        backendGradeResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(cal))
        backendGradeJson = json.loads(backendGradeResponse['Payload'].read())
        print('backend grade response:')
        print(backendGradeJson)
        print(json.loads(backendGradeJson['body'])['grade_list_get_response'])
        grade = json.loads(backendGradeJson['body'])['grade_list_get_response']
        graderesponse = {}
        if grade['problem_set'] == request['problem_set'] and grade['user_id'] == student:
            graderesponse['user_id'] = grade['user_id']
            graderesponse['grade_aggregate'] = int(grade['grade_aggregate'])
            graderesponse['run_time'] = grade['run_time']
            if type(grade['start_time']) == None:
                graderesponse['start_time'] = 'DNF'
            else:
                graderesponse['start_time'] = grade['start_time']
            if type(grade['end_time']) == None:
                graderesponse['end_time'] = 'DNF'
            else: 
                graderesponse['end_time'] = grade['end_time']
            #graderesponse['finished'] = grade['finished']
        gradelist.append(graderesponse)
    
    # using sorted and lambda to print list sorted
    # by age
    #print ("The list printed sorted by time: ")
    #print (sorted(gradelist, key=getDateValue))
    
    
    #Fill in missing start_times
    #for grade in gradelist:
    #    grade['start_time'] = datetime.datetime.strftime(grade['start_time'], "%m/%d/%Y, %H:%M:%S")
    
    print("The list before sorting:")
    print(gradelist)
    print ("The list printed sorted by grade aggregate: ")
    gradelist.sort(reverse=True, key = lambda x:x["grade_aggregate"])
    print(gradelist)
    return gradelist
    
    
def getDateValue(x):
    max_date = datetime.datetime.max
    if(x['start_time'] == None):
        x['start_time'] = max_date
        #return x
        return max_date
    start = datetime.datetime.strptime(x['start_time'], "%m/%d/%Y, %H:%M:%S") or max_date
    #x['start_time'] = datetime.datetime.strftime(start, "%m/%d/%Y, %H:%M:%S")
    x['start_time'] = start
    return x['start_time']
    #return datetime.datetime.strptime(x['start_time'], "%m/%d/%Y, %H:%M:%S") or max_date
    