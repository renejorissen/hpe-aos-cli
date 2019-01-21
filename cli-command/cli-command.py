##############################################################
## RUN CLI COMMAND ON ONE OR MORE SWITCHES AND WRITE OUTPUT TO FILE
##
## ADD SWITCH IP's TO SWITCHES.TXT
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
ip_address = []
file = open("switches.txt", "r")
for line in file:
    ip_address.append(line.strip('\n'))


##############################################################
## GET COMMAND INFORMATION
##############################################################
get_command = input("What command would you like to execute:")
cli_command = {"cmd": get_command}


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
    ## GET HOSTNAME & OPEN FILE
    ##############################################################
    get_hostname = requests.get(url + 'system', headers=headers, verify=False, timeout=5)
    #pprint.pprint(get_hostname.json())
    hostname = get_hostname.json()['name']
    file = open("SW{}_{}_{}.txt".format(ip, hostname, get_command), "w")


    ##############################################################
    ## RUN COMMAND
    ##############################################################
    run_cli = requests.post(url + 'cli', data=json.dumps(cli_command), headers=headers, verify=False, timeout=5)
    result_decode = base64.b64decode(run_cli.json()['result_base64_encoded']).decode('utf-8')
    #print(result_decode)
    file.write(result_decode)
    file.close()
    print("")
    print("COMMAND STATUS: ", run_cli.status_code)
    if run_cli.status_code == 200:
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