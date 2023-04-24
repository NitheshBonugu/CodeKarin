import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    req = event['request_no']
    # grade interfaces
    if req == 40:
        # add grade
        response = add_grade(event, context)
    elif req == 41:
        # get grade by id
        response = get_grade(event, context)
    elif req == 42:
        # delete grade by id
        response = delete_grade(event, context)
    elif req == 43:
        # get grade list
        response = get_grade_list(event, context)
    elif  req == 44:
        response = get_leaderboard_list(event, context)

    return response
    
def add_grade(event, context):
    ''' given grade attribues, add a new entry to the table '''
    
    class_id = event["classroom_id"]
    professor_id = event["professor_id"]
    problem_id = event["problem_id"]
    user_id = event["user_id"]
    grade = int(event["grade"])
    time = event["run_time"]
    finished = grade and 1

    dynamo_resource = boto3.resource('dynamodb')
    grades_table = dynamo_resource.Table('grades_table')
    grade_put_response = grades_table.put_item(
        Item={
            "grade_id": professor_id + class_id + problem_id + user_id,
            "classroom_id": class_id,
            "professor_id": professor_id,
            "problem_id": problem_id,
            "problem_set": problem_id.split("/")[0],
            "user_id": user_id,
            "grade": grade,
            "run_time": time
        }
    )

    return grade_put_response
    
def get_grade(event, context):
    
    ''' given id of user, problem, and class return grade attributes '''
    class_id = event["classroom_id"]
    professor_id = event["professor_id"]
    problem_id = event["problem_id"]
    user_id = event["user_id"]
    grade_get_response = {}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('grades_table')
    
    fe = boto3.dynamodb.conditions.Attr('classroom_id').eq(class_id) and boto3.dynamodb.conditions.Attr('professor_id').eq(professor_id) and boto3.dynamodb.conditions.Attr('problem_id').eq(problem_id) and boto3.dynamodb.conditions.Attr('user_id').eq(user_id)
        
    response = table.scan(
            FilterExpression=fe        
        )
    
    if len(response["Items"]) > 0 :
        grade_get_response = response["Items"][0]

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "grade_get_response": class_get_response
        }
    

def delete_grade(event, context):
    ''' given grade attributes delete given grade in dynamo '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('grades_table')
    
    class_id = event["classroom_id"]
    professor_id = event["user_id"]
    problem_id = event["problem_id"]
    user_id = event["user_id"]

    try:
        response = table.delete_item(
            Key={
                "grade_id": professor_id + class_id + problem_id + user_id,
                "user_id": user_id
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
        
    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "grade_del_response": response
        }

def get_grade_list(event, context):
    ''' given id of user, problem, and class return grade attributes '''
    class_id = event["classroom_id"]
    professor_id = event["professor_id"]
    user_id = event["user_id"]
    grade_list_get_response = {
        "user_id":user_id,
        "class_id":class_id,
        "professor_id":professor_id,
        "grade_aggregate": 0
        
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('grades_table')
    
    fe = boto3.dynamodb.conditions.Attr('classroom_id').eq(class_id) and boto3.dynamodb.conditions.Attr('professor_id').eq(professor_id) and boto3.dynamodb.conditions.Attr('user_id').eq(user_id)
        
    response = table.scan(
            FilterExpression=fe        
        )
    
    if len(response["Items"]) > 0 :
        for i in response["Items"]:
            grade_list_get_response['grade_aggregate'] += i['grade']
    else:
        grade_list_get_response['grade_aggregate'] = 0
        

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "grade_list_get_response": grade_list_get_response
        }
        
def get_leaderboard_list(event, context):
    ''' given id of user, problem, and class return grade attributes '''
    class_id = event["classroom_id"]
    professor_id = event["professor_id"]
    user_id = event["user_id"]
    problem_set = event["problem_set"]
    grade_list_get_response = {
        "user_id":user_id,
        "class_id":class_id,
        "professor_id":professor_id,
        "problem_set": problem_set,
        "start_time":None,
        "end_time":None,
        "run_time": 0,
        "grade_aggregate": 0
        
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('grades_table')
    
    fe = boto3.dynamodb.conditions.Attr('classroom_id').eq(class_id) and boto3.dynamodb.conditions.Attr('professor_id').eq(professor_id) and boto3.dynamodb.conditions.Attr('user_id').eq(user_id) and boto3.dynamodb.conditions.Attr('problem_set').eq(problem_set)
        
    response = table.scan(
            FilterExpression=fe
        )
    
    if len(response["Items"]) > 0 :
        print(response["Items"])
        for i in response["Items"]:
            if(not i['user_id'] == user_id):
                continue;
            grade_list_get_response['grade_aggregate'] += i['grade']
            grade_list_get_response['run_time'] += float(i['run_time'])
    else:
        grade_list_get_response['grade_aggregate'] = 0
        

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "grade_list_get_response": grade_list_get_response
        }