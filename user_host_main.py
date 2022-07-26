from random import choice
from requests import get
from time import sleep
from os import makedirs, path, system as system_caller

user_host_main_version = '2.1.1'
global_page = ''

def verify_global_site():
    global global_page
    while True:
        try:
            print(f'Trying to connect to global_page at {global_page}')
            if get(f"{global_page}/ping", timeout=5).text == 'ping':
                break
            else:
                _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=5).text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                global_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Unable to connect to github. Recheck internet connection?")
                sleep(1)


## Check self version
system_caller('cls')
print("Checking user host main version...\n\n")
while True:
    verify_global_site()
    try:
        current_version = get(f"{global_page}/current_user_host_main_version", timeout=5).text
        if current_version == user_host_main_version:
            break
        else:
            current_version_split = current_version.split('.')
            version_split = user_host_main_version.split('.')
            if version_split[0] == current_version_split[0]:
                print(f"An optional update is available. v{current_version}")
                sleep(5)
                break
            else:
                print(f"User Host Main is too old to run. Please update to v{current_version} to continue!! https://github.com/BhaskarPanja93/Adfly-View-Bot-Client/releases")
                input()
                exit()
    except:
        pass

### Check local drive to use
system_caller('cls')
print('Checking directories...\n\n')
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
print('Checking user_host version...\n\n')
print('This can take a while...\n\n')
while True:
    verify_global_site()
    try:
        with open(f'{live_location}/version', 'r') as version_info_file:
            version = float(version_info_file.read())
    except:
        open(f'{live_location}/version', 'w').write('0')
        version = 0.0
    try:
        response = get(f"{global_page}/other_files?file_code=8&version={version}", timeout=10).content
        if response[0] == 123 and response[-1] == 125:
            print("Data received. Preparing files...")
            response = eval(response)
            if response['file_code'] == '8':
                if response['version'] != version:
                    print("Writing new file")
                    with open(f'{live_location}/user_host.exe', 'wb') as file:
                        file.write(response['data'])
                    with open(f'{live_location}/version', 'w') as file:
                        file.write(str(response['version']))
                else:
                    print("No new Updates")
                break
            else:
                _ = 1 / 0
        else:
            _ = 1 / 0
    except:
        print("Retrying...")
        sleep(1)
system_caller(f'{live_location}/user_host.exe')