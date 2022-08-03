user_host_main_version = '2.4.2'

from random import choice
from requests import get
from time import sleep
from os import makedirs, path, system as system_caller

global_page = ''

def verify_global_site():
    global global_page
    while True:
        try:
            print(f'\n\nExpected global page : {global_page}')
            if get(f"{global_page}/ping", timeout=10).text == 'ping':
                break
            else:
                _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=10).text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                global_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Unable to connect to github. Recheck internet connection?")
                sleep(1)


## Check self version
system_caller('cls')
while True:
    verify_global_site()
    try:
        print("\n\nChecking user host main version...")
        current_version = get(f"{global_page}/current_user_host_main_version", timeout=10).text
        if current_version == user_host_main_version:
            break
        else:
            current_version_split = current_version.split('.')
            version_split = user_host_main_version.split('.')
            if version_split[0] == current_version_split[0]:
                if version_split[1] != current_version_split[1]:
                    print(f"An recommended update is available. v{current_version}. Please download from github for important patches.\n https://github.com/BhaskarPanja93/Adfly-View-Bot-Client/releases")
                    sleep(5)
                else:
                    print(f"An optional update is available. v{current_version}")
                    sleep(5)
                break
            else:
                print(f"User Host Main is too old to run. Please update to v{current_version} to continue!!\n https://github.com/BhaskarPanja93/Adfly-View-Bot-Client/releases")
                input()
                exit()
    except:
        print("Retrying...")

### Check local drive to use
system_caller('cls')
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
        input()
        exit()

live_location = f"{local_drive_name}://adfly_files"
updates_location = f"{local_drive_name}://adfly_files/updates"

### If first run, make necessary directories
if not path.exists(live_location) or not path.exists(updates_location):
    makedirs(live_location, exist_ok=True)
    makedirs(updates_location, exist_ok=True)
    with open(f'{live_location}/DO NOT MODIFY!!.txt', 'w') as file:
        file.write("Do not modify any file in this directory. It can cause conflicts and/or security bugs")

### check user_host version
system_caller('cls')
verify_global_site()
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
        response = get(f"{global_page}/other_files?file_code={file_code}&version={version}", timeout=30).content
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
                _ = 1 / 0
        else:
            _ = 1 / 0
    except:
        print("Retrying...")
        sleep(1)
system_caller(f'{live_location}/user_host.exe')
