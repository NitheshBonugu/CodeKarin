import json

def lambda_handler(event, context):
    
    #return statement
    ret = {
        'statusCode': 200,
        'body': json.dumps('this page is not implemented, use login.auth.codekarin.com instead')
    }

    print(ret)
    return ret