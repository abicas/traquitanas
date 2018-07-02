import sys
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta  

## PENDING - Restrict to account not default 
## PENDING - Exclude list 
## PENDING - Only a set of services 



def wipe_codestar():
## CODESTAR
    print ("- Wiping CodeStar Projects... ")
    client = boto3.client('codestar')
    cstar = client.list_projects()
    for cf in cstar['projects']:
        print ("    - Project FOUND:"),
        print cf['projectId']
        print ("    - Deleting Project...")
        client.delete_project(id=cf['projectId'])
        print ("    - Deleting Project... DONE")
    print ("- Wiping CodeStar Projects... DONE ")

def wipe_ec2():
## EC2 Block - Need to include EXCEPTIONS
    print ("- Wiping EC2 Instances... ")
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        print ("    - EC2 FOUND:"),
        print instance.instance_id+' -> '+instance.state['Name']
        if ( instance.state['Name'] == 'running'):
            print ("    - ISSUING TERMINATE TO: "),
            instance.terminate()
            print instance.instance_id+' -> '+instance.state['Name']
    print ("- Wiping EC2 Instances... DONE")

def wipe_s3():
## S3 Block - Need to include EXCEPTIONS
    print ("- Wiping S3 Buckets... ")
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print ("    - S3 BUCKET FOUND:"),
        print bucket.name
        if ( "do-not-delete" not in bucket.name):
            print ("        - Deleting ALL OBJECTS from: "+bucket.name)
            bucket.objects.all().delete()
            print ("        - ISSUING DELETE TO: "+bucket.name)
            bucket.delete()
    print ("- Wiping S3 BUckets... DONE")

def wipe_lambda():
## LAMBDA BLOCK - Exceptions yeah, yeah yeah
    print ("- Wiping LAMBDA Functions... ")
    print ("    - Listing all functions"),
    lamb = boto3.client('lambda')
    lambdas = lamb.list_functions()
    print ("DONE")
    for unique in lambdas['Functions']: 
        print ("    - LAMBDA Function FOUND:"),
        print (unique['FunctionName'])
        print ("    - Issuing DELETE :"),
        lamb.delete_function(FunctionName=unique['FunctionName'],)
        print ("DONE")
    print ("- Wiping LAMBDA Functions... DONE")

def wipe_dynamodb():
## DYNAMODB - Exceptions yeah, yeah yeah
    print ("- Wiping DynamoDB Functions... ")
    dynamodb = boto3.resource('dynamodb')
    for table in dynamodb.tables.all():
        print ("    - TABLE FOUND:"),
        print table.name
        print ("    - Issuing DELETE :"),
        table.delete()
        print ("DONE")
    print ("- Wiping DynamoDB... DONE")

def wipe_codebuild():
## CODESTAR
    print ("- Wiping CodeBuild Projects... ")
    client = boto3.client('codebuild')
    cstar = client.list_projects()
    for cf in cstar['projects']:
        print ("    - Project FOUND:"),
        print cf
        print ("    - Deleting Project...")
        client.delete_project(name=cf)
        print ("    - Deleting Project... DONE")
    print ("- Wiping CodeBuild Projects... DONE ")

def wipe_codecommit():
## CODESTAR
    print ("- Wiping CodeCommit Repos... ")
    client = boto3.client('codecommit')
    cstar = client.list_repositories()
    for cf in cstar['repositories']:
        print ("    - Repo FOUND:"),
        print cf['repositoryName']
        print ("    - Deleting Repo...")
        client.delete_repository(repositoryName=cf['repositoryName'])
        print ("    - Deleting Repo... DONE")
    print ("- Wiping CodeCommit Repos... DONE ")

def wipe_codepipeline():
## CODESTAR
    print ("- Wiping CodePipeline pipelines... ")
    client = boto3.client('codepipeline')
    cstar = client.list_pipelines()
    for cf in cstar['pipelines']:
        print ("    - Pipeline FOUND:"),
        print cf['name']
        print ("    - Deleting Pipe...")
        client.delete_pipeline(name=cf['name'])
        print ("    - Deleting Pipe... DONE")
    print ("- Wiping  CodePipeline pipelines... DONE ")
    
def wipe_apigateway():
## CODESTAR
    print ("- Wiping API Gateways... ")
    client = boto3.client('apigateway')
    cstar = client.get_rest_apis()
    for cf in cstar['items']:
        print ("    - API GW FOUND:"),
        print (cf['name']+' ('+cf['id']+')')
        print ("    - Deleting API GW...")
        client.delete_rest_api(restApiId=cf['id'])
        print ("    - Deleting API GW... DONE")
    print ("- Wiping API Gateways... DONE ")

print ("### STARTING CLEANUP ###")
wipe_codestar()
wipe_codecommit()
wipe_codepipeline()
wipe_codebuild()
wipe_apigateway()
wipe_ec2()
wipe_lambda()
wipe_dynamodb()
wipe_s3()