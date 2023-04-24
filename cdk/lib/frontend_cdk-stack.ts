import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as _lambda from '@aws-cdk/aws-lambda';
import * as s3 from '@aws-cdk/aws-s3';
import * as ecs from '@aws-cdk/aws-ecs';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import { DockerImageAsset } from '@aws-cdk/aws-ecr-assets';
import * as ecsPatterns from '@aws-cdk/aws-ecs-patterns';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as route53 from '@aws-cdk/aws-route53';
import * as targets from '@aws-cdk/aws-route53-targets';
import * as acm from '@aws-cdk/aws-certificatemanager';
import * as cognito from '@aws-cdk/aws-cognito';
import cognitoOutput from '../cognito_output.json';

interface FrontendStackProps extends cdk.StackProps {
  hostedZoneAttributes: route53.HostedZoneAttributes;
  parentDomain: string;
  subdomain: string;
}

// FRONTEND
export class frontend_CdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: FrontendStackProps) {
    super(scope, id, props);

    const backend_api_link = cdk.Fn.importValue('BackendApiLink');
    const table_arn_list_input = cdk.Fn.importValue('TableArnList');
    const table_arn_list = table_arn_list_input.split(",")
    const python_backend_lambda_arn = cdk.Fn.importValue('BackendLambdaArn');
    const frontend_role_arn = cdk.Fn.importValue('FrontendRoleArn');
    const frontend_lambda_role = iam.Role.fromRoleArn(this, 'frontend-lambda-role', frontend_role_arn);
    const user_pool_arn = cognitoOutput.CognitoStack.UserPoolArn;
    const userPool = cognito.UserPool.fromUserPoolArn(this, 'UserPoolArn', user_pool_arn);
    
    const domain = `${props.subdomain}.${props.parentDomain}`;
    
    const hostedZone = route53.HostedZone.fromHostedZoneAttributes(this, 'hosted-zone',
      props.hostedZoneAttributes
    );

    const cert = new acm.Certificate(this, 'parent-api-certificate', {
      domainName: domain,
      subjectAlternativeNames: [],
      validation: acm.CertificateValidation.fromDns(hostedZone),
    });
    cert.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    const browser_client_role = new iam.Role(this, 'browser_client_role', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      roleName: 'browserClientRole'
    });
    browser_client_role.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);
    
    // Lambda (front-end) [database / public s3 access]
    var python_frontend_lambda = new _lambda.Function(this, 'Frontend_Python_Lambda_Func', {
      runtime: _lambda.Runtime.PYTHON_3_8,
      code: _lambda.Code.fromAsset('../api/frontend_lambda_python'),
      handler:'apiGatewayHandler.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      role: frontend_lambda_role,
      logRetention: 5,
      environment: {
        "BackendLambdaArn": python_backend_lambda_arn
      }
    });
    python_frontend_lambda.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    const client_role_name_output = new cdk.CfnOutput(this, 'ClientRoleName', { value:  browser_client_role.roleName.toString(), exportName: 'ClientRoleName'});
    const python_frontend_lambda_arn_output = new cdk.CfnOutput(this, 'FrontendLambdaArn', { value:  python_frontend_lambda.functionArn, exportName: 'FrontendLambdaArn'});

    const auth = new apigateway.CognitoUserPoolsAuthorizer(this, 'authorizor', {
      cognitoUserPools: [userPool]
    });
    // API Gateway (front-end) [called by ECS cluster HTTP to front-end lambda]
    var frontend_api = new apigateway.LambdaRestApi(this, 'front-end-api', {
      handler: python_frontend_lambda,
      cloudWatchRole: true,
      proxy: true,
      defaultCorsPreflightOptions:{
        allowOrigins: [ 'https://codekarin.com' ],
        allowMethods: [ 'GET', 'POST' ]
      },
      defaultMethodOptions:{
        authorizer: auth,
        authorizationType: apigateway.AuthorizationType.COGNITO,
      }
    });
    auth._attachToApi(frontend_api);
    frontend_api.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    const apiDomain = frontend_api.addDomainName('frontend-domain-name', {
      domainName: domain,
      securityPolicy: apigateway.SecurityPolicy.TLS_1_2,
      certificate: cert,
    });
    apiDomain.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // Create an A record for the API root; this is required, otherwise Cognito
    // will fail to validate via DNS that I do indeed own my endpoint.
    const record = new route53.ARecord(this, 'api-domain-record', {
      recordName: domain,
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.ApiGateway(frontend_api))
    });
    record.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // add policy to browser role
    browser_client_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
	  resources: [python_frontend_lambda.functionArn],
	  actions: ['lambda:InvokeFunction'] 
	}));
    browser_client_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: [frontend_api.arnForExecuteApi()],
      actions: ['execute-api:*'],
    }));
  }
}
