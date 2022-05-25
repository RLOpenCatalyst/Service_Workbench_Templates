### Procedure to install EC2-RStudio-Server into Service Workbench

To run the following steps you need any Linux machine, preferably the same machine from where you installed Service Workbench. The following software is used by the installer and you will need to install the same before carrying out the installation process

 * **Install packer** : This solution uses Packer to create an Amazon Machine Image (AMI). This AMI forms the basis for RStudio environment that investigators use for their research.
To install Packer 1.6.0, use [pkenv](https://github.com/iamhsa/pkenv) 
[Packer Installation Link](https://learn.hashicorp.com/tutorials/packer/get-started-install-cli)
 * **Install AWS CLI 2**: [AWS  CLI Installation Link](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
 *  **Install Git**: [Git Installation Link](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
 *  **Install pip**: [pip Installation Link](https://pip.pypa.io/en/stable/installing/)
 * Clone the repository Service_Workbench_Templates by using the following git command. <br />
    ```
    git clone https://github.com/RLOpenCatalyst/Service_Workbench_Templates.git
    ```	

**Steps to install EC2-RStudio-Server AMI**

 * Change the configuration file for AMI creation.
Navigate to the the folder RStudio/machine-images/config/infra. <br />
Fill the following parameters in the file configuration.json by using the parameters specific to Service Workbench deployment region.

|       Configuration        |   Description   |
|--------|--------------------------------|
| AWS Access key | AWS programmatic access key that will used to create the AMI. Not needed when AWS Profile is used |
| AWS Secret key | AWS programmatic secret key that will used to create the AMI. Not needed when AWS Profile is used |
| Region | Region in which the AMI needs to be created |
| VPC ID | VPC in which the AMI needs to be created. Leave it blank to use default VPC |
| Subnet | Subnet in which the AMI needs to be created. Leave it blank to use default VPC |
| AMI Name | Name of the AMI that needs to be created |
| AWS Profile | AWS CLI profile that needs to be used to create the AMI. Not needed when AWS Access and Secret key are used |
| Stage Name |Stage file name used in the SWB deployment |
|

> **_NOTE:_**  To use a centralized devops account for storing AMIs. Use the Devops profile used in the SWB deployment as the **AWS Profile** configuration.

 * **secret.txt**: A single-line text file that contains the JWT secret from the Service Workbench deployment, which can be found in Parameter Store at /$stage/$solution/jwt/secret, where $stage is the stage name for the environment and $solution is the solution name. <br />
> **_NOTE:_** Add this secret.txt file to the following folder. RStudio/machine-images/config/infra/files/rstudio
 * Run the packer script in the folder RStudio/machine-images/config/infra using the following command

    ```
    packer build -var-file=configuration.json packer-ec2-rstudio-workspace.json
    ```

**Steps to install EC2-RStudio-Server**

 * Follow the steps for deploying Rstudio product into Service Workbench’s portfolio
    * Copy only the $stage file from the folder main/config/settings/ of
    Service Workbench deployment into folder of cloned repository of
    Service_Workbench_Templates/RStudio/machine-images/config/infra.
    * Please make sure you have the following keys and their values in the
    $stage file.
        -   solutionName
        -   awsRegion
    > **_NOTE:_** Add one more key called **portfolioId** to the same file. You can login to your Main account and access the Service Catalog in the region where your Service Workbench instance is deployed. Navigate to Portfolios in the left hand menu. Find the Service Workbench created portfolio and note down the portfolio id.
    * After adding the Portfolio ID to the $stage file you can run the
    following commands 
        ```	
        pip install -r requirements.txt
        ```	 
        ```
        python create-rstudio.py
        ```
    * If the script outputs saying ‘Stack created successfully’, the EC2-RStudio-Server product should be visible in the Workspace Types screen when you login to Service Workbench as an Administrator. Otherwise you can refer to the errors that are thrown by the script and correct them accordingly.