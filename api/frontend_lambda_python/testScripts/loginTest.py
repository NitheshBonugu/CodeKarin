import json
#from urllib import request
#from apiGatewayHandler import lambda_handler as api
# send JSON test objects to api and record the hard coded response that is returned

link = 'https://api.codekarin.com/prod/%7Bproxy+%7D?request_no=21&request_type=get_user&user=sampleUser&request_name=getUserUnitTest'

import urllib.request
req = request(link)
req.add_header('id_token', 'eyJraWQiOiJKUXZLcHRIXC84WndxVnlRSEVtU0Q5MXpWZlRWb1lFQVROUWF0ZXdcL2U0c3M9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiai1oVkxxMGtMRDBhc3U0T1BPTW8xdyIsInN1YiI6IjAwYzY0MjYxLTg0ZDUtNDc5Zi04ZmNjLTA5OWFjZTA1MWM0NCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV81VmFGa0pUWWQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZHlsYW53dWxmc29uIiwiYXVkIjoiM2R0MWJ0NGMzcW4wNGF2N2g4NzBrbjA5aGoiLCJldmVudF9pZCI6ImU1NDY0NjA4LTQwZjAtNDA5ZC1iNDc2LTNmZmY3YmZjNzI0ZiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjQ5MDE1OTU4LCJleHAiOjE2NDkwMTk1NTgsImlhdCI6MTY0OTAxNTk1OCwianRpIjoiNjBhNTZkNDQtNzgzYi00MGM3LWI1NjQtMDI4MTZkMjM2NTM0IiwiZW1haWwiOiJkd3VsZnNvbkBjb21jYXN0Lm5ldCJ9.gNKXX8iqlr8VmdddtIt77ow4xVvfId9kKpsOlaglcbtCIiUKnBlRdcuha-QpqpQXWEN55XnSf5E4Wx1RSMSHAkPtAXlzEP26ElGeWUHpqztN-8vr-CD3TGUb7vhsMejfUs1CYCilB4HiD0luf3rrIZ-cgf9d0srVoFHWyreJN_5GidZRCmj9XkVOV86F3NP-vgsT6h8QllXmaKM9vjV06sBH5vNzYK09QnG67k84IwW0Dka7ODCJZjh8LZ7pRLzR7WXhFHIGGF13cgb-f9PXtxXnnHMuBJyWkch4_0oKDxjjIOxjo1klPeKxpMTCS7g_XR0ct-8Thva4c49mBJwmAg')
req.add_header('access_token', 'eyJraWQiOiJBUlY1aEk4Qk9nNitEM1pZTXdWckNFQ1M0OUxpaFp0ZXNLbmQ0UEVaVXNzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwMGM2NDI2MS04NGQ1LTQ3OWYtOGZjYy0wOTlhY2UwNTFjNDQiLCJldmVudF9pZCI6ImU1NDY0NjA4LTQwZjAtNDA5ZC1iNDc2LTNmZmY3YmZjNzI0ZiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gb3BlbmlkIHByb2ZpbGUiLCJhdXRoX3RpbWUiOjE2NDkwMTU5NTgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzVWYUZrSlRZZCIsImV4cCI6MTY0OTAxOTU1OCwiaWF0IjoxNjQ5MDE1OTU4LCJ2ZXJzaW9uIjoyLCJqdGkiOiJiMWNiZGZjNi01YzY1LTQ3OTQtYWE2Yi1mYmVkNDE0MzY1MDciLCJjbGllbnRfaWQiOiIzZHQxYnQ0YzNxbjA0YXY3aDg3MGtuMDloaiIsInVzZXJuYW1lIjoiZHlsYW53dWxmc29uIn0.o7Lhfe8y9ncTI8JkRdRUssdTgEhtSw8GCnVYP05_gvClYgYh2CmxsjbEOKQFuFvAJn-l73WRCkUMiEPTdFwHBwXzz7BIfkryIUm2jVwdlcoG9f0NcruoEsJxCtq8wJl5aeYtZdvKJIsWI7oGtJIMQmwOy_vAvYCbYSxRa3VcYywGF7usOaLDpw1j-6vbHlaKHq0_lT896ddTheKd_ILv1vcizmrFGAf59bai3jRoAKg55htGTrYt8EQCu7g84Q9b8Amb_Cfn7xOm5j83BzOtBaHxq0x79DwI8bT-vyzoTettgC0RhLCWdO93RJqVXJvQiT3wt6mLUrs6f6ZAeWolAQ')
resp = request.urlopen(req)
content = resp.read()
print(content)





'''
loginEvent = {
    'queryStringParameters' : {
        'user' : 'sampleUser',
        'request_name' : 'loginUnitTest',
        'request_type' : 'login',
        'request_no' : '1000',
        'testFlag' : 1,
        'username' : 'sampleUsername',
        'password' : 'samplePassword'
    },
    'body' : ''
}

print("Test login event: ")
print(loginEvent)
print("\n")

context = {
    'test' : 'context shouldnt need anything for the api'
}

print("*If testing locally ignore the error from boto3*\n")

response = api(loginEvent, context)
print('\nresponse returned from API:')
print(response)
'''