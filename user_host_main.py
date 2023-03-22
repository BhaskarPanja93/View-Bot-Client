user_host_main_version = '2.5.1'
from threading import Thread
from random import choice
from requests import get
from time import sleep
from os import makedirs, path, system as system_caller
import webbrowser


def fetch_global_addresses():
    while True:
        try:
            response = get("https://raw.githubusercontent.com/BhaskarPanja93/AllLinks.github.io/master/README.md", timeout=15)
            response.close()
            link_dict = eval(response.text)
            global_host_page = choice(link_dict['viewbot_global_host_page_list'])
            global_host_address = choice(link_dict['viewbot_tcp_connection_list']).split(":")
            global_host_address[-1] = int(global_host_address[-1])
            global_host_address = tuple(global_host_address)
            break
        except Exception as e:
            print(f"Unable to connect to GitHub : {repr(e)}")
            sleep(0.1)
    return global_host_address, global_host_page


system_caller('cls')
## Check self version
while True:
    global_host_address, global_host_page = fetch_global_addresses()
    try:
        print("\n\nChecking user host main version...")
        response = get(f"{global_host_page}/current_user_host_main_version", timeout=15)
        response.close()
        current_version = response.text
        if len(current_version) > 10 or current_version.count(".") != 2:
            raise ZeroDivisionError

        if current_version == user_host_main_version:
            break
        else:
            current_version_split = current_version.split('.')
            version_split = user_host_main_version.split('.')
            if version_split[0] == current_version_split[0]:
                if version_split[1] != current_version_split[1]:
                    print(f"An recommended update is available. v{current_version}. Please download from github for important patches.\n https://github.com/BhaskarPanja93/View-Bot-Client/releases")
                    sleep(5)
                    webbrowser.open("https://github.com/BhaskarPanja93/View-Bot-Client/releases", new=2)
                else:
                    print(f"An optional update is available. v{current_version}")
                    sleep(3)
                    webbrowser.open("https://github.com/BhaskarPanja93/View-Bot-Client/releases", new=2)
                break
            else:
                print(f"User Host Main is too old to run. Please update to v{current_version} to continue!!\n https://github.com/BhaskarPanja93/View-Bot-Client/releases")
                webbrowser.open("https://github.com/BhaskarPanja93/View-Bot-Client/releases", new=2)
                input()
                exit()
    except Exception as e:
        print(f"Retrying... : {repr(e)}")


system_caller('cls')
print("Version fetched...")


### Check local drive to use
print('\n\nChecking directories...')
local_drive_name = 'C'
if not path.exists(f"{local_drive_name}://"):
    for _ascii in range(67, 90 + 1):
        local_drive_name = chr(_ascii)
        if path.exists(f"{local_drive_name}://"):
            break
    else:
        local_drive_name = ''
        print('No available local drive, please create a github issue!!')
        sleep(2)
        webbrowser.open("https://github.com/BhaskarPanja93/View-Bot-Client/issues/new", new=2)
        input()
        exit()


live_location = f"{local_drive_name}://viewbot_files"
updates_location = f"{local_drive_name}://viewbot_files/updates"


### If first run, make necessary directories
if not path.exists(live_location) or not path.exists(updates_location):
    makedirs(live_location, exist_ok=True)
    makedirs(updates_location, exist_ok=True)
    with open(f'{live_location}/DO NOT MODIFY!!.txt', 'w') as file:
        file.write("Do not modify any file in this directory. It can cause conflicts and/or security bugs")


system_caller('cls')
print("Directories found...")


### check user_host version
try:
    with open(f'{live_location}/version', 'r') as version_info_file:
        version = float(version_info_file.read())
except:
    open(f'{live_location}/version', 'w').write('0')
    version = 0.0

while True:
    try:
        print('\n\nChecking user_host version...')
        print('This can take a while...')
        file_code = 'stable_user_host'
        global_host_address, global_host_page = fetch_global_addresses()
        response = get(f"{global_host_page}/other_files?file_code={file_code}&version={version}", timeout=40).content
        if response[0] == 123 and response[-1] == 125:
            system_caller('cls')
            print("\n\nData received.")
            response = eval(response)
            if response['file_code'] == file_code:
                if response['version'] != version:
                    print("Writing new file")
                    with open(f'{live_location}/user_host.exe', 'wb') as file:
                        file.write(response['data'])
                    with open(f'{live_location}/version', 'w') as file:
                        file.write(str(response['version']))
                else:
                    system_caller('cls')
                    print("\n\nNo new Updates")
                break
            else:
                raise ZeroDivisionError
        else:
            raise ZeroDivisionError
    except Exception as e:
        print(f"Retrying... : {repr(e)}")
        sleep(1)
Thread(target=system_caller, args=(f'{live_location}/user_host.exe',)).start()
