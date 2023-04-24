import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as _lambda from '@aws-cdk/aws-lambda';
import * as s3 from '@aws-cdk/aws-s3';
import * as ecs from '@aws-cdk/aws-ecs';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as ecr from '@aws-cdk/aws-ecr';
import { DockerImageAsset } from '@aws-cdk/aws-ecr-assets';
import * as ecsPatterns from '@aws-cdk/aws-ecs-patterns';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as cognito from '@aws-cdk/aws-cognito';
import * as route53 from '@aws-cdk/aws-route53';
import * as targets from '@aws-cdk/aws-route53-targets';
import * as acm from '@aws-cdk/aws-certificatemanager';
import * as cloudfront from '@aws-cdk/aws-cloudfront';
import * as waf from '@aws-cdk/aws-waf';
import { LoadBalancerV2Origin } from '@aws-cdk/aws-cloudfront-origins';
import * as fs from 'fs';

interface ClientStackProps extends cdk.StackProps {
  hostedZoneAttributes: route53.HostedZoneAttributes;
  parentDomain: string;
}

// CLIENT
export class client_CdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: ClientStackProps) {
    super(scope, id, props);

    const table_arn_list_input = cdk.Fn.importValue('TableArnList');
    const table_arn_list = table_arn_list_input.split(",")
    const python_frontend_lambda_arn = cdk.Fn.importValue('FrontendLambdaArn');

    const browser_client_role_name = cdk.Fn.importValue('ClientRoleName');

    const domain = `${props.parentDomain}`;

    const browser_client_role = iam.Role.fromRoleName(this, 'browser_role', browser_client_role_name)

    const hostedZone = route53.HostedZone.fromHostedZoneAttributes(this, 'hosted-zone',
      props.hostedZoneAttributes
    );

    const cert = new acm.Certificate(this, 'parent-api-certificate', {
      domainName: domain,
      subjectAlternativeNames: [],
      validation: acm.CertificateValidation.fromDns(hostedZone),
    });
    cert.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // VPC [ECS public hosted, Lambda / DynamoDB / S3 access privately hosted, security group definitions, ACL definitions, NAT, IGW]
    const vpc_resource = new ec2.Vpc(this, 'Karin-Web-Vpc', { 
      maxAzs: 2,
    });

    const web_instance_sg = new ec2.SecurityGroup(this, 'web_instance_sg', {
      vpc: vpc_resource,
      description: 'Allow https access to ec2 instances',
      allowAllOutbound: true   // Can be set to false
    });
    web_instance_sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'HTTPS from anywhere');
    web_instance_sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'HTTP from anywhere');
    web_instance_sg.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    // ECS (Fargate) [front-end HTTP cluster w/ application load balancer]
    const cluster = new ecs.Cluster(this, 'Karin-Web-FargateCluster', { vpc: vpc_resource });

    const docker_webserver_image = new DockerImageAsset(this, 'docker_webserver_image', {
      directory: '../react-webserver',
      file:'./Dockerfile'
    });
    // const docker_webserver_repo = ecr.Repository.fromRepositoryName(this, 'docker_webserver_repo', 'docker-react-webserver');

    // Load Balanced Fargate Service
    const loadBalancedFargateService = new ecsPatterns.ApplicationLoadBalancedFargateService(this, 'Karin-Web-Service', {
      assignPublicIp: true,
      cluster: cluster,
      memoryLimitMiB: 2048,
      desiredCount: 1,
      cpu: 1024,
      domainName: domain,
      domainZone: hostedZone,
      certificate: cert,
      taskImageOptions: {
        image: ecs.ContainerImage.fromDockerImageAsset(docker_webserver_image),
        containerPort: 443,
        executionRole: browser_client_role,
        taskRole: browser_client_role
      },
      listenerPort: 443,
      openListener: true,
      publicLoadBalancer: true,
      securityGroups: [web_instance_sg],
    });

    const record = new route53.ARecord(this, 'Karin-Web-Service-DNS', {
      recordName: 'webserver',
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.LoadBalancerTarget(loadBalancedFargateService.loadBalancer)),
      ttl: cdk.Duration.minutes(1)
    });
    record.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    var healthcheckEndpoint = "/health";

    loadBalancedFargateService.targetGroup.configureHealthCheck({
      port: '443',
      path: healthcheckEndpoint,
    });
  
    // add policy to browser role
    browser_client_role.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: [python_frontend_lambda_arn],
      actions: ['lambda:*'],
    }));
  }
}
