##############################################################
##
##
## DEFAULT LOGIN & LOGOUT SCRIPT
##
##
## USEFULL URL: https://community.arubanetworks.com/t5/Forum-Fran%C3%A7ais/How-to-REST-API-sur-ArubaOS-Switch/m-p/305020
##############################################################
import requests
import urllib3
import getpass
import json
import base64
import pprint

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

ip_address = "10.10.1.2"
url = 'https://{}/rest/v3/'.format(ip_address)


##############################################################
## LOGIN AND GET THE COOKIE
##############################################################
get_cookie = requests.post(url + 'login-sessions', data=json.dumps(credentials), verify=False, timeout=2)

print("Login Status", get_cookie.status_code)
if get_cookie.status_code == 201:
    print("LOGIN SUCCESS!")
else:
    print("SOMETHING WENT WRONG!")

cookie = get_cookie.json()['cookie']
headers = {"Cookie" : cookie}

get_system = requests.get(url + 'system', headers=headers, verify=False, timeout=2)
pprint.pprint(get_system.json())

##############################################################
## LOGOUT AND GOODBYE
##############################################################
delete_session = requests.delete(url + 'login-sessions', headers=headers, verify=False, timeout=2)
print("Logout Status: {}".format(delete_session.status_code))
if delete_session.status_code == 204:
    print("LOGOUT SUCCESS - GOODBYE!!!")
else:
    print("LOGOUT WASN'T SUCCESSFUL")
