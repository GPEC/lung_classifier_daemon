# query REDCap
import requests

# query REDCap and get all data
#
# @input rc_api_url
# @input api_token
# @return list with all data on REDCap
def get_rc_status(rc_api_url, api_token):
    data = {
        'token': api_token,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    r = requests.post(rc_api_url,data=data)
    rc_d = list()
    if r.status_code==200:
        rc_d = r.json()
    
    return rc_d

#print('HTTP Status: ' + str(r.status_code))
#print(r.json())

# function to download file given a redcap record_id
# @input: record_id
# @input rc_api_url
# @input api_token
# @data_file_name: file name of the uploaded file
def get_rc_file(record_id, rc_api_url, api_token, data_file_name):
    data = {
        'token': api_token,
        'content': 'file',
        'action': 'export',
        'record': record_id,
        'field': 'data_file',
        'event': '',
        'returnFormat': 'json'
    }
    r = requests.post(rc_api_url,data=data)
    if r.status_code==200:
        f = open(data_file_name, 'wb')
        f.write(r.content)
        f.close()

