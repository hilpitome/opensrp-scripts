
import requests
import json
from datetime import datetime
now = datetime.now()

current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
current_filename = "server_versions_"+current_time
print(current_filename)

# api-endpoint  
URL = "http://localhost:8080/opensrp"
access_token = ""

with open('config.json', 'r') as f:
    config = json.load(f)

def is_monotonic(arr):
    for i in range (len(arr)-1):
        if(arr[i+1]<arr[i]):
            return False
    return True

def parse_server_versions(resp):
    cv =0
    line = ""
    versions = []
    print(resp)
    for obj in resp:
        line +=" "+str(obj['serverVersion'])
        cv = obj['serverVersion']
        versions.append(cv)
    line += " "+str(is_monotonic(versions))
    # Open a file with access mode 'a'
    filename = current_filename+'.txt'
    file_object = open(filename, 'a')
    file_object.write(line+'\n')
    file_object.close()
    # update the last client
    # print(resp[len(versions)-1])
    # update_client(resp[len(versions)-1])
    return cv

def post_client():
    # data
    data = {
        "_id": "645ff071-4228-4e04-b93a-55926aeaa92e",
        "_rev": "v1",
        "type": "Client",
        "gender": "female",
        "teamId": "9206b39f-918a-436b-8459-4faf41301a15",
        "lastName": "Joao",
        "addresses": [
            {
                "addressType": "",
                "addressFields": {
                    "address": "Kapalanga"
                }
            }
        ],
        "birthdate": "1975-08-15T13:00:00.000+01:00",
        "firstName": "Suzana",
        "attributes": {
            "lives": "urban",
            "religion": "christianity",
            "employment": "not_employed",
            "tel_owner1": "family_member",
            "no_children": "3",
            "tel_number1": "923344305",
            "marital_status": "living_with_partner",
            "highest_education": "lower_secondary"
        },
        "locationId": "0201cb6d-2018-4bb5-9945-ad1e94a81ea9",
        "middleName": "Antonio",
        "dateCreated": "2021-04-26T10:13:49.286+01:00",
        "identifiers": {
            "M_ZEIR_ID": "114610-9"
        },
        "baseEntityId": "40f5af7f-5df0-4f13-9bd6-0b4ddf229548",
        "serverVersion": 797,
        "birthdateApprox": False,
        "deathdateApprox": False
    }
    serverVersion = 0
    # defining a params dict for the parameters to be sent to the API

    HEADERS  = {'access-token': 'Bearer '+access_token}
    
    # sending get request and saving the response as response object
    r = requests.post(url = URL, data = data, headers=HEADERS)
    
    # extracting data in json format
    data = r.json()
    
    print(data)  

def get_all_clients(serverVersion, limit):
    endpoint = '/rest/client/getAll'
    PARAMS = {'serverVersion':serverVersion, 'limit':limit}
    HEADERS  = {"access-token": "Bearer "+access_token}
    print(HEADERS)
    r = requests.get(URL+endpoint, params=PARAMS,headers=HEADERS)
    return parse_server_versions(r.json())
    # print(json.load(r.text))

def update_client(data):
    # data
   
    serverVersion = 0
    # defining a params dict for the parameters to be sent to the API

    HEADERS  = {'access-token': 'Bearer '+access_token}
    
    # sending get request and saving the response as response object
    r = requests.post(url = URL+'/rest/event/add', data = data, headers=HEADERS)
    
    # extracting data in json format
    d = r.status_code
    # print(d)
    

def authorize():
    global access_token
    body = {
        'grant_type':config['grant_type'],
        'username':config['username'],
        'password':config['password'],
        'scope':config['scope'],
        'client_id':config['client_id'],
        'client_secret':config['client_secret']
    }
    r = requests.post(url = config['keycloak_access_token'], data = body)

    access_token =  r.json()['access_token']
    print(access_token)
  

authorize()

current_server_version = 0
while (current_server_version < 77443):
    current_server_version = get_all_clients(current_server_version, 100)
    current_server_version+=1
    
   


# for x in range(2):
#     post_client(URL)
