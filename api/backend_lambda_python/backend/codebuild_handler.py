import json
import boto3
from boto3.dynamodb.conditions import Key

def assemble_build(event, context):
    ''' this lambda_handler implements a workflow for the Karin Virtual Classroom Codebuild testing framework '''
    
    # load codebuild client
    cb_client = boto3.client('codebuild')
    # load s3 client
    sss_client = boto3.client('s3')
    s3 = boto3.resource('s3')
    
    # get event details
    longtermBucket = "karin-longterm-storage-bucket"
    default_project = "default_project/"
    inBucket = "karin-web-staging-bucket"
    inKey = event['problem_id']
    outBucket = "karin-input-staging-bucket"
    outPath = event['input_path'] + '/' + "default_project/"
    src_out_path = outPath + "src"
    
    # instantiate response object
    response = event

    # add user and request info to response
    response['user_id'] = event['user_id']
    response['problem_name'] = event['input_path']
    
    # verify that the input / output bucket and path exist
    # call database
    
    # format valid longterm bucket response
    response['s3_longterm_bucket'] = longtermBucket
    response['s3_longterm_path'] = default_project
    # format valid input bucket response
    response['s3_input_bucket'] = inBucket
    response['s3_input_path'] = inKey
    # format valid output bucket response
    response['s3_output_bucket'] = outBucket
    response['s3_output_path'] = outPath
    response['s3_src_output_path'] = src_out_path
    
    longtermBucket_res = s3.Bucket(longtermBucket)
    inBucket_res = s3.Bucket(inBucket)
    outBucket_res = s3.Bucket(outBucket)
    
    # verify inKey
    objs = []
    for obj in inBucket_res.objects.filter(Prefix=response['user_id'] + '/' + inKey + '/main/'):
        objs.append(obj)
        
    if(len(objs) == 0):
        return {
            'statusCode': 404,
            'body': response
        }
    
    # copy default project to s3-input-staging/problem-name/username/request-no/
    for obj in longtermBucket_res.objects.filter(Prefix=default_project):
        old_source = { 
            'Bucket': longtermBucket,
            'Key': obj.key
        }
        # replace the prefix
        new_key = outPath + obj.key[len(default_project):]
        new_obj = outBucket_res.Object(new_key)
        new_obj.copy(old_source)
    
    # copy src from longterm to default project in staging
    for obj in longtermBucket_res.objects.filter(Prefix=inKey + '/test/'):
        old_source = { 
            'Bucket': longtermBucket,
            'Key': obj.key
        }
        # replace the prefix
        new_key = src_out_path + obj.key[len(inKey):]
        new_obj = outBucket_res.Object(new_key)
        new_obj.copy(old_source)
        
    # copy src from web input to default project in staging
    for obj in inBucket_res.objects.filter(Prefix=response['user_id'] + '/' + inKey + '/main/'):
        old_source = { 
            'Bucket': inBucket,
            'Key': obj.key
        }
        # replace the prefix
        new_key = src_out_path + obj.key[len(response['user_id'] + '/' + inKey):]
        new_obj = outBucket_res.Object(new_key)
        new_obj.copy(old_source)
    
    resPath = outPath + "lambda_exec_output/assembly_response.json"
    result = sss_client.put_object(Bucket=outBucket, Key=resPath, Body=json.dumps(response), ContentEncoding="application/json")
    return {
            'statusCode': 200,
            'body': response
        }



def clean_build(event, context):
    ''' this lambda_handler implements a workflow for the Karin Virtual Classroom Codebuild testing framework '''
    
    # load codebuild client
    cb_client = boto3.client('codebuild')
    # load s3 client
    s3 = boto3.resource('s3')
    # load dynamo resource
    dynamo_resource = boto3.resource('dynamodb')
    
    # get event details
    user = event['user_id']
    inBucket = "karin-input-staging-bucket"
    outBucket = "karin-output-staging-bucket"
    
    # instantiate response object
    response = event
    
    # add user and request info to response
    response['user_id'] = event['user_id']
    
    # delete user info from input staging
    bucket = s3.Bucket(inBucket)
    bucket.objects.filter(Prefix=str(user)+"/").delete()
    # delete user info from output staging
    bucket = s3.Bucket(outBucket)
    bucket.objects.filter(Prefix=str(user)+"/").delete()
    # delete user build info
    table = dynamo_resource.Table('build_table')
    table.delete_item(
        Key={
            'build_id': user + "/" + event['problem_id'],
            'user_id': user
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }




def execute_build(event, context):
    ''' this lambda_handler implements a workflow for the Karin Virtual Classroom Codebuild testing framework '''
    # load codebuild client
    cb_client = boto3.client('codebuild')
    # load s3 client
    sss_client = boto3.client('s3')
    
    # get event details
    inBucket = "karin-input-staging-bucket"
    inKey = event['user_id'] + "/" + event['problem_id'] + "/default_project/"
    outBucket = "karin-output-staging-bucket"
    outPath = event['user_id'] + "/" + event['problem_id'] + "/"
    proName = "Karin-Project-Builder"
    
    # instantiate response object
    response = event
    
    # add user and request info to response
    response['user_id'] = event['user_id']
    response['request_no'] = event['request_no']
    
    # verify that the input bucket and path eist
    result = sss_client.list_objects(Bucket=inBucket, Prefix=inKey)
    if(not('Contents' in result)):
        # handle error accordingly
        return{
            'statusCode': 500,
            'body': "the codebuild input resources do not exist in the specified input s3 bucket"
        }
    
    # format valid bucket access response
    response['s3_input_bucket'] = inBucket
    response['s3_input_path'] = inKey
        
    # verify that the output bucket exists
    try:
        sss_client.head_bucket(Bucket=outBucket)
    except ClientError:
    # The bucket does not exist or you have no access
        return{
            'statusCode': 500,
            'body': "the s3 output resources do not exist"
        }

    # call client to start build based on the recievend project_name
    result = cb_client.start_build(projectName=proName, sourceLocationOverride = (inBucket + "/" + inKey), 
    artifactsOverride={
        'type': 'S3',
        'location': outBucket,
        'path': outPath,
        'name': 'out',
        'packaging': 'NONE'
    })
    
    response['project_name'] = result['build']['projectName']
    response['build_id'] = result['build']['id']
    response['build_arn'] = result['build']['id']
    response['source_location'] = result['build']['source']['location']
    response['start_time'] = result['build']['startTime'].strftime("%m/%d/%Y, %H:%M:%S")
    
    resPath = outPath + "lambda_exec_output/exec_response.json"
    result = sss_client.put_object(Bucket=outBucket, Key=resPath, Body=json.dumps(response), ContentEncoding="application/json")
    return {
            'statusCode': 200,
            'body': response
        }



def add_build(event, context):
    # retrieve event params
    user_id = event["user_id"]
    problem_id = event["problem_id"]
    user_type = event["user_type"]
    
    # retrieve boto3 resources for s3 and dyamoDB
    dynamo_client = boto3.client('dynamodb')
    sss_client = boto3.client('s3')
    dynamo_resource = boto3.resource('dynamodb')
    
    # define dict to return
    ret = event.copy()
    
    # get problem definition from dynamo problems table
    problem_get_response = dynamo_client.query(
        TableName='problem_table',
        KeyConditions={
            'problem_id':{
                'ComparisonOperator': 'EQ',
                "AttributeValueList": [ {"S": problem_id} ]
            }
        },
        Select='ALL_ATTRIBUTES'
    )
    
    # "body": "{\"problem_response\": [{\"question_id\": {\"S\": \"test-problems-test-1\"}, \"solution\": {\"S\": \"karin-project-longterm-storage:test-problems/test-1/\"}, \"problem_set\": {\"S\": \"test-problems\"}, \"problem_name\": {\"S\": \"test-1\"}}]}"
    
    # add queried items to ret dict
    if len(problem_get_response['Items']) <= 0:
        return {
            'statusCode': 404,
            'body': 'invalid problem id'
        }
    ret['solution'] = problem_get_response['Items'][0]['solution']['S']
    
    # solution array
    ar = ret['solution'].split(':')
    
    ret['src_bucket'] = ar[0]
    ret['src_path'] = ar[1]
    ret['build_id'] = str(user_id + '/' + problem_id)
    ret['input_path'] = str(user_id + '/' + problem_id)
    
    build_table = dynamo_resource.Table('build_table')
    
    build_get_response = dynamo_client.query(
        TableName='build_table',
        KeyConditions={
            'build_id':{
                'ComparisonOperator': 'EQ',
                "AttributeValueList": [ {"S": ret['build_id']} ]
            }
        },
        Select='ALL_ATTRIBUTES'
    )
        
    tmp_status= None
    if(len(build_get_response['Items']) > 0):
        if('build_body' in build_get_response['Items'][0]):
            body_tmp = build_get_response['Items'][0]['build_body']
            stat_tmp = build_get_response['Items'][0]['status']
    else: 
        body_tmp = None
        stat_tmp = None
        
    if(ret['status'] == "CHECK"):
        ret['build_body'] = body_tmp
        ret['status'] = stat_tmp
        return {
            'statusCode': 200,
            'body':{
                'body': body_tmp,
                'status': 'CHECK',
                'ret_stats': stat_tmp
            }
        }
    else:
        ret['status'] = 'NOT_STARTED'
        
    if 'build_body' not in ret.keys():
        ret['build_body'] = ''
    if 'status' in event.keys():
        ret['status'] = event['status']
    
    build_put_response = build_table.put_item(
        Item={
            'build_id': ret['build_id'],
            'user_id': user_id,
            'build_body': ret['build_body'],
            'problem_id': problem_id,
            'src_bucket': ret['src_bucket'],
            'src_path': ret['src_path'],
            'input_bucket': 'karin-web-staging-bucket',
            'input_path': user_id + '/' + problem_id + '/',
            'build_type': user_type,
            'status': ret['status']
        }
    )
    
    ret['user_id'] = user_id
    ret['build_body'] = ret['build_body']
    ret['problem_id'] = problem_id
    ret['build_type'] = str(user_type)
    ret['status'] = ret['status']
    
    return {
            'statusCode': 200,
            'body': ret
        }
    
