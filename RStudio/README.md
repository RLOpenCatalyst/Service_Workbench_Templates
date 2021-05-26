# RStudio V2* on AWS Service Workbench
*RStudio with Application Load Balancer (ALB)

Researchers use RStudio very commonly in their day to day efforts. While RStudio is a popular product, the process of installing RStudio securely on AWS Cloud and using it in a cost effective manner is a non-trivial task specially for Researchers. With AWS SWB the goal is to make this process very simple, secure and cost effective for Researchers so that they can focus on “Science” and not “Servers” thereby increasing their productivity.

  ![image](https://user-images.githubusercontent.com/73109773/119454257-fbd76800-bd55-11eb-8292-cb2533e549a0.png)

RStudio V2 on Service Workbench is a comprehensive solution with an Application Load Balancer (ALB).  While launched through SWB
Workspaces the ALB is shared between multiple RStudio instances within same AWS account. Using ALB, secure access to each RStudio instance over unique 
presigned URL.

  ![image](https://user-images.githubusercontent.com/73109773/119454593-5375d380-bd56-11eb-89fb-cf11328ed468.png)

## Key Features
Below are a few key features of RStudio V2 
*	The shared AWS ALB used with AWS ACM certificates for each Hosting Account simplifies the Certificate Management Lifecycle.
*	Use unique self-signed certificate to encrypt ALB and RStudio EC2 to ensure secure connection, thus enabling encrypted connection per RStudio.
*	ALB listener rules leveraged to ensure secure access only to allowed CIDR blocks in case of compromised / shared RStudio URL.

## Getting Started
### Prerequisite
* Before deploying RStudio V2, create Service Workbench with a custom domain associated with SSL certificate. 
* Generate a new SSL Certificate in AWS
* Update the root domain record pointing to custom domain, update the Route53 DNS records, Nameservers of newly created Hosted Zone. 

For detailed steps on prerequisites [Click here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/Prerequisite/prerequisite.md)

### Implementation
* Refer to the Implementation [guide] to deploy RStudio V2
* To deploy RStudio V2, the SWB Service Catalog product portfolio needs to be added with RStudio V2 Cloud Formation Template, [Click here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/ec2-rlrstudio.yaml)

### Configuration
* Post adding RStudio V2 Cloud Formation Template to SWB Service Catalog product portfolio do the following steps:
    1. Login to SWB as admin
    2. Navigate to Workspace Types to import RStudio V2 
    3. Configure RStuido V2 with Input Parameters.
    4. Launch Workspace Rstudio V2 to provision an RStudio Server

### Launch Solution
Having gone through the preceding steps, here’s an AWS CloudFormation template so that you can quickly and easily deploy this infrastructure in your own 
AWS Cloud environment.

[![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=rlrstudio&templateURL=https://rlswb.s3.amazonaws.com/ec2-rlrstudio.yaml)

