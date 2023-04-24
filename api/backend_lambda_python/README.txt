Assembly-Handler

 - Get default build from longterm bucket
 - Get user code from longterm bucket or input staging bucket
 - Put assembled build in input staging bucket

_________________________________________________________

Execution-Handler

 - Start build from the input staging bucket using CodeBuild
 - Output Lambda artifacts to output staging bucket

_________________________________________________________

Clean-Build-Handler

 - Delete all user builds in input / output staging buckets given a username

_________________________________________________________

request.json

 - Defines request / response formats for lambda functions
 - request for assembly handler produces a response that is formatted as a request for the execution handler and so on...
