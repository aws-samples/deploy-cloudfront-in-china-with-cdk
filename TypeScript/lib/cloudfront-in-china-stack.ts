import {CfnOutput, RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import * as cf from 'aws-cdk-lib/aws-cloudfront';
import * as s3 from 'aws-cdk-lib/aws-s3';
import {Construct} from 'constructs';

// Replace the value with your IAM server certificate ID.
const iamCertId:string = 'YOUR_CERTIFICATE_ID';

// Replace the value with your alternate domain names for the cloudfront distribution
const cname = ['www1.example.com.cn', 'www2.example.com.cn'];

export class CloudfrontInChinaStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const s3Bucket = new s3.Bucket(this, 'S3OriginBucket', {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    const oai = new cf.OriginAccessIdentity(this, 'MyOriginAccessIdentity');
    oai.applyRemovalPolicy(RemovalPolicy.DESTROY);
    s3Bucket.grantRead(oai);
    const oaiId = `origin-access-identity/cloudfront/${oai.originAccessIdentityId}`;

    const cfDistribution = new cf.CfnDistribution(this, 'MyCloudfrontDistribution', {
      distributionConfig: {
        defaultCacheBehavior: {
          targetOriginId: s3Bucket.bucketName,
          viewerProtocolPolicy: 'redirect-to-https',
          compress: true,
          forwardedValues: {
            queryString: false,
          },
        },
        enabled: true,
        aliases: cname,
        defaultRootObject: 'index.html',
        httpVersion: 'http2',
        ipv6Enabled: false,
        origins: [
          {
            id: s3Bucket.bucketName,
            domainName: s3Bucket.bucketRegionalDomainName,
            s3OriginConfig: {
              originAccessIdentity: oaiId,
            },
          },
        ],
        viewerCertificate: {
          iamCertificateId: iamCertId,
          minimumProtocolVersion: 'TLSv1.2_2021',
          sslSupportMethod: 'sni-only',
        },
      },
    });

    new CfnOutput(this, 'BucketName', {value: s3Bucket.bucketName});
    new CfnOutput(this, 'BucketDomainName', {value: s3Bucket.bucketDomainName});
    new CfnOutput(this, 'BucketRegionalDomainName', {value: s3Bucket.bucketRegionalDomainName});
    new CfnOutput(this, 'DistributionId', {value: cfDistribution.attrId});
  }
}