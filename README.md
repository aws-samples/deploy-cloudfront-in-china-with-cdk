## AWS CDK demo: deploy Amazon CloudFront Distributions in AWS China Regions

AWS offers China Regions (Beijing and Ningxia) allowing customers to host websites and applications that serve the Chinese market. While the China Regions provide the same foundational services like CloudFront and S3, there are some key differences compared to other AWS Regions that can trip up customers trying to automate deployments. This is a CDK sample code that creates CloudFront distributions in AWS China using the SDK & CDK while accounting for the nuances of this region. It can help you set up a repeatable deployment pipeline to launch CloudFront in China to accelerate delivery of your site and keep your Chinese users happy.

### Prerequisites

Amazon CloudFront in the China Regions currently does not support Amazon Certificate Manager for managing SSL/TLS certificates. Therefore, before we get started, we need to upload the TLS certificate to AWS IAM and specify a certificate name.

### Specify the TLS certificate name and the CNAMEs

Modify the value of `ServerCertificateName` and `cname` in `lib/cloudfront_in_china_stack.py`

```python
# Read the certificate id from IAM cert store
my_cert = iam_client.get_server_certificate(
    ServerCertificateName='example.com_01'      # Replace example.com_01 with your certificate name.
)
server_cert_id = my_cert['ServerCertificate']['ServerCertificateMetadata']['ServerCertificateId']

# Input your alternate domain names for the cloudfront distribution here
cname = ['www1.example.com.cn', 'www2.example.com.cn']
```

### Deploy resources in Beijing Region

```python
pip install -r requirements.txt
cdk synth
cdk bootstrap aws://<YOUR_AWSCN_ACCOUNT_ID>/cn-north-1
cdk deploy
```

### Clean up

```python
cdk destroy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

