##############################################################
## RUN CLI COMMAND ON ONE OR MORE SWITCHES AND WRITE OUTPUT TO FILE
## ADD SWITCH IP's TO SWITCHES.TXT
##
##
## USEFULL LINK: https://community.arubanetworks.com/t5/Forum-Fran%C3%A7ais/How-to-REST-API-sur-ArubaOS-Switch/td-p/305020
##############################################################
import requests
import urllib3
import pprint
import json
import base64


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##############################################################
## GET ADMIN INFORMATION
##############################################################
username = input('Enter username: ')
password = input('Enter password: ')
credentials = {
               "userName" : username,
               "password" : password
                }

##############################################################
## GET IP ADDRESS INFORMATION
##############################################################
switch_input = input('Which file to open (swiches.txt, switches-access.txt or switches-core.txt: ')

ip_address = []
file = open(switch_input, "r")
for line in file:
    ip_address.append(line.strip('\n'))


##############################################################
## GET COMMAND INFORMATION
##############################################################
get_command = []
file = open("commands.txt", "r")
for line in file:
    get_command.append(line.strip('\n'))

##############################################################
## LETS GO
##############################################################

for ip in ip_address:
    url = 'https://{}/rest/v3/'.format(ip)


    ##############################################################
    ## LOGIN AND GET THE COOKIE
    ##############################################################
    get_cookie = requests.post(url + 'login-sessions', data=json.dumps(credentials), verify=False, timeout=5)
    print("")
    print("################################")
    print("YOU ARE LOGGING IN TO: {}".format(ip))
    print("LOGIN STATUS", get_cookie.status_code)
    if get_cookie.status_code == 201:
        print("LOGIN SUCCESS!")
    else:
        print("SOMETHING WENT WRONG!")

    cookie = get_cookie.json()['cookie']
    headers = {"Cookie" : cookie}

    ##############################################################
    ## GET HOSTNAME
    ##############################################################
    get_hostname = requests.get(url + 'system', headers=headers, verify=False, timeout=5)
    #pprint.pprint(get_hostname.json())
    hostname = get_hostname.json()['name']
    print("LETS START WITH SWITCH {}".format(hostname))

    ##############################################################
    ## RUN COMMAND
    ##############################################################
    for command in get_command:
        # CONVERT VARIABLE FROM BASE64 TO UTF-8
        encoded_command = base64.b64encode(command.encode('utf-8'))
        command_data = {"cli_batch_base64_encoded":encoded_command.decode('utf-8')}

        # RUN THE COMMAND
        run_cli = requests.post(url + 'cli_batch', data=json.dumps(command_data), headers=headers, verify=False, timeout=5)

        # FAILURE CHECK
        print("")
        print("COMMAND STATUS: ", run_cli.status_code)
        if run_cli.status_code == 202:
            print("COMMAND EXECUTED SUCCESSFULLY!")
        else:
            print("SOMETHING WENT WRONG!")

    ##############################################################
    ## LOGOUT AND GOODBYE
    ##############################################################
    delete_session = requests.delete(url + 'login-sessions', headers=headers, verify=False, timeout=5)
    print("")
    print("LOGOUT STATUS: {}".format(delete_session.status_code))
    if delete_session.status_code == 204:
        print("LOGOUT SUCCESS - GOODBYE!!!")
    else:
        print("LOGOUT WASN'T SUCCESSFUL")
    print("")
    print("=================================")