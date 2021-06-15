# EC2-RStudio-Server* on AWS Service Workbench
*RStudio with Application Load Balancer (ALB)

Researchers use RStudio very commonly in their day to day efforts. While RStudio is a popular product, the process of installing RStudio securely on AWS Cloud and using it in a cost effective manner is a non-trivial task specially for Researchers. With AWS SWB the goal is to make this process very simple, secure and cost effective for Researchers so that they can focus on “Science” and not “Servers” thereby increasing their productivity.
  
  ![image](https://user-images.githubusercontent.com/73109773/120605679-f7086780-c46b-11eb-9b50-8bfe546e6094.png)

 
EC2-RStudio-Server on Service Workbench is a comprehensive solution with an Application Load Balancer (ALB).  While launched through SWB Workspaces 
the ALB is shared between multiple RStudio instances within same AWS account. Using ALB, secure access to each RStudio instance over unique 
presigned URL.

  ![image](https://user-images.githubusercontent.com/73109773/119657685-d62b8b00-be49-11eb-9618-95dfd8d7bea6.png)

## Key Features
Below are a few key features of EC2-RStudio-Server 
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
* Before deploying EC2-RStudio-Server, create Service Workbench with a custom domain associated with SSL certificate.
   * The current implementation assigns hostnames to RStudio instances with the form rstudio-$env.$domain_name where $env is the environment identifier for the workspace, and $domain_name is the custom domain used for Service Workbench. This means that all certificates (the private key and the certificate chain mentioned above) must be for the wildcard (*.$domain_name). Failing to do so would cause nginx to not start in the EC2 instance that is backing the RStudio environment. You could also check if nginx setup is successful by running "systemctl restart nginx" on this EC2 instance.

   * This also means that Service Workbench must be deployed with a custom domain for RStudio to work properly. In order to configure your custom domain name, please override and specify the following config settings in your main/config/settings/$stage.yml file:

   * domainName
   * certificateArn
   * hostedZoneId
* Generate a new SSL Certificate for the Hosting accounts in AWS.
 

For detailed steps on prerequisites [Click here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/prerequisites/prerequisite.md)

### Implementation
* Refer to the Implementation [guide] to deploy EC2-RStudio-Server.
* To deploy EC2-RStudio-Server, you will have to add EC2-RStudio-Server CFT as a product in SWB Service Catalog

### Configuration
* Post adding EC2-RStudio-Server CFT to SWB Service Catalog product portfolio do the following steps:
    1. Login to SWB as admin.
    2. Navigate to Workspace Types to import EC2-RStudio-Server.
    3. Configure EC2-RStudio-Server with input parameters.
    
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
       
    4. Launch EC2-RStudio-Server Workspace to provision an RStudio Server. 

## New Customer Registration for RStudio with ALB 
As part of an ongoing collaboration with AWS SWB teams, we expect customers would need help with implementation, support, and ongoing enhancements of the above solution. Kindly register with Relevance Lab to get these benefits. 


[![download](https://user-images.githubusercontent.com/64137641/121536646-e2eed800-ca20-11eb-8853-e24ced0fe622.jpg)](https://gd1.relevancelab.com/aws-service-workbench/#Contact%20us)
