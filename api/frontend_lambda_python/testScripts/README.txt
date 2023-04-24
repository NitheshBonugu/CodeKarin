Some of the test scripts need to be updated

For testing the live API use the testing window in AWS Lambda 
 or if offline testing is needed copy/paste the json object from AWS into one of these scripts, the rest is boilerplate code and can be changed for readability 

json2url is a script to loop through a JSON object and generate a sample URL to call a request from the API
 no validation is done to make sure the requests actually exist on the API side
 the script is just meant to make writing URLs easier for team members unfamiliar with JSON

To run one of the tests move it to the frontend_lambda_python parent folder and run it using either python at the command line or from within an editor
 non-fatal errors will be thrown if botocore has not been added to the python install: "pip install botocore"
 
Botocore documentation: https://pypi.org/project/botocore/
