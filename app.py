#!/usr/bin/env python3

import aws_cdk as cdk

from lib.cloudfront_in_china_stack import CloudfrontInChinaStack


app = cdk.App()
CloudfrontInChinaStack(app, "cdk")

app.synth()
