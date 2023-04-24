import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as codebuild from '@aws-cdk/aws-codebuild';
import * as iam from '@aws-cdk/aws-iam';
import * as dynamo from '@aws-cdk/aws-dynamodb';
import * as _lambda from '@aws-cdk/aws-lambda';
import * as eventsources from '@aws-cdk/aws-lambda-event-sources';
import * as apigateway from '@aws-cdk/aws-apigateway';

// BACKEND
export class backend_CdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // role definitions
    const backend_lambda_role = new iam.Role(this, 'backend_lambda_role', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });
    backend_lambda_role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    backend_lambda_role.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    const backend_codebuild_role = new iam.Role(this, 'backend_codebuild_role', {
      assumedBy: new iam.ServicePrincipal('codebuild.amazonaws.com'),
    });
    backend_codebuild_role.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // role definitions
    const frontend_lambda_role = new iam.Role(this, 'frontend_lambda_role', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });
    frontend_lambda_role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    frontend_lambda_role.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // DynamoDB [build runtime definitions, user definitions, classroom definitions, relational data between users, classrooms, problems, and builds]
    var user_table = new dynamo.Table(this, 'user_table', {
      partitionKey: {name: 'user_id', type: dynamo.AttributeType.STRING},
      sortKey: {name: 'cognito_id', type: dynamo.AttributeType.STRING},
      tableName: 'user_table',
    });
    user_table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    var classroom_table = new dynamo.Table(this, 'classroom_table', {
      partitionKey: {name: 'classroom_id', type: dynamo.AttributeType.STRING},
      sortKey: {name: 'professor_id', type: dynamo.AttributeType.STRING},
      tableName: 'classroom_table',
    });
    classroom_table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    var problem_table = new dynamo.Table(this, 'problem_table', {
      partitionKey: {name: 'problem_id', type: dynamo.AttributeType.STRING},
      sortKey: {name: 'problem_set', type: dynamo.AttributeType.STRING},
      tableName: 'problem_table',
    });
    problem_table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    var build_table = new dynamo.Table(this, 'build_table', {
      partitionKey: {name: 'build_id', type: dynamo.AttributeType.STRING},
      sortKey: {name: 'user_id', type: dynamo.AttributeType.STRING},
      tableName: 'build_table',
    });
    build_table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    var grades_table = new dynamo.Table(this, 'grades_table', {
      partitionKey: {name: 'user_id', type: dynamo.AttributeType.STRING},
      sortKey: {name: 'problem_id', type: dynamo.AttributeType.STRING},
      tableName: 'grades_table',
    });
    grades_table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    var discussion_table = new dynamo.Table(this, 'discussion_table', {
      partitionKey: {name: 'sender_id', type: dynamo.AttributeType.STRING},
      sortKey: {name: 'classroom_id', type: dynamo.AttributeType.STRING},
      tableName: 'discussion_table',
    });
    discussion_table.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // S3 [problem storage and CodeBuild resource storage buckets]
    var longterm_storage_bucket = new s3.Bucket(this, 'longterm-s3', {
      accessControl: s3.BucketAccessControl.PRIVATE,
      autoDeleteObjects: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      bucketName: "karin-longterm-storage-bucket"

    });

    var input_staging_bucket = new s3.Bucket(this, 'input-s3', {
      accessControl: s3.BucketAccessControl.PRIVATE,
      autoDeleteObjects: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      bucketName: "karin-input-staging-bucket"

    });

    var output_staging_bucket = new s3.Bucket(this, 'output-s3',{
      accessControl: s3.BucketAccessControl.PRIVATE,
      autoDeleteObjects: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      bucketName: "karin-output-staging-bucket"
    });

    // s3 web input bucket
    var web_input_staging_bucket = new s3.Bucket(this, 'web-s3', {
      accessControl: s3.BucketAccessControl.PRIVATE,
      autoDeleteObjects: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      bucketName: "karin-web-staging-bucket"
    });

    // CodeBuild [execution project]
    var codebuild_builder = new codebuild.Project(this, 'project-builder', {
      description: 'this is a codebuild project to compile and build source for the Karin Virtual Classroom applications',
      projectName: 'Karin-Project-Builder',
      source: codebuild.Source.s3({
        bucket: input_staging_bucket,
        path: '',
      }),
      artifacts: codebuild.Artifacts.s3({
        bucket: output_staging_bucket,
        includeBuildId: false,
        packageZip: false,
        path: '',
      }),
      environment: {
        privileged: true,
        buildImage:  codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
        computeType: codebuild.ComputeType.SMALL,
      },
      role: backend_codebuild_role
    });
    codebuild_builder.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // Lambda (back-end) [database / private s3 access]
    var python_backend_lambda = new _lambda.Function(this, 'Backend_Python_Lambda_Func', {
      runtime: _lambda.Runtime.PYTHON_3_8,
      code: _lambda.Code.fromAsset('../api/backend_lambda_python'),
      handler:'backend/handler.lambda_handler',
      role: backend_lambda_role,
      timeout: cdk.Duration.seconds(30),
      logRetention: 5,
    });

    // add event source for output staging bucket
    python_backend_lambda.addEventSource(new eventsources.S3EventSource(output_staging_bucket, {
      events: [ s3.EventType.OBJECT_CREATED ],
    }));
    python_backend_lambda.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // API Gateway (back-end) [called by front-end API to back-end lambda]
    var backend_api = new apigateway.LambdaRestApi(this, 'back-end-api', {
      handler: python_backend_lambda,
      endpointExportName: "BackendApiLink",
      cloudWatchRole: true
    });
    backend_api.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);


    const table_arn_list = [user_table.tableArn, classroom_table.tableArn, problem_table.tableArn, build_table.tableArn, grades_table.tableArn, discussion_table.tableArn];
    const bucket_arn_list = [longterm_storage_bucket.bucketArn, input_staging_bucket.bucketArn, output_staging_bucket.bucketArn];

    const table_arn_list_output = new cdk.CfnOutput(this, 'TableArnList', { value: table_arn_list.toString(), exportName: 'TableArnList'});
    const python_backend_lambda_arn_output = new cdk.CfnOutput(this, 'BackendLambdaArn', { value:  python_backend_lambda.functionArn, exportName: 'BackendLambdaArn'});
    const frontend_lambda_role_arn = new cdk.CfnOutput(this, 'FrontendRoleArn', { value:  frontend_lambda_role.roleArn, exportName: 'FrontendRoleArn'});

    // apply backend codebuild role policy on resources
    backend_codebuild_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: (table_arn_list) as string[],
      actions: ['dynamodb:*'],
    }));
    backend_codebuild_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: [codebuild_builder.projectArn],
      actions: ['*'],
    }));


    // apply backend lambda role policy on resources
    backend_lambda_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: (table_arn_list) as string[],
      actions: ['dynamodb:*'],
    }));
    backend_lambda_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: [codebuild_builder.projectArn],
      actions: ['*'],
    }));
    backend_lambda_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ['cognito-idp:*'],
    }));

    // add policies to frontend lambda role
    frontend_lambda_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: table_arn_list,
      actions: ['dynamodb:*'],
    }));
    frontend_lambda_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
	  resources: [python_backend_lambda.functionArn],
	  actions: ['lambda:InvokeFunction'] 
	}));
    frontend_lambda_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ['cognito-idp:*'],
    }));
  
    // grant backend lambda role ability to read / write objects in s3
    longterm_storage_bucket.grantDelete(backend_lambda_role)
    web_input_staging_bucket.grantDelete(frontend_lambda_role)
    input_staging_bucket.grantDelete(backend_lambda_role)
    input_staging_bucket.grantDelete(backend_codebuild_role)
    output_staging_bucket.grantDelete(backend_lambda_role)
    output_staging_bucket.grantDelete(backend_codebuild_role)
    web_input_staging_bucket.grantDelete(backend_lambda_role)
    
    longterm_storage_bucket.grantReadWrite(backend_lambda_role)
    web_input_staging_bucket.grantReadWrite(frontend_lambda_role)
    input_staging_bucket.grantReadWrite(backend_lambda_role)
    input_staging_bucket.grantReadWrite(backend_codebuild_role)
    output_staging_bucket.grantReadWrite(backend_lambda_role)
    output_staging_bucket.grantReadWrite(backend_codebuild_role)
    web_input_staging_bucket.grantReadWrite(backend_lambda_role)

    longterm_storage_bucket.grantPut(backend_lambda_role)
    web_input_staging_bucket.grantPut(frontend_lambda_role)
    input_staging_bucket.grantPut(backend_lambda_role)
    input_staging_bucket.grantPut(backend_codebuild_role)
    output_staging_bucket.grantPut(backend_lambda_role)
    output_staging_bucket.grantPut(backend_codebuild_role)
    web_input_staging_bucket.grantPut(backend_lambda_role)
  }
}
