import io
import os
import json
import traceback
import urllib.parse
import boto3
import copy
import botocore.response as br
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
            notif_data['DeviceLocation']='Plant A'
            notif_data['DeviceType']='Monitron'
            notif_data['BUCKETId']=bucket
            notif_data['eventData']=filedata
            #fetch oauth token for SAP Event Mesh
            token = get_em_oauth_token()
            #Send event to SAP Event Mesh
            api_call_headers = {
                                'x-qos': '1',
                                'Authorization': 'Bearer ' + token,
                                'Content-Type': 'application/json'
            }
            em_rest_url = os.environ.get('SAP_EM_REST_URL')
            api_call_response = requests.post(em_rest_url, data=json.dumps(notif_data), headers=api_call_headers, verify=False)
            print("Successfuly sent event to BTP")
    except Exception as e:
        traceback.print_exc()
        return e

def get_em_oauth_token():
    auth_server_url = os.environ.get('SAP_EM_OAUTH_URL')
    client_id = os.environ.get('SAP_EM_OAUTH_CLIENT_ID')
    #Secret Manager
    secret = smclient.get_secret_value(
        SecretId=os.environ.get('SAP_EM_OAUTH_SECRET')
    )
    client_secret = secret['SecretString']
    token_req_payload = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url,
    data=token_req_payload, verify=False, allow_redirects=False,
    auth=(client_id, client_secret))
    #print(token_response)            
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
        raise ValueError('Failed to obtain token from the OAuth 2.0 server')
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']



   




