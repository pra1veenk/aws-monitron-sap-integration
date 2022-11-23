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
        self.sapauth = appConfig['sapenv']['SAP_AUTH_SECRET']
        self.saphost  = appConfig['sapenv']['SAP_HOST_NAME']
        self.sapport  = appConfig['sapenv']['SAP_PORT']
        self.sapprotocol  = appConfig['sapenv']['SAP_PROTOCOL']
        self.ddbtable    = appConfig['ddbtablename']
        self.timeout = appConfig['lambdaTimeout']
        self.bucketname = appConfig['s3']['bucketname']
        self.inferencefolder = appConfig['s3']['inferencefolder'] 
        self.vpc = appConfig['vpcId']
        self.subnet=appConfig['subnet']


