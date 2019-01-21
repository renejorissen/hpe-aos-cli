##############################################################
##
##
## ADD VLAN TO MULTIPLE SWITCH.
## ADD SWITCH IP ADDRESS TO switches.txt
## SCRIPT ASKS FOR CREDENTIALS AND VLAN INPUT
##
##
##############################################################
import requests
import urllib3
import pprint
import json
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##############################################################
## GET BASE INFORMATION
##############################################################
username = input('Enter username: ')
password = input('Enter password: ')
credentials = {
               "userName" : username,
               "password" : password
                }

##############################################################
## DEFINE VLAN
##############################################################
vlan_data = {"vlan_id": 1, "name": "vlanname"}
print("")
print("Enter the VLAN ID and name you would like to create")
get_vlan_id = int(input('Enter VLAN ID: '))
get_vlan_name = input('Enter VLAN name: ')
vlan_data['vlan_id'] = get_vlan_id
vlan_data['name'] = get_vlan_name



##############################################################
## GET IP ADDRESS INFORMATION
##############################################################
switch_input = input('Which file to open (swiches.txt, switches-access.txt or switches-core.txt: ')

ip_address = []
file = open(switch_input, "r")
for line in file:
    ip_address.append(line.strip('\n'))

for ip in ip_address:
    url = 'https://{}/rest/v3/'.format(ip)

##############################################################
## LOGIN AND GET THE COOKIE
##############################################################
    get_cookie = requests.post(url + 'login-sessions', data=json.dumps(credentials), verify=False, timeout=5)

    #print("Login Status", get_cookie.status_code)
    if get_cookie.status_code == 201:
        print("LOGIN SUCCESS!")
    else:
        print("SOMETHING WENT WRONG!")

    cookie = get_cookie.json()['cookie']
    headers = {"Cookie" : cookie}

##############################################################
## GET THE HOSTNAME
##############################################################
    get_system = requests.get(url + 'system', headers=headers, verify=False, timeout=5)
    #pprint.pprint(get_system.json())
    hostname = get_system.json()['name']
    #print(hostname)
    print("LETS START WITH SWITCH {}".format(hostname))

##############################################################
## CHECKING AND CREATING VLAN
##############################################################

    ## GET VLAN INFO
    get_vlan = requests.get(url + 'vlans', headers=headers, verify=False, timeout=5)
    pprint.pprint(get_vlan.json())

    ## APPEND ALL VLANS INTO A LIST
    vlan_list = []
    for key_id in get_vlan.json()['vlan_element']:
        vlan_list.append(key_id['vlan_id'])

    ## CHECK IF VLAN X IS CONFIGURED
    if get_vlan_id in vlan_list:
        print("VLAN {} already configured".format(get_vlan_id))
    else:
        print("VLAN doesn't exist. Let's create VLAN {}!!!!".format(get_vlan_id))

    ## CREATE THE VLAN
    post_vlan = requests.post(url + 'vlans', json=vlan_data, headers=headers, verify=False, timeout=5)
    print("")
    print("Response Code: {}".format(post_vlan.status_code))
    if post_vlan.status_code == 201:
        print("VLAN created successfully")
    else:
        print("Something went wrong!!")

##############################################################
## LOGOUT AND GOODBYE
##############################################################
    delete_session = requests.delete(url + 'login-sessions', headers=headers, verify=False, timeout=5)
    print("Logout Status: {}".format(delete_session.status_code))
    if delete_session.status_code == 204:
        print("LOGOUT SUCCESS - GOODBYE!!!")
    else:
        print("LOGOUT WASN'T SUCCESSFUL")
    print("")
    print("=================================")
