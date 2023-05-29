# EC2-RStudio-Server* for Service Workbench on AWS
*RStudio with Application Load Balancer (ALB)

*Changes to the core Service Workbench product are in progress and must complete prior to Customers using the new RStudio experience

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
    |      1.4.1717          |   4.3.0    |
    
            
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
       | AccessFromCIDRBlock  | The CIDR block used to access the ec2 instances. Example: 0.0.0.0/0 |
       | AmiId  | Amazon Machine Image for the EC2 instance which is pre-installed with R packages and Rstudio server |
       | EncryptionKeyArn | The ARN of the KMS encryption Key used to encrypt data in the instance.|
       | EnvironmentInstanceFiles | An S3 URI (starting with "s3://") that specifies the location of files to be copied to the environment instance, including any bootstrap scripts |
       | IamPolicyDocument | The IAM policy to be associated with the launched Workspace Type |
       | InstanceType | Instance type of EC2. Please refer to  the below note for recommended configuration. |
       | KeyName  | Name of keypair that is used for performing SSH to the instance |
       | Namespace | An environment name that will be prefixed to resource names. This is used to differentiate the resources |
       | S3Mounts | This is used to mount data on EC2 instance|
       | Subnet | The VPC subnet in which the EC2 instance will reside |
       | VPC | The VPC in which the EC2 instance will reside |
       | ACMSSLCertARN | The ARN of the AWS Certificate Manager SSL Certificate to associate with the Load Balancer. Follow the steps to get the ARN from [this](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/prerequisites/prerequisite.md#steps-to-generate-new-ssl-certificate-in-aws) |

       **NOTE**: For all the above parameters, you can use default values except for ACMSSLCertARN, InstanceType and AmiId
       
    4. Launch EC2-RStudio-Server Workspace to provision an RStudio Server. 
* **NOTE**: Following are the recommended configurations for EC2 instance type. <br />

    | Configuration item | Minimum   | Recommended |
    |--------------------|-----------|-------------|
    | Instance type      | t3.medium | t3.xlarge + |
    | Hard disk          | 100GB     | 100GB +     |

## How to connect
Since RStudio currently requires a custom domain name, please configure the same by following the steps in the [link](https://github.com/awslabs/service-workbench-on-aws/blob/mainline/main/solution/machine-images/README.md)
* The EC2 instance backing this workspace must be in the Ready state.
* Click on the connections button and hit Connect.
* If you're provisioning an RStudio instance with studies selected, the selected studies will show up as mounted directories in the RStudio. These study directories will contain files uploaded to the corresponding study. Any files uploaded to the study from the Service Workbench will automatically appear in the mounted study directories after a short delay.
* Note: Connection-critical SSM parameters are created once RStudio instances are fully initialized. Allow up to a minute after an RStudio instance becomes available on Service Workbench for connections to work.

**Notes**:
* If you're provisioning an RStudio instance with studies selected, these studies will only get mounted on your instance once you click on the RStudio workspace's "Terminal" tab.
* If you started a previously stopped RStudio instance (manually or automatically) and connect to it, you might see an error dialog box saying the session closed abruptly. Although this typically does not affect your data, it is recommended to quit your session from within your RStudio workspace before stopping the instance through SWB.
* The auto-stop feature is enabled by default and configured to 1 hour. For configuring a different auto-stop timeout, please assign the MAX_IDLE_MINUTES value accordingly in [link](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/tree/main/RStudio/machine-images/config/infra/files/rstudio/check-idle) and redeploy the machine-images SDC.
* To disable auto-stop, assign the value 0 to MAX_IDLE_MINUTES and redeploy machine-images SDC.

### Start and Stop workspace
RStudio workspaces can be stopped when not in use. Click the stop button to stop the workspace, and click the start button to start the workspace again.

### EDIT CIDR
We can edit CIDR blocks by adding or deleting. This block will determine who can access the RStudio. <br />
**NOTE**: We can add upto 4 CIDR blocks for port 443.

### Common connection issues
* Connection to workspace is restricted to specific CIDR block.
* Check if your public IP is covered by the restricted CIDR block of the workspace.
* Check if workspace type configuration has hard-coded value in field 'AccessFromCIDRBlock'. (Admin only)
* If you're using VPN, your public IP address might change. Try disconnect VPN, and then connect to workspace.



## New Customer Registration for EC2-RStudio-Server 
As part of an ongoing collaboration with AWS SWB teams, we expect customers would need help with implementation, support, and ongoing enhancements of the above solution. Kindly register with Relevance Lab to get these benefits. 


[![Signup-06b](https://user-images.githubusercontent.com/63344463/122898944-f5dea200-d368-11eb-86a6-20d43c2a3903.png)](https://gd1.relevancelab.com/registration-form/)



