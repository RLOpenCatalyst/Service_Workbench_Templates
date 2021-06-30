import boto3
import sys
from botocore.exceptions import ClientError
import random
import time
import json
import datetime
import os
import yaml
import argparse

templateURL = 'https://github.com/RLOpenCatalyst/Service_Workbench_Templates/blob/main/RStudio/cfn-templates/RstudioToServiceCatalog.yaml'
regionShortNamesMap = {
  'us-east-2': 'oh',
  'us-east-1': 'va',
  'us-west-1': 'ca',
  'us-west-2': 'or',
  'ap-east-1': 'hk',
  'ap-south-1': 'mum',
  'ap-northeast-3': 'osa',
  'ap-northeast-2': 'sel',
  'ap-southeast-1': 'sg',
  'ap-southeast-2': 'syd',
  'ap-northeast-1': 'ty',
  'ca-central-1': 'ca',
  'cn-north-1': 'cn',
  'cn-northwest-1': 'nx',
  'eu-central-1': 'fr',
  'eu-west-1': 'irl',
  'eu-west-2': 'ldn',
  'eu-west-3': 'par',
  'eu-north-1': 'sth',
  'me-south-1': 'bhr',
  'sa-east-1': 'sao',
  'us-gov-east-1': 'gce',
  'us-gov-west-1': 'gcw',
}

configuration = {}
stackName = ''
def formRoleName():
    global configuration
    global stackName
    roleName = ''
    fileName = ''
    extension = ''
    stageFileFound = False
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".yml") or file.endswith(".yaml"):
            fileSplit = os.path.splitext(file)
            fileName = fileSplit[0]
            extension = fileSplit[1]
            stageFileFound = True
    
    print('looking for the stage file '+ fileName + extension + ' in the current working directory')
    if not stageFileFound:
        raise Exception('Stage file is not found in the current working directory. Please add the stage file into the specified directory')
    else:
        print('Found the stage file ' + fileName + extension + ' in the current working directory')
        with open(os.path.join(sys.path[0], fileName+extension), "r") as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)
            if configuration is None:
                raise Exception('Stage file is empty. Please use the stage file content that you have used during SWB installation')
            print('Checking for the key solutionName in the stage file')
            if 'solutionName' not in configuration.keys():
                raise Exception('Solution name does not exist in your stage file. Please add solution name into your stage file')
            if configuration['solutionName'] is None:
                raise Exception('Solution name value does not exist in your stage file. Please add solution name that you have used during SWB installation into your stage file')
            print('Found the solutionName and its value in the stage file')
            print('Checking for the key awsRegion in the stage file')
            if 'awsRegion' not in configuration.keys():
                raise Exception('AWS region does not exist in your stage file. Please add aws region into your stage file')
            if configuration['awsRegion'] is None:
                raise Exception('AWS Region value does not exist in your stage file. Please add region name that you have used during SWB installation into your stage file')
            print('Checking for the key awsRegion and its value in the stage file')
            checkIfRegionisValid(configuration['awsRegion'])
            regionShortName = regionShortNamesMap.get(configuration['awsRegion'])
            solutionName = configuration['solutionName']
            commonName = fileName + '-' + regionShortName +'-'+ solutionName
            roleName = commonName + '-LaunchConstraint'
            stackName = commonName + '-rlrstudio'
    return roleName, stackName, commonName

def getPortfolioIdUsingRoleName(roleName):
    portfolioFound = False
    portfolioId = ''
    if roleName.endswith('-LaunchConstraint'):
        portfolioName = roleName[:-(len('-LaunchConstraint'))]
        print('Checking for portfolio name ' + portfolioName + ' in the AWS account')
        client = boto3.client('servicecatalog')
        response = client.list_portfolios(
            AcceptLanguage='en',
            PageSize=10
        )
        response = json.dumps(response, default=myconverter)
        responseJson = json.loads(response)
        portfolioList = responseJson['PortfolioDetails']
        for portfolio in portfolioList:
            if portfolio['DisplayName'] == portfolioName:
                portfolioFound = True
                portfolioId = portfolio['Id']
                break
        if portfolioFound:
            print('Found portfolio name '+ portfolioName + ' in the AWS account')
        else:
            raise Exception('Portfolio with the name ' + portfolioName + ' is not found in the account. Please check the parameters in the stage file')
    return portfolioId



def checkIfRegionisValid(region):
    print('Checking for the validity of region '+ region + ' which is in the stage file')
    client = boto3.client('ec2')
    response = client.describe_regions(
        RegionNames=[
            region
        ]
    )
    print('Provided region '+ region + ' which is in the stage file is valid')
    return response

def checkIfPortfolioExistInAccount():
    print('Checking for the Portfolio ID '+ configuration['portfolioId'] + ' in the account ')
    client = boto3.client('servicecatalog')
    response = client.describe_portfolio(
        AcceptLanguage='en',
        Id=configuration['portfolioId']
    )
    print('Found the Portfolio ID ' + configuration['portfolioId'] + ' in the account ')
    return response

def parseTemplate():
    cloudFormationClient = boto3.client('cloudformation')
    with open("../../../cfn-templates/RstudioToServiceCatalog.yaml", "rb") as templateFileobj:
        template_data = templateFileobj.read()
    cloudFormationClient.validate_template(TemplateBody=template_data)
    return template_data

def createStack(roleName, stackName, bucketUrl):
    client = boto3.client('cloudformation')
    roleExist = IsRoleNameExist(roleName)
    portfolioId = ''
    templateBody = ''
    if roleExist:
        if('portfolioId' not in configuration.keys()):
            portfolioId = getPortfolioIdUsingRoleName(roleName)
        else:
            portfolioId = configuration['portfolioId']
            checkIfPortfolioExistInAccount()
        if portfolioId == '':
            raise Exception("Portfolio ID value is not available. Please enter Portfolio ID value into stage file or check your SWB installated account")
        templateBody = parseTemplate()
        response = client.create_stack(
            StackName=stackName,
            TemplateBody=templateBody,
            Parameters=[
                {
                    'ParameterKey': 'PortfolioID',
                    'ParameterValue': portfolioId
                },
                {
                    'ParameterKey': 'RoleName',
                    'ParameterValue': roleName
                },
                {
                    'ParameterKey': 'TemplateUrl',
                    'ParameterValue': bucketUrl
                }
            ])
    else:
        raise Exception('Launch Role ' + roleName + ' does not exist in your main SWB installation account. Please contact your administrator')
    return response

eventsList = []
def listObjectsNotInList(eventsList,latestList):
    responseList = []
    for items in latestList:
        exists = False
        for item in eventsList:
            if item['EventId'] == items['EventId']:
                exists = True
                break
        if exists != True:
            responseList.append(items)
    if len(eventsList) == 0:
        for items in latestList:
            eventsList.append(items)
    else:
        for events in responseList:
            eventsList.append(items)
    return responseList

def getStackEvents(stackName):
    client = boto3.client('cloudformation')
    global eventsList
    print('-------------------------Started creating the stack----------------------------------')
    print('Status                   ' + 'Logical ID                  ' + 'Status Reason')
    print('-------------------------------------------------------------------------------------')
    for i in range(3):
        latestList = []
        finalList = []
        time.sleep(10)
        stackEventsResponse = client.describe_stack_events(
            StackName=stackName
        )
        stackEventsResponse = json.dumps(stackEventsResponse, default=myconverter)
        responseJson = json.loads(stackEventsResponse)
        latestList = responseJson['StackEvents']
        finalList = listObjectsNotInList(eventsList,latestList)
        mainList = {}
        index = 0
        for event in finalList:
            if 'ResourceStatusReason' in event:
                miniList = [event['ResourceStatus'],event['LogicalResourceId'],event['ResourceStatusReason']]
            else:
                miniList = [event['ResourceStatus'],event['LogicalResourceId'],'-']
            mainList[index] = miniList
            index = index + 1
        for k, v in mainList.items():
            status, LogicalResourceId, statusReason = v
            print ("{:<24} {:<28} {:<30}".format(status, LogicalResourceId, statusReason))
        

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def describeStack(stackName):
    client = boto3.client('cloudformation')
    response = client.describe_stacks(StackName=stackName)
    response = json.dumps(response, default=myconverter)
    responseJson = json.loads(response)
    stackStatus = responseJson['Stacks'][0]['StackStatus']
    if(stackStatus == 'CREATE_COMPLETE'):
        print('-------------------------Stack created successfully----------------------------------')
        return
    if(stackStatus == 'CREATE_FAILED' or 'IMPORT_FAILED' or 'IMPORT_ROLLBACK_IN_PROGRESS' or 'IMPORT_ROLLBACK_FAILED' or 'IMPORT_ROLLBACK_COMPLETE' or 'ROLLBACK_IN_PROGRESS'):
        print('Stack ' + stackName + ' is with status ' + stackStatus + ', so deleting the stack')
        print('Please check the input parameters and try again')
        print('-------------------------Deleting the stack----------------------------------')
        deleteStack(stackName)

def deleteStack(stackName):
    client = boto3.client('cloudformation')
    client.delete_stack(StackName = stackName)

def IsRoleNameExist(roleName):
    print('Checking for Launch role '+ roleName + ' name in the account')
    roleNameExists = False
    iamClient = boto3.client('iam')
    roleDetails = iamClient.get_role(RoleName=roleName)
    response = json.dumps(roleDetails, default=myconverter)
    responseJson = json.loads(response)
    if(responseJson is not None and responseJson['Role']['RoleName'] == roleName):
        roleNameExists = True
    print('Found the Launch role '+ roleName + ' name in the account')
    return roleNameExists

def getArtifactsBucketName(commonName):
    accountId = boto3.client("sts").get_caller_identity()["Account"]
    artifactsBucketName = accountId +'-' + commonName +'-artifacts'
    s3Client = boto3.client('s3')
    response = s3Client.head_bucket(
        Bucket=artifactsBucketName
    )
    return artifactsBucketName

def uploadRstudioTemplateToArtifactsBucketAndgetTheURL(bucketName):
    print('Uploading the EC2-Rstudio server template to SWB artifacts bucket')
    print('Bucket name ', bucketName)
    s3Client = boto3.client('s3')
    objectName = 'ec2-rstudio-server.cfn.yml'
    bucketUrl = ''
    path = os.getcwd()
    mainPath = path.replace('/machine-images/config/infra','')
    templatePath = os.path.join(mainPath, 'cfn-templates/ec2-rlstudio.yaml')
    print('Template Path ', templatePath)
    with open(templatePath, "rb") as f:
        response = s3Client.upload_file(templatePath, bucketName, 'service-catalog-products/{}'.format(objectName))
        print('Response of upload file object ',response)
        preSignedUrlResponse = s3Client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucketName,
                                                            'Key': 'service-catalog-products/{}'.format(objectName)},
                                                    ExpiresIn=3600)
        response = json.dumps(preSignedUrlResponse, default=myconverter)
        bucketUrl = response[1 : response.index('?')]
        print('Bucket URL', bucketUrl)
    return bucketUrl

if __name__ == "__main__":
    try:
        parser=argparse.ArgumentParser(
            description=''' Run this command to create the Service Catalog product for the RStudio Server with ALB support.
                The command expects a single yaml file in the same folder as the script as input. 
                Copy the $stage.yml file from your SWB installation and add a line with key as portfolio-id and the value as the portfolio-id created during the deployment of SWB. The script will error out if it does not find this file.
                The script also looks for the role that was created during SWB installation. It needs the solutionName in the yaml file to build the role-name.
                The script also needs the AWS region into which the SWB installation was made. It looks for the awsRegion key in the yaml file.''')
        args=parser.parse_args()
        roleName,stackName,commonName = formRoleName()
        bucketName = getArtifactsBucketName(commonName)
        bucketUrl = uploadRstudioTemplateToArtifactsBucketAndgetTheURL(bucketName)
        stackResponse = createStack(roleName,stackName,bucketUrl)
        getStackEvents(stackName)
        describeStack(stackName)
    except Exception as e:
        if('ResourceNotFoundException' in e.message and 'DescribePortfolio' in e.message):
            print('Portfolio ID in the stage file does not exist in the AWS account')
        elif('NoSuchEntity' in e.message and 'GetRole' in e.message):
            print('Launch Role does not exist in your main SWB installation account. Please contact your administrator or check your stage file')
        elif('InvalidParameterValue' in e.message and 'DescribeRegions' in e.message):
            print('AWS region name provided in the stage file is invalid. Please add region name that you have used during SWB installation into your stage file')
        elif('AlreadyExistsException' in e.message and 'CreateStack' in e.message):
            print('A stack with the same configurations already exist. So the RStudio-server template will be available as part of your current SWB deployment. Please check by logging in as an administrator into SWB')
        elif('Not Found' in e.message):
            print('Please use the AWS credentials of SWB deployment in the aws Configure or check the stage file')
        else:
            print('Exception ',e)
        if stackName != '':
            deleteStack(stackName)