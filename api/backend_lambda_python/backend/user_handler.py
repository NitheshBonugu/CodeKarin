import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    req = event['request_no']
    # user interfaces
    if req == 20:
        # add user
        response = add_user(event, context)
    elif req == 21:
        # get user by id
        response = get_user_by_id(event, context)
    elif req == 22:
        # del user by id
        response = delete_user(event, context)
    elif req == 23:
        # add user list
        response = add_user_list(event, context)
    elif req == 24:
        # delete user lis
        response = delete_user_list(event, context)
    elif req == 25:
        # get user list
        response = get_user_list(event, context)

    return response


def add_user(event, context):
    ''' given user attribues, add a new entry to the table '''

    # user_id: username
    # cognito_id: user_id
    # list <classroom_id>

    # get passed new user info
    new_id = event['new_user_id']
    new_classrooms = event['new_user_classrooms']
    new_group = event['new_user_group']
    new_email = event['new_user_email']
    
    email_verified = "true"
    if(event['is_test']):
        email_verified = "false"
    
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    
    # call once to create new user with verified email
    cogntio_add_response = cognito.admin_create_user(
        UserPoolId='us-east-1_v6tN0GE5K',
        Username=new_id,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': new_email
            },
            {
                "Name": "email_verified", 
                "Value": email_verified
            }
        ],
        ValidationData=[],
        MessageAction='SUPPRESS',
        DesiredDeliveryMediums=[
            'EMAIL',
        ]
    )
    # call again to send temporary password to user
    cogntio_add_response = cognito.admin_create_user(
        UserPoolId='us-east-1_v6tN0GE5K',
        Username=new_id,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': new_email
            },
            {
                "Name": "email_verified", 
                "Value": email_verified
            }
        ],
        ValidationData=[],
        MessageAction='RESEND',
        DesiredDeliveryMediums=[
            'EMAIL',
        ]
    )

    dynamo_resource = boto3.resource('dynamodb')
    user_table = dynamo_resource.Table('user_table')
    
    user_put_response = user_table.put_item(
        Item={
            "user_id": new_id,
            "cognito_id": "example_tmp",
            "classrooms": new_classrooms,
            "user_group": new_group
        }
    )

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            'cogntio_add_response': cogntio_add_response,
            "user_put_response": user_put_response
        }
    
    user_put_response

def get_user_by_id(event, context):
    ''' given id of user return user attributes '''
    uid = event['uid_to_get']
    user_get_response = {}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_table')
    
    fe = boto3.dynamodb.conditions.Attr('user_id').eq(uid);

    response = table.scan(
            FilterExpression=fe        
        )
    
    if len(response["Items"]) > 0 :
        user_get_response = response["Items"][0]
        

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "user_get_response": user_get_response
        }
    
def delete_user(event, context):
    ''' given user id delete given user in dynamo and cognito '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_table')
    
    del_user_id = event['del_user_id']
    del_cog_id = event['del_cog_id']

    try:
        response = table.delete_item(
            Key={
                'user_id': del_user_id,
                'cognito_id': del_cog_id
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    cogntio_del_response = cognito.admin_delete_user(
        UserPoolId='us-east-1_v6tN0GE5K',
        Username=del_user_id
    )
    
    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "user_del_response": response,
            "cognito_del_response": cogntio_del_response
        }
        
        
def add_user_list(event, context):
    new_user_list = event['new_users']
    respnse_list = []
    for i in new_user_list:
        event['new_user_id'] = i['new_user_id']
        event['new_user_classrooms'] = i['new_user_classrooms']
        event['new_user_group'] = i['new_user_group']
        event['new_user_email'] = i['new_user_email']
        event['request_no'] = 20
        event['is_test'] = i['is_test']
        response = add_user(event, context)
        respnse_list.append(response)
    
    event['request_no'] = 23
        
    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "add_user_list_response": respnse_list
        }
        
def get_user_list(event, context):
    ''' get a list of users info given a list of user ids '''
    users_to_get = event['uids_to_get']
    get_user_list_response = []
    for i in users_to_get:
        event['uid_to_get'] = i
        response = get_user_by_id(event, context)
        get_user_list_response.append(response)

    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "user_get_list_response": get_user_list_response
        }
    

def delete_user_list(event, context):
    del_user_list = event['del_users']
    respnse_list = []
    for i in del_user_list:
        event['del_user_id'] = i['del_user_id']
        event['del_cog_id'] = i['del_cog_id']
        event['request_no'] = 22
        try:
            response = delete_user(event, context)
            respnse_list.append(response)
        except Exception:
            pass
    
    event['request_no'] = 23
        
    return {
            "statusCode": 200,
            "request_no": event['request_no'],
            "add_user_list_response": respnse_list
        }