#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CloudfrontInChinaStack } from '../lib/cloudfront-in-china-stack';

const app = new cdk.App();
new CloudfrontInChinaStack(app, 'CloudfrontInChinaStack');
