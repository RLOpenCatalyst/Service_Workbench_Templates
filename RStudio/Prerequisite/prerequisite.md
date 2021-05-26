# To Launch RStudio in SWB 
* Before deploying RStudio create Service Workbench with a custom domain associated with SSL certificate. To know how to install Service Workbench [Click Here](https://docs.aws.amazon.com/solutions/latest/service-workbench-on-aws/service-workbench-on-aws.pdf)
 * To generate a new SSL Certificate in AWS [Click Here](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)

* To update the root domain record pointing to custom domain, update the Route53 DNS records, Name Servers of newly created Hosted Zone. To know how to do this [refer](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-routing-traffic-for-subdomains.html)

