import requests
import sys
import json
import time
import uuid
import random
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper

api = TheHiveApi('localhost:9000', 'SECRET')

#----First exercice----#

artifacts = [
    AlertArtifact(dataType='url', data='mikrosoft365.com/loginpage'),
    AlertArtifact(dataType='domain', data='mikrosoft365.com'),
    AlertArtifact(dataType='url', data='taxes.gav.au/link/page22/'),
    AlertArtifact(dataType='domain', data='taxes.govs.au'),
    AlertArtifact(dataType='url', data='cisca-webex.com/login/yourmail.training.org/'),
    AlertArtifact(dataType='domain', data='cisca-webex.com'),
    AlertArtifact(dataType='url', data='netflix.obvious-phishing.com/login'),
    AlertArtifact(dataType='domain', data='obvious-phishing.com'),  
    AlertArtifact(dataType='url', data='aple.com/loginpage'),
    AlertArtifact(dataType='domain', data='aple.com'),
    AlertArtifact(dataType='url', data='https://poczta.pl-getbuys.icu/'),
    AlertArtifact(dataType='domain', data='pl-getbuys.icu'),
    AlertArtifact(dataType='ip', data='1.2.3.4'),
    AlertArtifact(dataType='ip', data='134.43.25.11'),
    AlertArtifact(dataType='ip', data='94.154.129.50'),
    AlertArtifact(dataType='ip', data='72.167.191.83')
]

#customFields = CustomFieldHelper()\
#    .add_string('businessUnit', 'Finance')\
#    .add_string('location', 'Sydney')\
#    .build()

sourceRef = str(uuid.uuid4())[0:6]

alert = Alert(title='Phishing list update 7.5.2021',
    tlp=3,
    tags=['source:MISP', 'origin:CIRCL_LU'],
    description='A curated list of phishing IOCs',
    type='external',
    source='MISP',
    sourceRef='event_1576',
    artifacts=artifacts,
#    customFields=customFields
)

try:
   response = api.create_alert(alert)

   # Print the JSON response 
   print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
   print("Alert create error: {}".format(e))


#----Second Exercice----#

artifacts = [
    AlertArtifact(dataType='ip', data='94.23.172.164'),
    AlertArtifact(dataType='url', data='proxycheker.pro'),
    AlertArtifact(dataType='hash', data='BBDE33F5709CB1452AB941C08ACC775E')
]

alert = Alert(title='FireEye reports on APT34 - Oilrg',
    tlp=3,
    tags=['source:MISP', 'origin:FireEye'],
    description='Disclaimer: IOC are real ones, never browse them.',
    type='external',
    source='MISP',
    sourceRef='event_1654',
    artifacts=artifacts,
#    customFields=customFields
)

try:
   response = api.create_alert(alert)

   # Print the JSON response
   print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
   print("Alert create error: {}".format(e))

