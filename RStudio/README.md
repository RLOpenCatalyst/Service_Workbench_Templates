# RStudio v2* on AWS Service Workbench
*RStudio with Application Load Balancer (ALB)

Researchers use RStudio very commonly in their day to day efforts. While RStudio is a popular product, the process of installing RStudio securely on AWS Cloud and using it in a cost effective manner is a non-trivial task specially for Researchers. With AWS SWB the goal is to make this process very simple, secure and cost effective for Researchers so that they can focus on “Science” and not “Servers” thereby increasing their productivity.
  
  ![image](https://user-images.githubusercontent.com/73109773/120605679-f7086780-c46b-11eb-9b50-8bfe546e6094.png)

 
RStudio v2 on Service Workbench is a comprehensive solution with an Application Load Balancer (ALB).  While launched through SWB Workspaces 
the ALB is shared between multiple RStudio instances within same AWS account. Using ALB, secure access to each RStudio instance over unique 
presigned URL.

  ![image](https://user-images.githubusercontent.com/73109773/119657685-d62b8b00-be49-11eb-9618-95dfd8d7bea6.png)

## Key Features
Below are a few key features of RStudio v2 
*	The shared AWS ALB used with AWS ACM certificates for each Hosting Account simplifies the Certificate Management Lifecycle.
*	Use unique self-signed certificate to encrypt ALB and RStudio EC2 to ensure secure connection, thus enabling encrypted connection per RStudio.
           
## RStudio AMI
* The current Rstudio AMI is embedded with a user provided certificate and key for the custom domain. The new design will eliminate the need for those 
and bake the AMI with self signed certificates. The self signed certificates are used to encrypt only the traffic between ALB and EC2.
The AMI is also packed with additional R packages that are commonly used by the researchers.
    
    |RStudio Server Version | 
    |-----------------------| 
    |      1.3.959          | 
    
            
    | Additional Packages Installed |
    | ------------------------------|
    |      tidyverse                |
    |      devtools                 |
    |      kableExtra               |
    |      survival                 |
    |      survminer                |
    |      MASS                     |
    |      quantreg                 |
    |      DescTools                |
    
     
## Getting Started
### Prerequisite
* Before deploying RStudio v2, create Service Workbench with a custom domain associated with SSL certificate.
   * The current implementation assigns hostnames to RStudio instances with the form rstudio-$env.$domain_name where $env is the environment identifier for the workspace, and $domain_name is the custom domain used for Service Workbench. This means that all certificates (the private key and the certificate chain mentioned above) must be for the wildcard (*.$domain_name). Failing to do so would cause nginx to not start in the EC2 instance that is backing the RStudio environment. You could also check if nginx setup is successful by running "systemctl restart nginx" on this EC2 instance.

   * This also means that Service Workbench must be deployed with a custom domain for RStudio to work properly. In order to configure your custom domain name, please override and specify the following config settings in your main/config/settings/$stage.yml file:

   * domainName
   * certificateArn
   * hostedZoneId
* Generate a new SSL Certificate for the Hosting accounts in AWS.
 

For detailed steps on prerequisites [Click here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/prerequisites/prerequisite.md)

### Implementation
* Refer to the Implementation [guide] to deploy RStudio v2.
* To deploy RStudio v2, will have to add RStudio v2 CFT as a product in SWB Service Catalog, click on the Launch Stack to upload RStudio v2 CFT.

[![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=rlrstudio&templateURL=https://gitrstudiocft.s3.amazonaws.com/v2upldtosc)

### Configuration
* Post adding RStudio v2 CFT to SWB Service Catalog product portfolio do the following steps:
    1. Login to SWB as admin.
    2. Navigate to Workspace Types to import RStudio v2.
    3. Configure RStudio v2 with input parameters.
    
       | Name         |   Notes      |
       | ------------- | ------------- |
       | AccessFromCIDRBlock  | The CIDR used to access the ec2 instances  |
       | AmiId  | Amazon Machine Image for the EC2 instance  |
       | EncryptionKeyArn | The ARN of the KMS encryption Key used to encrypt data in the instance |
       | EnvironmentInstanceFiles | An S3 URI (starting with "s3://") that specifies the location of files to be copied to the environment instance, including any bootstrap scripts |
       | IamPolicyDocument | The IAM policy to be associated with the launched workstation |
       | InstanceType | EC2 instance type to launch |
       | KeyName  | Keypair name for SSH access |
       | Namespace | An environment name that will be prefixed to resource names |
       | S3Mounts | A JSON array of objects with name, bucket, and prefix properties used to mount data |
       | Subnet | The VPC subnet in which the EC2 instance will reside |
       | VPC | The VPC in which the EC2 instance will reside |
       | ACMSSLCertARN | The ARN of the AWS Certificate Manager SSL Certificate to associate with the Load Balancer |
       
    4. Launch Rstudio v2 Workspace to provision an RStudio Server. 

## New Customer Registration for RStudio with ALB 
Customers who chose to download and use RStudiov2 can register themselves by providing the details for notifications on Patches, Updates.
They can do so by 
1. Sending an email to rlcloudsupport@relevancelab.com or 
2. Log into portal https://serviceone@relevancelab.com or
3. Submit form on https://relevancelab.com/aws-cloud/
