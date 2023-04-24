# This is the cdk app used to instantiate resources for the Karin Virtual Classroom Web Application

to execute / deploy stacks run:
	
	(validate typescript files)
	npm run build

	(deploy)
	MANUAL STEPS REQUIRED FOR DEPLOYMENT:
		1. deploy cognito stack
		2. check the cognito pool id and cognito client id and save them
		3. edit the cognito pool id in the api/frontend_lambda_python/frontend/cognito.py
		4. edit the cognito client id in the react-webserver/src/App.js login route
		5. deploy the backend, frontend, and client stacks

	sudo cdk deploy CognitoStack
	sudo cdk deploy backend-CDK-Stack
	sudo cdk deploy frontend-CDK-Stack --outputs-file ./frontend_cdk_outputs.json
	sudo cdk deploy client-CDK-Stack

	(teardown)
	cdk destroy client-CDK-Stack
	cdk destroy frontend-CDK-Stack
	cdk destroy backend-CDK-Stack
	cdk destroy CognitoStack

to update the existing infrastructure edit the following files:

	bin/cdk.ts
	lib/cognito-stack.ts
		(cognito definitions)
	lib/backend_cdk-stack.ts
		(data layer and backend definitions)
	lib/frontend_cdk-stack.ts
		(frontend api definitions)
	lib/client-cdk-stack.ts
		(public web client definitions)

Default Readme.md contend is below

# Welcome to your CDK TypeScript project!

This is a blank project for TypeScript development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
