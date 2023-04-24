import os
import json
import boto3
from boto3.dynamodb.conditions import Key

def submit_code_handler(event, context):
    #scrape params
    request = event['queryStringParameters']
    print(request)
    request_type = request['request_type']
    #append body
    request['body'] = event['body']
    
    client = boto3.client('lambda')
    #paste of code from backendCaller
    pid = request['problem_id']
    cid = request['classroom_id']
    user = request['user']
    code = json.loads(request['body'])['code']
    buildExists = 0
    key = user +'/'+pid+'/main/java/Code.java'
    #prep s3 bucket
    #disabled until permission updated

    print('Sending code to s3:')
    s3 = boto3.resource('s3')
    object = s3.Object('karin-web-staging-bucket', key)
    object.put(Body=code, Bucket='karin-web-staging-bucket', Key=key)
    
    backendInput = {
        'request_no' : 3,
        'build_id' : user+'/'+pid,
        'build_body' : '',
        'user_id' : user,
        'problem_id' : pid,
        'user_type' : 'student',
        'status' : 'NOT_STARTED'
    }
    #TODO figure out why backend errors
    print('calling backend AddBuild for new build')
    print(backendInput)
    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendInput))
    print('backend response:')
    print(backendResponse)
    backendJson = json.loads(backendResponse['Payload'].read())
    print('backend JSON body:')
    backendbody = json.loads(backendJson['body'])
    #ABANDON ALL HOPE
    print(json.loads(json.loads(json.loads(backendbody['body'])['body'])['body'])['body'])
    db_data = json.loads(json.loads(json.loads(backendbody['body'])['body'])['body'])['body']
    #return backendJson
    return db_data
    
def check_build(event, context):
    #same thing as submit_code without the s3 put
    #scrape params
    request = event['queryStringParameters']
    print('check_build request:')
    print(request)
    
    client = boto3.client('lambda')
    problem_set = request['set_name']
    problem_name = request['problem_name']
    pid = problem_set + '/' + problem_name
    cid = request['classroom_id']
    user = request['user']
    buildExists = 0
    backendInput = {
        'request_no' : 3,
        'build_id' : user+'/'+pid,
        'build_body' : '',
        'user_id' : user,
        'problem_id' : pid,
        'user_type' : 'student',
        'status' : 'CHECK'
    }
    #TODO figure out why backend errors
    print('calling backend AddBuild for status of existing build')
    print(backendInput)
    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendInput))
    print('backend response:')
    print(backendResponse)
    backendJson = json.loads(backendResponse['Payload'].read())
    print('backend JSON body:')
    backendbody = backendJson['body']
    print(backendbody)
    #ABANDON ALL HOPE
    db_data = json.loads(backendbody)['body']
    print(db_data)
    if('B' in db_data['body']):
        db_data['body'] = db_data['body']['B']
    else:
        db_data['body'] = json.loads(db_data['body']['S'])
    
    if(db_data['status']['S'] == 'COMPLETE'):
        # CALL DELETE FUNCTION
        backendInput = {
            'request_no' : 3,
            'build_id' : user+'/'+pid,
            'build_body' : '',
            'user_id' : user,
            'problem_id' : pid,
            'user_type' : 'student',
            'status' : 'READ'
        }
        backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendInput))
    #return backendJson
    return {
        'status' : db_data['status']['S'],
        'body' : db_data['body']
    }

    
def submit_code_handler_old(event, context):
    #scrape params
    request = event['queryStringParameters']
    request_type = request['request_type']
    #append body
    request['body'] = event['body']
    if 'testFlag' in request and request['testFlag'] != 'submit':
        return {
        'body' : event['body'],
        'status' : 'NOT STARTED (TEST CALL)',
        'build_body' : 'Pretend this is useful'
        }
    else:    
        if request_type == 'submit_code':
            client = boto3.client('lambda')
            key = request['problem_id']

            #prep s3 bucket
            print('Sending code to s3:')
            s3 = boto3.resource('s3')
            object = s3.Object('Karin-Input-Staging-Bucket-prod', key+'/Code.java')
            #object = s3.Object('Karin-Input-Staging-Bucket', key+'/Code.java')
            object.put(Body=request['body'], Bucket='Karin-Input-Staging-Bucket-prod', Key=key+'/Code.java')
            #object.put(Body=request['code'], Bucket='Karin-Input-Staging-Bucket', Key=key+'/Code.java')

            #prep data to go to backend
            
            #paste of code from backendCaller
            pid = event['problem_id']
            cid = event['classroom_id']
            user = event['user']
            stuPath = event['path']
            code = event['body']
            buildExists = 0

            #may need to upload to s3 as part of studentCode

            #statuses: NOT-STARTED, IN-PROGRESS, BUILD-FAILURE, BUILD-SUCCESS, TEST-FAILURE, TEST-SUCCESS
            #build_id: username-problem_id
            #TODO query dynamo to see if build exists already
            dbclient = boto3.resource('dynamodb')
            table = dbclient.Table('build_table')
            bid = ''+user+'-'+pid
            print('build id:')
            print(bid)
            response = table.query(KeyConditionExpression=Key('build_id').eq(bid))
            print('dynamo response:')
            print(response)
            responseJson = {}
            if response['ScannedCount'] < 1:
                print('no matching build in dynamo')
                #return{
                #    'statusCode' : 200,
                #    'body' : 'build not in dynamo'
                #}
            else:
                #may need to change to account for more than one resulting build
                responseJson = json.dumps(response['Items'][0])
                responseJson = json.loads(responseJson)
                status = json.dumps(responseJson['status'])
                testResults = json.dumps(responseJson['build_body'])
                
                if status == '"COMPLETE"':
                    client = boto3.client('lambda')
                    backendInput = {
                        'request_no' : 3,
                        'build_id' : bid,
                        'build_body' : '',
                        'user_id' : user,
                        'problem_id' : pid,
                        'problem_name' : 'test-problems/test-0',
                        'input_key' : 'test-problems/test-0',
                        'input_bucket' : 'karin-web-staging-bucket',
                        'user_type' : 'student',
                        'status' : 'READ'
                    }
                    print('calling backend AddBuild with READ')
                    print(backendInput)
                    backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendInput))
                    print('backend response:')
                    print(backendResponse)
                    backendJson = json.loads(backendResponse['Payload'].read())
                    print('backend JSON:')
                    print(backendJson)
                    return {
                        'body':backendJson,
                        'status' : status,
                        'build_body':testResults    
                    }
                print('status:')
                print(status)
                return{
                    'body' : responseJson,
                    'status' : status
                }
            #TODO forward s3 location of non-existent builds to backend
            client = boto3.client('lambda')
            backendInput = {
                'request_no' : 3,
                'build_id' : bid,
                'build_body' : '',
                'user_id' : user,
                'problem_id' : pid,
                #'problem_name' : pid,
                'problem_name' : 'test-problems/test-0',
                #'in_key' : pid,
                'input_key' : 'test-problems/test-0',
                'input_bucket' : 'karin-web-staging-bucket',
                'user_type' : 'student',
                'status' : 'NOT_STARTED'
                #'status' : 'READ'
            }
            print('calling backend AddBuild for new build')
            print(backendInput)
            backendResponse = client.invoke(FunctionName=os.environ['BackendLambdaArn'], InvocationType='RequestResponse', Payload=json.dumps(backendInput))
            print('backend response:')
            print(backendResponse)
            backendJson = json.loads(backendResponse['Payload'].read())
            print('backend JSON body:')
            print(backendJson)
            print('called backend handler')
            return backendJson

        return response['body']
            
            