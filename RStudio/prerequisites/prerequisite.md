# To Launch RStudio in SWB

## Custom domain creation
* Before deploying RStudio create Service Workbench with a custom domain associated with SSL certificate [Click Here](https://github.com/awslabs/service-workbench-on-aws/tree/mainline/main/solution/machine-images) . To know how to install Service Workbench [Click Here](https://docs.aws.amazon.com/solutions/latest/service-workbench-on-aws/service-workbench-on-aws.pdf)

## Steps to generate new SSL certificate in AWS
 * To generate a new SSL Certificate in AWS [Click Here](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)
    * You can navigate to Certificate Manager service of the target AWS account
    * Click on "Request a certificate"
    * Provide a sub domain name
    * Choose DNS validation in the next step
    * Copy the CNAME record's name and value

* To update the root domain record pointing to sub domain, update the Route53 with the CNAME record of newly created Hosted Zone during the SWB installation. 

* After sometime the root domain's Route53 gets updated with the CNAME record and validation status of SSL certificate gets changed to Success. Now you can copy the ARN of the certificate and use this during the configuration of the Rstudio.

## Onboard role update
* Before provisioning RStudio-server powered by RL, please update the stack created for the role during the SWB account onboarding. You can update the stack using the following template [Template link](https://github.com/awslabs/service-workbench-on-aws/tree/mainline/addons/addon-base-raas/packages/base-raas-cfn-templates/src/templates/onboard-account.cfn.yml)


