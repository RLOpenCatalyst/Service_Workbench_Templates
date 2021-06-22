


# Service_Workbench_Templates

# Relevance Lab and AWS Partnership for Service WorkBench on AWS (To know more, Click [here](https://gd1.relevancelab.com/aws-service-workbench/))
Both AWS SWB and Relevance Lab RLCatalyst Research Gateway teams are committed to making scientific research frictionless for researchers. With a shared goal, this new initiative speeds up collaboration and will help provide new innovative open-source solutions leveraging AWS Service Workbench and partner-provided solutions like this RStudio with ALB from Relevance Lab. The collaboration efforts will soon be adding more solutions covering Genomic Pipeline Orchestration with Nextflow, use of HPC Parallel cluster, and secure research workspaces with AppStream 2.0, so stay tuned.

Cloud computing offers the research community access to vast amounts of computational power, storage, specialized data tools, and public data sets, collectively referred to as Research IT, with the added benefit of paying only for what is used. However, researchers may not be experts in using the AWS Console to provision these services in the right way. This is where software solutions like AWS Service Workbench (SWB) make it possible to deliver scientific research computing resources in a secure and easily accessible manner.

RStudio is a popular software used by the Scientific Research Community and supported by AWS Service Workbench (SWB). Researchers use RStudio very commonly in their day-to-day efforts. While RStudio is a popular product, the process of installing RStudio securely on AWS Cloud and using it in a cost-effective manner is a non-trivial task, especially for Researchers. With AWS SWB, the goal is to make this process very simple, secure, and cost-effective for Researchers so that they can focus on “Science” and not “Servers” thereby, increasing their productivity.

To get started with RStudio on SWB provided by Relevance Lab Click [here](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/tree/main/RStudio)

Relevance Lab (RL), in partnership with AWS, set out to make the experience of using RStudio with AWS Service Workbench simple and secure.

# Getting started with EC2-RStudio-Server for Service Workbench on AWS


|    Steps      |   Activities   |   Links                          |
|--------|------------|--------------------------------|
| Step-1  | **Install the SWB Enterprise instance with Custom Domain.** It is very important that the SWB instance is deployed with a custom domain option. This allows you to request an Amazon-issued certificate using ACM for your domain, and this certificate can then be used to provide secure access to your SWB instance and the resources provisioned using SWB. | [Documentation](https://docs.aws.amazon.com/solutions/latest/service-workbench-on-aws/overview.html)            [Deployment guide](https://docs.aws.amazon.com/solutions/latest/service-workbench-on-aws/automated-deployment.html) |
| Step-2 |    **Add ACM certificate to the hosting account.** 
|| It is best to set up your SWB domain (e.g. swb.yourdomain.com) as its own hosted zone. See “Set up routing for your sub-domain”. Then request a new SSL certificate in AWS ACM  | a. [Setup routing for your sub-domain](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-routing-traffic-for-subdomains.html) b. [Request a new SSL certificate in AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)|
|Step-3| **Install new EC2-Rstudio-Server Templates**
||Clone the repo from Relevance Lab and run the script to create the AMI in your AWS account and the Service Catalog product in your SWB portfolio. |[EC2-Rstudio-Server Templates hosted by Relevance Lab](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/README.md)|
|Step-4|Log into SWB as Admin and detect the newly uploaded template (EC2-Rstudio-Server) and import as Workspace Type.   |[Post-launch tasks](https://docs.aws.amazon.com/solutions/latest/service-workbench-on-aws/automated-deployment.html#step-2.-post-launch-tasks)|  
|Step-5|Configure and ready for researchers to use a brand new upgraded RStudio with secure ALB architecture.| [SWB Configuration](https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/README.md#configuration)||



# Registration for a new Customer and Support Process details

As shown below, Customers who wish to use Relevance Lab Custom Solution and wish to get support for issues, upgrades will need to signup as shown below. You can do so by clicking on the sign up button below.

![Signup Process](https://user-images.githubusercontent.com/63344463/122382998-10d79d80-cf88-11eb-9cea-562a958e0346.jpg)

Once signed up, Customers can raise an issue as shown below.

![Support Process](https://user-images.githubusercontent.com/63344463/122383529-893e5e80-cf88-11eb-965b-da984dcba1a4.jpg)


[![SignUp](https://user-images.githubusercontent.com/63344463/122757544-5f04dd80-d2b5-11eb-9a76-87391229b1cd.png)](https://gd1.relevancelab.com/registration-form/)
