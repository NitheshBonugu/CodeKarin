import { Duration, RemovalPolicy, Stack, StackProps, CfnOutput } from '@aws-cdk/core'
import * as acm from '@aws-cdk/aws-certificatemanager';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as cognito from '@aws-cdk/aws-cognito';
import * as lambda from '@aws-cdk/aws-lambda';
import * as route53 from '@aws-cdk/aws-route53';
import * as targets from '@aws-cdk/aws-route53-targets';
import { Construct } from 'constructs';

import * as path from 'path';

interface CognitoStackProps extends StackProps {
  hostedZoneAttributes: route53.HostedZoneAttributes;
  parentDomain: string;
  subdomain: string;
}

export class CognitoStack extends Stack {
  constructor(scope: Construct, id: string, props: CognitoStackProps) {
    super(scope, id, props);

/// NEW CLEAN COFIG

	// This is the subdomain on the root API where all auth management resources will
    // be created.
    const domain = `${props.subdomain}.${props.parentDomain}`;

    // This is the subdomain of the root subdomain, where the Cognito managed login
    // page will be reachable internally. It must be done like this to work around
    // compatibility constraints between CloudFormation / Cognito / Route53.
    const cloudfrontDomain = `login.${domain}`;

    // Reference existing hosted zone
    const hostedZone = route53.HostedZone.fromHostedZoneAttributes(this, 'hosted-zone',
      props.hostedZoneAttributes
    );

    // Create a managed DNS certificate; necessary for associating a record with Cognito's
    // managed CloudFront endpoint. The certificate covers both the `domain` and the
    // `cloudfrontDomain` because we need both for endpoint validation, so might as well
    // put them both under one certificate.
    const cert = new acm.Certificate(this, 'public-certificate', {
      domainName: domain,
      subjectAlternativeNames: [ cloudfrontDomain ],
      validation: acm.CertificateValidation.fromDns(hostedZone),
    });
    cert.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // Lambda handler for the `props.parentDomain` API; currently, this just returns a string
    // indicating the page is not supported. In the future, it may be replaced by an actual
    // API to serve a remote management cosnole or something.

    var rootLambda = new lambda.Function(this, 'lambda', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(path.join(__dirname, '../lib/handler')),
      handler:'index.lambda_handler',
      timeout: Duration.seconds(10),
      logRetention: 5,
    });
    rootLambda.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // `props.parentDomain` API; currently, this isn't used for anything helpful, but since we
    // need an endpoint + A record route to setup Cognito endpoints, that implies we also need
    // an API to route for the root domain. In the future, this may be replaced by an actual
    // API to serve a remote management cosnole or something.
    const api = new apigateway.RestApi(this, `root-gateway`, {
      description: 'This fronts the root domain for a reusable Cognito-based auth mechanism.',
      deploy: true,
      endpointTypes: [apigateway.EndpointType.EDGE],
    });
    api.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // Route the root Lambda to the API root
    api.root.addMethod('GET', new apigateway.LambdaIntegration(rootLambda, {
      requestTemplates: { 'application/json': '{ "statusCode": "200" }' }
    }));

    // Create a custom domain for the API so we can route an A record to it
    const apiDomain = api.addDomainName('root-domain-name', {
      domainName: domain,
      certificate: cert,
    });
    apiDomain.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // Create an A record for the API root; this is required, otherwise Cognito
    // will fail to validate via DNS that I do indeed own my endpoint.
    const record = new route53.ARecord(this, 'root-domain-alias', {
      recordName: domain,
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.ApiGateway(api))
    });
    record.applyRemovalPolicy(RemovalPolicy.DESTROY);

        // Create the Cognito User Pool
    // following this: https://aws.amazon.com/getting-started/hands-on/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/module-2/
    const userPool = new cognito.UserPool(this, 'user-pool', {
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY, // TODO: make this configurable (including imposed API limitations for which are allowed when)
      // autoVerify: ,
      // customAttributes: , // TODO: make this configurable
      // customSenderKmsKey: new kms.Key(this, 'test-user-pool-sender-key', {
      //   enableKeyRotation: true,
      //   enabled: true,
      // }),
      deviceTracking: {
        challengeRequiredOnNewDevice: true,
        deviceOnlyRememberedOnUserPrompt: true,
      },
      // email: cognito.UserPoolEmail.withSES({ // requires additional setup
      //   fromEmail: 'noreply@' + props.domainProps.domainName,
      //   fromName: 'Test Serverless App',
      // }),
      enableSmsRole: false, // may not be necessary
      // lambdaTriggers: ,
      mfa: cognito.Mfa.OPTIONAL,
      // mfaMessage: ,
      mfaSecondFactor: {
        sms: false,
        otp: true,
      },
      passwordPolicy: { // TODO: make this configurable
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
        tempPasswordValidity: Duration.days(1),
      },
      removalPolicy: RemovalPolicy.DESTROY, // change this in prod
      signInAliases: { // TODO: make this configurable
        username: true,
        email: true,
        phone: false,
        preferredUsername: true,
      },
      signInCaseSensitive: true,
      // smsRole: ,
      // smsRoleExternalId: ,
      // standardAttributes: , // TODO: make this configurable
      // userInvitation: , // TODO: make this configurable
      // userPoolName: ,
      userVerification: { // TODO: make this configurable
        emailSubject: 'Verify your email for codekarin!',
        emailBody: 'Thanks for signing up to codekarin! Your verification code is {####}',
        emailStyle: cognito.VerificationEmailStyle.CODE,
        smsMessage: 'Thanks for signing up to codekarin! Your verification code is {####}',
      },
    });

    const user_pool_arn_output = new CfnOutput(this, 'UserPoolArn', { value:  userPool.userPoolArn, exportName: 'UserPoolArn'});

    const client = userPool.addClient('cognito-client', {
    	oAuth: {
      	  flows: {
      	    authorizationCodeGrant: true,
      	  },
      	  scopes: [ cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE, cognito.OAuthScope.COGNITO_ADMIN ],
      	  callbackUrls: [ 'https://codekarin.com/home'],
      	  logoutUrls: [ 'https://codekarin.com/logout']
      	},
    });

    // Associate the managed Cognito CloudFront endpoint with the custom domain
    const customDomain = userPool.addDomain('custom-domain', {
      customDomain: {
        domainName: cloudfrontDomain,
        certificate: cert,
      },
    });

    // Cognito verifies the custom `domain` it will be mapping is owned by verifying
    // there's an A record on the `props.parentDomain`. This line explicitly ensures
    // the record exists before CloudFormation attempts to create the custom domain.
    customDomain.node.addDependency(record);

    // Route the internal `domain` to the CloudFront managed endpoint
    new route53.CnameRecord(this, 'cloudfront-route', {
      domainName: customDomain.cloudFrontDomainName,
      zone: hostedZone,
      recordName: cloudfrontDomain,
    });
  }
}
