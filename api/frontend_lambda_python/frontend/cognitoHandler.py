import json
import boto3

def login_test(event, context):
	request = event['queryStringParameters']
	username=request['user']
	token = request['token']
	client=boto3.client('cognito-idp', region_name="us-east-1")
	response = client.associate_software_token(AccessToken=token)
	if response != null:
		return {
			'status' : 'true'
		}
	else:
		return {
			'status':'false'
		}

def check_username(event, context):
	request = event['queryStringParameters']
	#id_token = request['id_token']
	client = boto3.client('cognito-idp', region_name='us-east-1')
	
	
	nameresponse = client.get_user(
		AccessToken = request['access_token']
	)
	print('username response:')
	print(nameresponse)
	response = client.admin_get_user(
		UserPoolId = 'us-east-1_v6tN0GE5K',
		Username = nameresponse['Username']
	)
	print('admin response:')
	print(response)
	if 'UserAttributes' in response and 'UserStatus' in response:
		attr = response['UserAttributes']
		stat = response['UserStatus']
		email = None
		for i in attr:
			if i['Name'] == 'email':
				email = i['Value']
		print(attr)
		print(stat)
		print(response)
		
		if stat == 'CONFIRMED' and email != None:
			return {
				'user_id' : response['Username'],
				'email' : email
			}
	return{
		'statusCode' : 403,
		'body' : 'user not found'
	}