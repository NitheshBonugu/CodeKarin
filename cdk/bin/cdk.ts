#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CognitoStack } from '../lib/cognito-stack';
import { frontend_CdkStack } from '../lib/frontend_cdk-stack';
import { backend_CdkStack } from '../lib/backend_cdk-stack';
import { client_CdkStack } from '../lib/client_cdk-stack';

const app = new cdk.App();

// The Cognito managed CloudFront endpoint must exist in us-east-1, so this stack
// does, too. This stack reuses a pre-existing hosted zone.
new CognitoStack(app, 'CognitoStack', {
  env: {
    account: '200015229140',
    region: 'us-east-1', // Has to be in US-EAST-1 because CloudFront
  },
  hostedZoneAttributes: {
    zoneName: 'codekarin.com',
    hostedZoneId: 'Z0467455OW4YWWROH92Y',
  },
  parentDomain: 'codekarin.com',
  subdomain: 'auth',
});

new backend_CdkStack(app, 'backend-CDK-Stack', {
  env: { 
    account: '200015229140', 
    region: 'us-west-2' 
  },
  stackName: 'KarinVirtualClassroomBackend',
  description: 'This stack is designed to instantiate and build AWS cloud resources related to the Karin Virtual Classroom teaching tool backend',
  terminationProtection: false, // allow stack to be terminated by admin from CLI
  
});

new frontend_CdkStack(app, 'frontend-CDK-Stack', {
  env: { 
    account: '200015229140', 
    region: 'us-west-2' 
  },
  hostedZoneAttributes: {
    zoneName: 'codekarin.com',
    hostedZoneId: 'Z0467455OW4YWWROH92Y',
  },
  parentDomain: 'codekarin.com',
  subdomain: 'api',
  stackName: 'KarinVirtualClassroomFrontend',
  description: 'This stack is designed to instantiate and build AWS cloud resources related to the Karin Virtual Classroom teaching tool frontend',
  terminationProtection: false, // allow stack to be terminated by admin from CLI
});

new client_CdkStack(app, 'client-CDK-Stack', {
  env: { 
    account: '200015229140', 
    region: 'us-west-2' 
  },
  hostedZoneAttributes: {
    zoneName: 'codekarin.com',
    hostedZoneId: 'Z0467455OW4YWWROH92Y',
  },
  parentDomain: 'codekarin.com',
  stackName: 'KarinVirtualClassroomClient',
  description: 'This stack is designed to instantiate and build AWS cloud resources related to the Karin Virtual Classroom teaching tool frontend',
  terminationProtection: false, // allow stack to be terminated by admin from CLI
});
