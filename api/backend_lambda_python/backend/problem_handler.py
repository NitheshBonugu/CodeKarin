import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    req = event['request_no']
    # problem interfaces
    if req == 30:
        # add problem_set
        response = add_problem_set(event, context)
    elif req == 31:
        # get problem_set by id
        response = get_problem_set(event, context)
    elif req == 32:
        # delete problem_set by id
        response = delete_problem_set(event, context)
    elif req == 33:
        # get problem by id
        response = get_problem_by_id(event, context)

    return response


def add_problem_set(event, context):
    ''' given problem set name, add all problems in longterm s3 to new entries '''

    bucket_name = 'karin-longterm-storage-bucket'
    client = boto3.client('dynamodb')
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    #Make sure you provide / in the end
    prefix = event['problem_set'] + '/'
    class_id = event['classroom_id']
    professor_id = event['professor_id']
    end_date = event['end_date']
    
    result = []
    for objects in bucket.objects.filter(Prefix=prefix):
        tmp_path = objects.key
        arr = tmp_path.split("/")
        tmp_path = arr[0] + "/" + arr[1]
        if(tmp_path not in result):
            result.append(tmp_path)
            
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('problem_table')
    
    db_response = []
    for r in result:  
        arr = r.split("/")
        response = table.put_item(
            Item={
                    'problem_id': str(r),
                    'problem_set': str(arr[0]),
                    'problem_name': str(arr[1]),
                    'class_id': class_id,
                    'professor_id': professor_id,
                    'solution': bucket_name + ":" + r,
                    'end_date': end_date
                }
        )
        db_response.append(response)
        
    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "paths": result,
            "db_response": db_response
        }

def get_problem_set(event, context):
    ''' given id of problem set return problem attributes '''
    problem_get_response = []
    problem_set = event['problem_set']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('problem_table')
    
    fe = boto3.dynamodb.conditions.Attr('problem_set').eq(problem_set);

    response = table.scan(
            FilterExpression=fe        
        )
    
    for i in response["Items"]:
        problem_get_response.append(i)

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "problem_set_get_response": problem_get_response
        }
        
def get_problem_by_id(event, context):
    ''' given id of problem return problem attributes '''
    problem_get_response = []
    problem_id = event['problem_id']
    
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('problem_table')
    
    fe = boto3.dynamodb.conditions.Attr('problem_id').eq(problem_id);

    response = table.scan(
            FilterExpression=fe        
        )
        
    for i in response["Items"]:
        problem_get_response.append(i)
      
    no_db_entry = False
    if len(problem_get_response) == 0:  
        no_db_entry = True    
        return {
                'statusCode' : 404,
                'body': "no problem with given id found in database"
            }
    
    if no_db_entry:
        return {
                'statusCode' : 404,
                'body': "no problem with given id found in database"
            }
    
    soln = problem_get_response[0]['solution']
    ar = soln.split(':')
    
    obj = s3.get_object(Bucket=ar[0], Key=ar[1] + "/description.json")
    desc = json.loads(obj['Body'].read().decode('utf-8'))

    obj = s3.get_object(Bucket=ar[0], Key=ar[1] + "/boilerplate.java")
    boiler = obj['Body'].read().decode('utf-8')

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "problem_get_response": {
                "boilerplate": boiler,
                "description": desc,
                "class_id": problem_get_response[0]['class_id'],
                "professor_id": problem_get_response[0]['professor_id']
            }
        }
    
def delete_problem_set(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('problem_table')
    
    get_problem_set_response = get_problem_set(event, context)
    
    problem_get_response = get_problem_set_response['problem_set_get_response']
    del_problem_set = event['problem_set']

    del_problem_response = []
    for p in problem_get_response:
        del_problem_id = p['problem_id']
        try:
            response = table.delete_item(
                Key={
                    'problem_id': del_problem_id,
                    'problem_set': del_problem_set
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        del_problem_response.append(response)
        
    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "del_problem_set_response": del_problem_response
        }