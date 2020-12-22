from slack import WebClient
from slack.errors import SlackApiError
import json
import base64
import logging
from time import time
import os

slackToken = os.environ['slackToken'] # token format => xoxb-xxxxxxxx-xxxxxxxx-xxxxxxxx
slackChannel = os.environ['slackChannel']

def cloudFunctionTrigger(event, context):
    #Cloud Function triggered by Pub/Sub.

    if 'data' in event:
        data = json.loads(base64.b64decode(event['data']))
        print(data)
        status = data['status']
        logUrl= data['logUrl']

        if(status=="FAILURE"):
            sendFailure(logUrl=logUrl)
            exit()
        elif(status=="TIMEOUT"):
            sendTimeout(logUrl=logUrl)
            exit()
        source = data.get("source")
        if source != None:
            if 'gitSource' in data['source']:
                if(status == "WORKING"):
                    sendDeploying(logUrl=logUrl,text="Deploying from `{0}/{1}`".format(data['substitutions']['REPO_NAME'],data['substitutions']['BRANCH_NAME']))
                elif(status == "SUCCESS"):
                    sendSuccess(logUrl=logUrl,text="Successfully Deployed from `{0}/{1}`".format(data['substitutions']['REPO_NAME'],data['substitutions']['BRANCH_NAME']))
                
    else:
        print("No data found!!")
        exit()

def sendDeploying(logUrl,text):

    client = WebClient(token=slackToken)
    try:
        response = client.chat_postMessage(
            channel=slackChannel,
            attachments=[{
                'title': "Build Log",
                'title_link':logUrl,
                'color': "#4d86d1",
                'fields': [{
                  'title': "Status:",
                  'value': text
              }],
            'footer': 'Google Cloud Build',
            'footer_icon':'https://cloud.google.com/container-registry/images/builder.png',
            'ts': time()
            }
            ]
        )
    except SlackApiError as e:
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

def sendFailure(logUrl):

    client = WebClient(token=slackToken)
    try:
        response = client.chat_postMessage(
            channel=slackChannel,
            attachments=[{
                'title': "Build Log",
                'title_link':logUrl,
                'color': '#a63636',
                'fields': [{
                  'title': "Status:",
                  'value': "Failed!!, check the build logs."
              }],
            'footer': 'Google Cloud Build',
            'footer_icon':'https://cloud.google.com/container-registry/images/builder.png',
            'ts': time()
            }
            ]
        )
    except SlackApiError as e:
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
def sendTimeout(logUrl):

    client = WebClient(token=slackToken)
    try:
        response = client.chat_postMessage(
            channel=slackChannel,
            attachments=[{
                'title': "Build Log",
                'title_link':logUrl,
                'color': "#f0c126",
                'fields': [{
                  'title': "Status:",
                  'value': "TimeOut!"
              }],
            'footer': 'Google Cloud Build',
            'footer_icon':'https://cloud.google.com/container-registry/images/builder.png',
            'ts': time()
            }
            ]
        )
    except SlackApiError as e:
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

def sendSuccess(logUrl,text):

    client = WebClient(token=slackToken)
    try:
        response = client.chat_postMessage(
            channel=slackChannel,
            attachments=[{
                'title': "Build Log",
                'title_link':logUrl,
                'color': "#55b551",
                'fields': [{
                  'title': "Status:",
                  'value': text
              }],
            'footer': 'Google Cloud Build',
            'footer_icon':'https://cloud.google.com/container-registry/images/builder.png',
            'ts': time()
            }
            ]
        )
    except SlackApiError as e:
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
