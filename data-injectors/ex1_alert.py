import time
import requests
import sys
import json
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper, Case, CaseTaskLog

api = TheHiveApi('URL', 'SECRET')

artifacts = [
    AlertArtifact(dataType='url', data='https://poczta.pl-getbuys.icu/', message = 'http method: POST'),
    AlertArtifact(dataType='domain', data='pl-getbuys.icu'),
    AlertArtifact(dataType='mail', data='robb@training.org'),
    AlertArtifact(dataType='username', data='robb@training.org')
]

customFields = CustomFieldHelper()\
    .add_string('businessUnit', 'Finance')\
    .add_string('location', 'Sydney')\
    .build()

sourceRef = str(uuid.uuid4())[0:6]

alert = Alert(title='User posted information on known phishing URL',
    tlp=3,
    tags=['source:siem', 'log-source:proxy'],
    description='SIEM automated alert: the user robb@training.org has posted information on a known phishing url',
    type='external',
    source='SIEM',
    sourceRef=sourceRef,
    artifacts=artifacts,
    customFields=customFields
)

try:
   response = api.create_alert(alert)

   # Print the JSON response
   #print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
   print("Alert create error: {}".format(e))


#old alert/case
artifacts = [
    AlertArtifact(dataType='ip', data='94.154.129.50'),
    AlertArtifact(dataType='url', data='https://moneyfornothing.pl-getbuys.icu/', message = 'http method: POST'),
#    AlertArtifact(dataType='mail', data='robb@training.org')
#    AlertArtifact(dataType='username', data='robb@training.org')
]

customFields = CustomFieldHelper()\
    .add_string('businessUnit', 'Finance')\
    .add_string('location', 'Sydney')\
    .build()

sourceRef = str(uuid.uuid4())[0:6]

alert = Alert(title='User posted information on known phishing URL',
    tlp=3,
    tags=['source:siem', 'log-source:proxy'],
    description='SIEM automated alert: the user robb@training.org has posted information on a known phishing url',
    type='external',
    source='SIEM',
    sourceRef=sourceRef,
    artifacts=artifacts,
    customFields=customFields
)

try:
   response = api.create_alert(alert)

   # Print the JSON response
   #print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
   print("Alert create error: {}".format(e))

#promote old alert as case
alert = response.json()
alert_id = alert['_id']
promote=api.promote_alert_to_case(alert_id, case_template='Phishing')
case_imported = promote.text
case = json.loads(case_imported)

#adding some task logs
time.sleep(3)
case_id = case['_id']
case_tasks = api.get_case_tasks(case_id)
print(case_tasks.text)
response = json.loads(case_tasks.text)
idItem=0
for item in response:
    ctid = (response[idItem]['id'])
    if (response[idItem]['title']) == 'Initial alert':
        ctl = CaseTaskLog(message='SIEM Alert about the user account robb@training.org posting data on a phishing URL. Source: Proxy, TI Feeder: MISP')
        api.create_task_log(ctid,ctl)
    elif (response[idItem]['title']) == 'Analysis':
        ctl = CaseTaskLog(message='no referer, user most probably clicked this link on an phishing email. Edit: user confirmed.')
        api.create_task_log(ctid,ctl)
    elif (response[idItem]['title']) == 'Notification / Communication':
        ctl = CaseTaskLog(message="from: csirt@training.org \r\n\r to: robb@training.org \r\n\r subject: case #1234 - phishing \r\n\r Dear robb, \r\n\r Please come to our office monday 8am to follow the awareness training about phishing. \r\n\r Regards, \r\n\r CSIRT")
        api.create_task_log(ctid,ctl)
    elif (response[idItem]['title']) == 'Remediation':
        ctl = CaseTaskLog(message='Robb agreed to change his password and follow an awareness training')
        api.create_task_log(ctid,ctl)
    elif (response[idItem]['title']) == 'Lessons learnt':
        ctl = CaseTaskLog(message='every newcomer should follow cybersecurity awareness')
        api.create_task_log(ctid,ctl)
    idItem+=1

#closing the case with modified date
case_id = case['_id']
case_temp=api.get_case(case_id)
case_data=case_temp.json()
case_data['startDate'] = 1587409512000
case_data['status'] = "Resolved"
case_data['resolutionStatus'] = "TruePositive"
case_data['impactStatus'] = "NoImpact"
case_data['summary'] = "user changed his password. no suspicious activity on his account since he being phished."
print(case_data)
api.update_case(case=Case(json=case_data), fields=['startDate','status','resolutionStatus','impactStatus','summary'])
