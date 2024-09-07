# query REDCap
import requests
def get_rc_status():
    data = {
        'token': API_TOKEN,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'records[0]': '1',
        'fields[0]': 'record_id',
        'fields[1]': 'user_email',
        'fields[2]': 'last_name',
        'fields[3]': 'first_name',
        'fields[4]': 'data_file',
        'fields[5]': 'data_upload_complete',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    r = requests.post(RC_API_URL,data=data)
    rc_d = list()
    if r.status_code==200:
        rc_d = r.json()
    
    return rc_d

#print('HTTP Status: ' + str(r.status_code))
#print(r.json())

# function to download file given a redcap record_id
# @input: record_id
# @data_file_name: file name of the uploaded file
def get_rc_file(record_id, data_file_name):
    data = {
        'token': API_TOKEN,
        'content': 'file',
        'action': 'export',
        'record': '1',
        'field': 'data_file',
        'event': '',
        'returnFormat': 'json'
    }
    r = requests.post(RC_API_URL,data=data)
    if r.status_code==200:
        f = open(os.path.join(OUTPUT_DIR,"submission",str(record_id),data_file_name), 'wb')
        f.write(r.content)
        f.close()

