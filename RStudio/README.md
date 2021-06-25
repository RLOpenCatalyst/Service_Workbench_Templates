# EC2-RStudio-Server* for Service Workbench on AWS
*RStudio with Application Load Balancer (ALB)

Researchers commonly use RStudio in their day-to-day efforts. While RStudio is a popular product, the process of installing RStudio securely on AWS Cloud and using it in a cost-effective manner is a non-trivial task, especially for Researchers. With Service Workbench on AWS (SWB), the goal is to make this process very simple, secure, and cost-effective for Researchers so that they can focus on “Science” and not “Servers” thereby increasing their productivity.

  
  ![image](https://user-images.githubusercontent.com/73109773/120605679-f7086780-c46b-11eb-9b50-8bfe546e6094.png)

 
EC2-RStudio-Server on Service Workbench is a comprehensive solution with an Application Load Balancer (ALB). When launched through SWB Workspaces, the ALB is shared between multiple RStudio instances within the same AWS account. Using ALB, secure access to each RStudio instance over a unique presigned URL.

  ![RStudio-Accesibility-Architecture](https://user-images.githubusercontent.com/58428150/123269798-f324ae00-d51c-11eb-9a47-3ebe37ccecc6.jpg)

## Key Features
Below are a few key features of EC2-RStudio-Server 
*	Latest version of RStudio Server (1.4.1717)
*	Commonly used packages pre-installed
*	Easy connection to the instance using a pre-authenticated URL launched from within Service Workbench
*	Secure SSL connection to RStudio Server using Amazon issued certificates managed in AWS Certificate Manager (ACM)
*	Shared AWS Application Load-balancer (ALB) used with AWS ACM certificates for each Hosting Account simplifies the Certificate Management Lifecycle.
*	Use unique self-signed certificate to encrypt traffic between ALB and RStudio EC2 to ensure secure connection from end to end.
           
## RStudio AMI
* The Rstudio AMI bundled with SWB is embedded with a user-provided certificate and key for the custom domain. The new design will eliminate the need for those and bake the AMI with self-signed certificates. The self-signed certificates are used to encrypt only the traffic between ALB and EC2. The AMI is also packed with additional R packages that are commonly used by the researchers.
    
    | RStudio Server Version | R Version  |
    |------------------------|------------| 
    |      1.4.1717          |   3.6.3    |
    
            
    | Packages Installed            |  Version |          Description                                |
    | ------------------------------|----------|-----------------------------------------------------|
    | [tidyverse](https://www.tidyverse.org/)|    1.3.1 | Performs subsetting, transforming, visualizing with data                                                                     |
    | [devtools](https://www.r-project.org/nosvn/pandoc/devtools.html)|    2.4.0 | Provides R functions that simplifies many common tasks                                                                     |
    | [kableExtra](https://cran.r-project.org/web/packages/kableExtra/index.html)|    1.3.4 | Helps you build common complex tables and manipulate table style                                                        |
    | [survival](https://cran.r-project.org/web/packages/survival/index.html) |   3.2.10 | Helps you to do survival analysis |
    | [survminer](https://cran.r-project.org/web/packages/survminer/readme/README.html)                |    0.4.9 | Provides functions for facilitating survival analysis and visualization                                                    |
    | [MASS](https://cran.r-project.org/web/packages/MASS/index.html) | 7.3.53.1 | Common library loads the package MASS (for Modern Applied Statistics with S) into memory                                  |
    | [quantreg](https://cran.r-project.org/web/packages/quantreg/index.html) |     5.85 | Performs estimation and inference on the conditional quantile function, its first derivative, and its second derivative over a region of covariate values and/or quantile indices                                      |
    | [DescTools](https://cran.r-project.org/web/packages/DescTools/index.html)|  0.99.41 | It's an extensive collection of miscellaneous basic statistics functions and comfort wrappers not available in the R basic system |
    
     
## Getting Started
### Prerequisite
* For detailed steps on prerequisites [click here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/prerequisites/prerequisite.md)

### Implementation
* Refer to the Implementation [guide](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/tree/main/RStudio/machine-images/config/infra/README.md) to deploy EC2-RStudio-Server.


### Configuration
* After running the installer scripts as mentioned in the Implementation guide, do the following steps:
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
       | InstanceType | Instance type of EC2. Please refer to  the below note for recommended configuration|
       | KeyName  | Keypair name for SSH access |
       | Namespace | An environment name that will be prefixed to resource names |
       | S3Mounts | A JSON array of objects with name, bucket, and prefix properties used to mount data |
       | Subnet | The VPC subnet in which the EC2 instance will reside |
       | VPC | The VPC in which the EC2 instance will reside |
       | ACMSSLCertARN | The ARN of the AWS Certificate Manager SSL Certificate to associate with the Load Balancer |
       
    4. Launch EC2-RStudio-Server Workspace to provision an RStudio Server. 
* **NOTE**: Following are the recommended configurations for EC2 instance type. <br />

    | Configuration item | Minimum   | Recommended |
    |--------------------|-----------|-------------|
    | Instance type      | t3.medium | t3.xlarge + |
    | Hard disk          | 100GB     | 100GB +     |

## New Customer Registration for EC2-RStudio-Server 
As part of an ongoing collaboration with AWS SWB teams, we expect customers would need help with implementation, support, and ongoing enhancements of the above solution. Kindly register with Relevance Lab to get these benefits. 


[![Signup-06b](https://user-images.githubusercontent.com/63344463/122898944-f5dea200-d368-11eb-86a6-20d43c2a3903.png)](https://gd1.relevancelab.com/registration-form/)



