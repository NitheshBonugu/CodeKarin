This project is designed to be a teacher-oriented code submission and review platform to teach programming at any level.

Authors:
	Jacob Hollis	
	Ngan Tran
	Kate Brayshaw
	Dylan Wulfson
	Nithesh Bonugu

Client: 
	Dr. Krishna Kadiyala, Assistant Professor of Computer Science at Texas Christian University


DIRECTORY OVERVIEW:
	api
	''' AWS lambda packages written in python3.8 '''
		frontend_api
		backend_api

	cdk
	''' AWS CDK package containing 3 CDK stacks '''
		client_stack
		''' implements react frontend webserver and public data layer resources '''
		frontend_stack
		''' implements frontend api resources '''
		backend_stack
		''' implements backend api and data layer resources '''
			Codebuild (Testing Runtime)
			DynamoDB (User Tables)
			s3 (Object Storage for unformatted data)
		cognito_stack
		''' implements cognito / domain name integration resources '''

	problems
	''' storage location for platform problems '''
		scripts
		''' stores useful development scripts for manipulating the problem sets manually '''
		default_package
		''' the default runtime for java maven projects immplemented using AWS codebuild '''
		**
		''' problem_set '''
			** 
			''' problem_name '''
			see readme in problems for more information
	react-webserver
	''' contains ReactJS webserver with docker integration for dynamic web hosting '''

