##############################################################
##
##
## DELETE VLAN ON MULTIPLE SWITCH
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
vlan_data = {"vlan_id": 1}
print("")
print("Enter the VLAN ID you like to delete")
get_vlan_id = int(input('Enter VLAN ID: '))
str_vlan_id = str(get_vlan_id)
vlan_data['vlan_id'] = get_vlan_id

##############################################################
## GET IP ADDRESS INFORMATION
##############################################################
ip_address = []
file = open("switches.txt", "r")
for line in file:
    ip_address.append(line.strip('\n'))

for ip in ip_address:
    url = 'https://{}/rest/v3/'.format(ip)

##############################################################
## LOGIN AND GET THE COOKIE
##############################################################
    get_cookie = requests.post(url + 'login-sessions', data=json.dumps(credentials), verify=False, timeout=2)

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
    get_system = requests.get(url + 'system', headers=headers, verify=False, timeout=2)
    #pprint.pprint(get_system.json())
    hostname = get_system.json()['name']
    #print(hostname)
    print("LETS START WITH SWITCH {}".format(hostname))

##############################################################
## CHECKING AND CREATING VLAN
##############################################################

    ## GET VLAN INFO
    get_vlan = requests.get(url + 'vlans', headers=headers, verify=False, timeout=2)
    #pprint.pprint(get_vlan.json())

    ## APPEND ALL VLANS INTO A LIST
    vlan_list = []
    for key_id in get_vlan.json()['vlan_element']:
        vlan_list.append(key_id['vlan_id'])

    ## CHECK IF VLAN X IS CONFIGURED
    if get_vlan_id in vlan_list:
        print("VLAN {} does exist, so lets delete it!!!!".format(get_vlan_id))
    else:
        print("VLAN doesn't exist. No action needed".format(get_vlan_id))

    ## DELETE THE VLAN
    post_vlan = requests.delete(url + 'vlans/' + str_vlan_id, json=vlan_data, headers=headers, verify=False, timeout=2)
    print("")
    print("Response Code: {}".format(post_vlan.status_code))
    if post_vlan.status_code == 204:
        print("VLAN deleted successfully")
    else:
        print("Something went wrong!!")

##############################################################
## LOGOUT AND GOODBYE
##############################################################
    delete_session = requests.delete(url + 'login-sessions', headers=headers, verify=False, timeout=2)
    print("Logout Status: {}".format(delete_session.status_code))
    if delete_session.status_code == 204:
        print("LOGOUT SUCCESS - GOODBYE!!!")
    else:
        print("LOGOUT WASN'T SUCCESSFUL")
    print("")
    print("=================================")
