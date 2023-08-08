import json
import os 

class Config:
    def __init__(self):
        root_dir = os.path.dirname(os.path.dirname( __file__ ))
        configfile = open(root_dir + '/appConfig.json')
        appConfig = json.load(configfile)
        
        self.account = appConfig['env']['account']
        self.region  = appConfig['env']['region']
        self.stackname = appConfig['stackName']
        self.sapemoauthsecret = appConfig['sapenv']['SAP_EM_OAUTH_SECRET']
        self.sapemoauthurl = appConfig['sapenv']['SAP_EM_OAUTH_URL']
        self.sapemoauthclientid = appConfig['sapenv']['SAP_EM_OAUTH_CLIENT_ID']
        self.sapemresturl = appConfig['sapenv']['SAP_EM_REST_URL']
        self.timeout = appConfig['lambdaTimeout']
        self.bucketname = appConfig['s3']['bucketname']
        self.vpc = appConfig['vpcId']
        self.subnet=appConfig['subnet']


