from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Stack,
    RemovalPolicy,
    aws_cloudfront as cf,
    aws_s3 as s3
)

# Replace the value with your IAM server certificate ID.
iam_cert_id = 'YOUR_CERTIFICATE_ID'

# Replace the value with your alternate domain names for the cloudfront distribution
cname = ['www1.example.com.cn', 'www2.example.com.cn']


class CloudfrontInChinaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(
            self, 'S3OriginBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        oai = cf.OriginAccessIdentity(self, 'MyOriginAccessIdentity')
        oai.apply_removal_policy(RemovalPolicy.DESTROY)
        s3_bucket.grant_read(oai)
        oai_id = 'origin-access-identity/cloudfront/{}'.format(oai.origin_access_identity_id)

        cf_distribution = cf.CfnDistribution(
            self, 'MyCloudfrontDistribution',
            distribution_config=cf.CfnDistribution.DistributionConfigProperty(
                # Create cache behaviors with legacy cache settings
                default_cache_behavior=cf.CfnDistribution.DefaultCacheBehaviorProperty(
                    target_origin_id=s3_bucket.bucket_name,
                    viewer_protocol_policy='redirect-to-https',
                    compress=True,
                    forwarded_values=cf.CfnDistribution.ForwardedValuesProperty(
                        query_string=False
                    )
                ),
                enabled=True,
                aliases=cname,
                default_root_object='index.html',
                http_version='http2',
                ipv6_enabled=False,
                origins=[
                    cf.CfnDistribution.OriginProperty(
                        id=s3_bucket.bucket_name,
                        domain_name=s3_bucket.bucket_regional_domain_name,
                        s3_origin_config=cf.CfnDistribution.S3OriginConfigProperty(
                            origin_access_identity=oai_id
                        )
                    )
                ],
                viewer_certificate=cf.CfnDistribution.ViewerCertificateProperty(
                    iam_certificate_id=iam_cert_id,
                    minimum_protocol_version='TLSv1.2_2021',
                    ssl_support_method='sni-only'
                )
            )
        )

        CfnOutput(self, 'BucketName', value=s3_bucket.bucket_name)
        CfnOutput(self, 'BucketDomainName', value=s3_bucket.bucket_domain_name)
        CfnOutput(self, 'BucketRegionalDomainName', value=s3_bucket.bucket_regional_domain_name)
        CfnOutput(self, 'DistributionId', value=cf_distribution.attr_id)
