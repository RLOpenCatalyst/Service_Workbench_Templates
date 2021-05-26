# RStudio with ALB on AWS Service Workbench

  ![image](https://user-images.githubusercontent.com/73109773/119454257-fbd76800-bd55-11eb-8292-cb2533e549a0.png)

RStudio on Service Workbench is a comprehensive solution with an Application Load Balancer (ALB), while launched through SWB
Workspaces the ALB is shared between multiple RStudio instances within same AWS account. Using ALB further secures access to each RStudio over unique 
Presigned URL.

  ![image](https://user-images.githubusercontent.com/73109773/119454593-5375d380-bd56-11eb-89fb-cf11328ed468.png)

## Key Features
Below are a few key features of RStudio with Application Load Balancer (ALB)
*	The shared AWS ALB (Application Load Balancer) used with AWS ACM certificates for each Hosting Account simplifies the Certificate Management Lifecycle.
*	Using unique self-signed certificate to encrypt between ALB and RStudio EC2 to ensure secure connection, thus enabling encrypt connection per RStudio.
*	ALB Listener Rules leveraged to ensure secure access only to allowed CIDR blocks in case of compromised / shared RStudio URL.

## Getting Started
To prepare and launch RStudio V2, refer to prerequisites [here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/Prerequisite/prerequisite.md) and
* Refer to the Implementation [guide] to deploy RStudio V2
* To deploy RStudio V2 (with ALB) the SWB Service Catalog product portfolio needs to be added with RStudio V2 Cloud Formation Template, available [here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/ec2-rlrstudio.yaml)
* Having added RStudio V2 Cloud Formation Template to SWB Service Catalog product portfolio, login to SWB, navigate to Worksapce Types to import and configure RStuido V2 with Input Parameters.
### Launch Solution
Having gone through the preceding steps, here’s an AWS CloudFormation template so that you can quickly and easily deploy this infrastructure in your own 
AWS Cloud environment.

[![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=rlrstudio&templateURL=https://rlswb.s3.amazonaws.com/ec2-rlrstudio.yaml)

