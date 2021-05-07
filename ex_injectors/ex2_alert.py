import time
import requests
import sys
import json
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper, Case, CaseTaskLog

api = TheHiveApi('localhost:9000', 'secret')

#alert on malicious IP telnet

artifacts = [
    AlertArtifact(dataType='hostname', data='PC-Robb'),
    AlertArtifact(dataType='ip', data='94.23.172.164', message='real IOC, do not browse'),
    AlertArtifact(dataType='username', data='robb@training.org')
]

customFields = CustomFieldHelper()\
    .add_string('businessUnit', 'Finance')\
    .add_string('location', 'Sydney')\
    .build()

sourceRef = str(uuid.uuid4())[0:6]

alert = Alert(title='User connected to known malicious IP over Telnet',
    tlp=3,
    tags=['source:edr', 'protocol: telnet', 'ex2'],
    description='EDR automated alert: the user robb@training.org has connected to known malicious IP over Telnet',
    type='internal',
    source='EDR',
    sourceRef='EDR_' + sourceRef,
    artifacts=artifacts,
    customFields=customFields
)

try:
   response = api.create_alert(alert)

   # Print the JSON response 
   #print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
   print("Alert create error: {}".format(e))


#alert on malicious hashes 

artifacts = [
    AlertArtifact(dataType='hash', data='BBDE33F5709CB1452AB941C08ACC775E', message= 'real IOC'),
    AlertArtifact(dataType='hostname', data='PC-Robb'),    
]

customFields = CustomFieldHelper()\
    .add_string('businessUnit', 'Finance')\
    .add_string('location', 'Sydney')\
    .build()

sourceRef = str(uuid.uuid4())[0:6]

alert = Alert(title='Malicious payload detected',
    tlp=3,
    tags=['source:edr', 'log-source:endpoint-protection', 'ex2'],
    description='EDR automated alert: malicious payload detected on computer PC-Robb',
    type='internal',
    source='EDR',
    sourceRef='EDR_' + sourceRef,
    artifacts=artifacts,
    customFields=customFields
)

try:
   response = api.create_alert(alert)

   # Print the JSON response
   #print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
   print("Alert create error: {}".format(e))
