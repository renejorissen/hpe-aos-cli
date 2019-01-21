##############################################################
##
##
## DELETE PORT FROM A VLAN
## ADD SWITCH IP ADDRESS TO switches.txt
## SCRIPT ASKS FOR CREDENTIALS AND VLAN AND PORT INPUT
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
vlan_port_data = {"vlan_id": 1,"port_id":"Trk1"}
print("")
print("Enter the VLAN ID and the port you like to delete from the VLAN")
get_vlan_id = int(input('Enter VLAN ID: '))
str_vlan_id = str(get_vlan_id)
get_port_id = input('Enter Port-Id (1,2,3,Trk1): ')

vlan_port_data['vlan_id'] = get_vlan_id
vlan_port_data['port_id'] = get_port_id




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
## DELETE PORT FROM VLAN
##############################################################

    ## CHANGE PORT STATUS ON VLAN
    add_port_to_vlan = requests.delete(url + 'vlans-ports/' + str_vlan_id + "-" + get_port_id, headers=headers, verify=False, timeout=2)

    ## CHECK IF COMMAND EXECUTED SUCCESSFULLY
    print("")
    print("Response Code: {}".format(add_port_to_vlan.status_code))
    if add_port_to_vlan.status_code == 204:
        print("Port added to VLAN")
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
