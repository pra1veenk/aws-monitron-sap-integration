import io
import os
import json
import traceback
import urllib.parse
import boto3
import copy
import botocore.response as br
import pyodata
import requests
from PIL import Image
import base64


#clients
s3       = boto3.resource('s3')
smclient = boto3.client('secretsmanager')
sapauth={}

#constants
#Replace the below variables with the API endpoint if using SAP BTP
#for eg if the API URL is https://359600betrial-trial.integrationsuitetrial-apim.us10.hana.ondemand.com:443/359600betrial/API_DEFECT_SRV
#DEFECT_SERVICE = /359600betrial/API_DEFECT_SRV
#ATTACHMENT_SERVICE = /359600betrial/API_CV_ATTACHMENT_SRV

DEFECT_SERVICE='/sap/opu/odata/sap/API_DEFECT_SRV'
DEFECT_SERVICE_PATH='/sap/opu/odata/sap/ZAPI_QUAL_NOTIFICATION_SRV'
ATTACHMENT_SERVICE='/sap/opu/odata/sap/API_CV_ATTACHMENT_SRV'
NOTIF_SERVICE = '/359600betrial/ZSERVICE_PM_NOTIFICATION_SRV/'

def handler(event,context):
    try:
# Incoming json file
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],\
             encoding='utf-8')
        # Read the json file   
        print(bucket)
        print(key)
        
        S3client = boto3.client("s3")
        
        fileobj = S3client.get_object(
        Bucket=bucket,
        Key=key
        ) 
        
        
        filetext = fileobj['Body'].read().decode('utf-8')
        #print(filetext)
        filesplit = filetext.splitlines()
        #get the latest record
        filedata=json.loads(filesplit[-1])
        #print(filedata)
        if filedata['assetState']['newState'] == 'NEEDS_MAINTENANCE' and filedata['assetState']['newState'] != filedata['assetState']['previousState']:

            #Snotif = getODataClient(NOTIF_SERVICE)
            notif_data = {}
            notif_data['SourceSystem']='AWS'
            notif_data['DeviceLocation']='PlantA'
            notif_data['DeviceType']='Monitron'
            notif_data['BUCKETId']=bucket
            notif_data['eventData']=filedata
            #fetch oauth token for SAP Event Mesh
            token = get_em_oauth_token()
            #Send event to SAP Event Mesh
            api_call_headers = {'Authorization': 'Bearer ' + token}
            em_rest_url = os.environ.get('SAP_EM_REST_URL')
            api_call_response = requests.post(em_rest_url, headers=api_call_headers, verify=False)
            print("Successfuly sent event to BTP")
            #If you choose to pass the file data in the long text
            #Longtext = json.dumps(filedata)
            #Longtext = Longtext.replace("\\r\\n  ", " ")
            #print("popualre")
            
            #ddbConfigTable = ddb.Table(os.environ.get('DDB_CONFIG_TABLE'))
        
            #response = ddbConfigTable.query(KeyConditionExpression=Key('monpath').eq(bucket))
            #print(response['Items'])
           
            #configItem = response['Items']
            #print(type(configItem))
            
            #notif_data["FunctLoc"] = configItem[0]['location']
            #notif_data["Equipment"] = configItem[0]['sapequi']
            #notif_data['ShortText'] = 'Monitron error'
            #notif_data['LongText'] = " Needs Maintenance, check S3  " +bucket
            
            #print(notif_data)
            
            #create_request = Snotif.entity_sets.NOTIF_CREATESet.create_entity()
            #create_request.set(**notif_data)
            #try:
             #   new_notif_set = create_request.execute()
            #except pyodata.exceptions.HttpError as ex:
             #    print(ex.response.text)
            #print('Notification Number'+new_notif_set.NotifNo)
    except Exception as e:
        traceback.print_exc()
        return e

def get_em_oauth_token():
    auth_server_url = os.environ.get('SAP_EM_OAUTH_URL')
    client_id = os.environ.get('SAP_EM_OAUTH_CLIENT_ID')
    #Secret Manager
    client_secret = smclient.get_secret_value(
        SecretId=os.environ.get('SAP_EM_OAUTH_SECRET')
    )
    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url,
    data=token_req_payload, verify=False, allow_redirects=False,
    auth=(client_id, client_secret))
                
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
        raise ValueError('Failed to obtain token from the OAuth 2.0 server')
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']
    
def getODataClient(service,**kwargs):
    try:
        sap_host = os.environ.get('SAP_HOST_NAME')
        sap_port = os.environ.get('SAP_PORT')
        sap_proto = os.environ.get('SAP_PROTOCOL')
        serviceuri = sap_proto + '://' + sap_host + ':' + sap_port + service
       
        print('service call:'+serviceuri)
       #Secret Manager
        authresponse = smclient.get_secret_value(
            SecretId=os.environ.get('SAP_AUTH_SECRET')
        )

        sapauth = json.loads(authresponse['SecretString'])
        
       #Set session headers - Auth,token etc
        session = requests.Session()
        # If using SAP Netweaver Gateway, please uncomment
        #session.auth = (sapauth['user'],sapauth['password'])
        #If using BTP, please uncomment
        session.headers.update({'APIKey': sapauth['APIKey']})
        response = session.head(serviceuri, headers={'x-csrf-token': 'fetch'})
        token = response.headers.get('x-csrf-token', '')
        session.headers.update({'x-csrf-token': token})
        oDataClient = pyodata.Client(serviceuri, session)
        
        return oDataClient

    except Exception as e:
          traceback.print_exc()
          return e        



   




