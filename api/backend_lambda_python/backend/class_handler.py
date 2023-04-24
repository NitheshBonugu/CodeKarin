import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    req = event['request_no']
    # class interfaces
    if req == 10:
        # add class
        response = add_class(event, context)
    elif req == 11:
        # get class by id
        response = get_class_by_id(event, context)
    elif req == 12:
        response = delete_class(event, context)

    return response


def add_class(event, context):
    ''' given class attribues, add a new entry to the table '''

    # class id: class_#
    # prof_id: user_id
    # end_date: date time
    # list <problem_id>
    # list <user_id>
    # list <discussion_id>
    
    class_id = event["new_class_id"]
    professor_id = event["user_id"]
    end_date = event["end_date"]
    problems = event["problem_sets"]
    contests = event["contest_sets"]
    students = event["students"]

    dynamo_resource = boto3.resource('dynamodb')
    class_table = dynamo_resource.Table('classroom_table')
    class_put_response = class_table.put_item(
        Item={
            "classroom_id": class_id,
            "professor_id": professor_id,
            "end_date": end_date,
            "problems": problems,
            "contests": contests,
            "students": students,
            "discussion": {}
        }
    )

    return class_put_response

def get_class_by_id(event, context):
    ''' given id of class return class attributes '''
    cid = event['cid_to_get']
    class_get_response = {}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('classroom_table')
    
    fe = boto3.dynamodb.conditions.Attr('classroom_id').eq(cid);

    response = table.scan(
            FilterExpression=fe        
        )
    
    if len(response["Items"]) > 0 :
        class_get_response = response["Items"][0]

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "classroom_get_response": class_get_response
        }
    

def delete_class(event, context):
    ''' given class id delete given class in dynamo '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('classroom_table')
    
    user_id = event['user_id']
    del_class_id = event['del_class_id']

    try:
        response = table.delete_item(
            Key={
                'professor_id': user_id,
                'classroom_id': del_class_id
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
            "classroom_del_response": response
        }