## AWS CDK demo: deploy Amazon CloudFront Distributions in AWS China Regions

### Prerequisites

CloudFront in China currently does not support ACM for managing SSL/TLS certificates. Instead, you need to obtain an SSL/TLS certificate from a third-party certificate authority (CA) and upload it to the IAM certificate store in your account for AWS China Regions. See [Managing server certificates in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html) in the AWS Identity and Access Management User Guide for more details.

### What the demo will do:

* Create an Amazon S3 bucket in AWS China (Beijing) Region
* Create an Origin Access Identity (OAI) and grant the Amazon S3 bucket access to CloudFront with the OAI
* Create a CloudFront distribution with a default cache behavior pointing to the Amazon S3 Origin, and an IAM server certificate association (we assume that you already have the server certificate ID)

This demo provides AWS CDK code in two languages, Python and TypeScript, placed in `Python/` and `TypeScript/` directories separately.

#### Deploy the demo in TypeScript

Modify the value of `iamCertId` and `cname` in `lib/cloudfront_in_china_stack.py`

```TypeScript
// Replace the value with your IAM server certificate ID.
const iamCertId:string = 'YOUR_CERTIFICATE_ID';

// Replace the value with your alternate domain names for the cloudfront distribution
const cname = ['www1.example.com.cn', 'www2.example.com.cn'];
```

Enter the `TypeScript/` directory, install the dependencies, deploy the CDK stack.

```Bash
npm install
cdk synth
cdk bootstrap aws://<YOUR_AWSCN_ACCOUNT_ID>/cn-north-1
cdk deploy
```

#### Deploy the demo in Python

Modify the value of `iam_cert_id` and `cname` in `lib/cloudfront_in_china_stack.py`

```python
# Replace the value with your IAM server certificate ID.
iam_cert_id = 'YOUR_CERTIFICATE_ID'

# Replace the value with your alternate domain names for the cloudfront distribution
cname = ['www1.example.com.cn', 'www2.example.com.cn']
```

Enter the `Python/` directory, install the dependencies, deploy the CDK stack.

```Bash
pip install -r requirements.txt
cdk synth
cdk bootstrap aws://<YOUR_AWSCN_ACCOUNT_ID>/cn-north-1
cdk deploy
```

### Clean up

To delete the deployed resources, run the `cdk destroy` command from the stack directory.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

