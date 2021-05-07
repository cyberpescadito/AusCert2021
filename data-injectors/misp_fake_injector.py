import requests
import sys
import json
import time
import uuid
import random
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper

api = TheHiveApi('URL', 'SECRET')
numberFakeAlerts = 6

def createArtifacts(urlList,ipList):
    artifacts = []
    for item in urlList:
        artifacts.append(AlertArtifact(dataType='url', data=item,message='fake'))
    for item in ipList:
        artifacts.append(AlertArtifact(dataType='ip', data=item,message='fake'))
    return artifacts

def randomUrls(how):
    i=0
    urlList = []
    tldList = ['.fr','.com','.org','.ru','.eu', '.online','.io', '.au']
    wordList = ['look','forward','sharing','further','progress','future','reports','continue','innovate','enhance','diversity','equity']
    while i != how:
        path=str(uuid.uuid4())[0:8]
        tld=random.choice(tldList)
        hostname=random.choice(wordList)
        hostname2=random.choice(wordList)
        urlList.append(str(hostname + '-' + hostname2 + tld + '/' + path))
        i+=1
    return urlList

def randomIp(how):
    i=0
    ipList=[]
    while i != how:
        octets = random.sample(range(1, 255), 4)
        ipList.append(str(octets[0]) + '.' + str(octets[1]) + '.' + str(octets[2]) + '.' + str(octets[3]))
        i+=1
    return ipList

def generateRandomAlert():
    ipList = randomIp(3)
    urlList = randomUrls(3)
    artifacts = createArtifacts(urlList,ipList)

    alert = Alert(title='Phishing list update 8.5.2021',
        tlp=random.randint(1, 3),
        tags=['source:MISP', 'origin:CIRCL_LU'],
        description='A curated list of fake phishing IOCs',
        type='external',
        source='MISP',
        sourceRef='event_' + str(random.randint(0, 99999)),
        artifacts=artifacts
        #    customFields=customFields
    )
    try:
        response = api.create_alert(alert)

        # Print the JSON response
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    except AlertException as e:
        print("Alert create error: {}".format(e))

    return response

i=0
while i != numberFakeAlerts:
    generateRandomAlert()
    i+=1

