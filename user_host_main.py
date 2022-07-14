"""import sys

version = '2.0.0'

from random import choice
from requests import get
from subprocess import Popen
from time import sleep, time
from threading import Thread
from os import stat, remove, mkdir, path

global_host_page = ''
def verify_global_host_site():
    global global_host_page
    while True:
        try:
            print(f'Trying to connect to {global_host_page=}\n')
            if get(f"{global_host_page}/ping").text == 'ping':
                print("Successfully connected to global host!!")
                break
            else:
                _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                global_host_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Unable to connect to github. Recheck VM's internet connection?\n")
                sleep(1)


## Check self version
print("Checking self version")
while True:
    verify_global_host_site()
    try:
        current_version = get(f"{global_host_page}/current_user_host_main_version").text
        if current_version == version:
            break
        else:
            current_version_split = current_version.split('.')
            version_split = version.split('.')
            if version_split[0] == current_version_split[0]:
                print(f"A optional update is available. v{current_version}")
                sleep(5)
                break
            else:
                print(f"\n\nUser Host Main is too old to run. Please update to v{current_version} to continue!!\n https://github.com/BhaskarPanja93/Adfly-View-Bot-Client/releases")
                input()
    except:
        pass


### Check local drive to use
print('Checking directories')
local_drive_name = 'C'
if not path.exists(f"{local_drive_name}://"):
    for _ascii in range(67,90+1):
        local_drive_name = chr(_ascii)
        if path.exists(f"{local_drive_name}://"):
            break
    else:
        local_drive_name = ''
        print('No available local drive, please create a github issue!!')
        input()

data_location = f"{local_drive_name}://adfly_files"
updates_location = f"{local_drive_name}://adfly_files/updates"

### If first run, make necessary directories
if not path.exists(data_location):
    mkdir(data_location)
    mkdir(updates_location)
    with open(f'{data_location}/DO NOT MODIFY!!.txt', 'w') as file:
        file.write("Do not modify any file in this directory. It can cause conflicts and/or security bugs")
    with open(f'{data_location}/version', 'w') as file:
        file.write("0")
    print('Directories made!\n')


### check user_host version
print('Checking user_host version')
while True:
    try:
        verify_global_host_site()
        try:
            with open(f'{data_location}/version', 'r') as version_info_file:
                version = float(version_info_file.read())
        except:
            #open(f'{data_location}/version', 'w').write('0')
            version = 0
        sleep(2)
        s = time()
        response = get(f"{global_host_page}/exe_files?file_code=8&version={version}").content
        print(time()-s)
        if response[0] == 123 and response[-1] == 125:
            print("Data received. Preparing files...\n")
            response = eval(response)
            if response['file_code'] == '8':
                print(type(version), type(response['version']))
                if response['version'] != version:
                    print("\nWriting new file")
                    with open(f'{updates_location}/user_host.exe', 'wb') as file:
                        file.write(response['data'])
                    with open(f'{updates_location}/version', 'w') as file:
                        file.write(str(response['version']))
                else:
                    print("\nNo new Updates")
                break
        else:
            _ = 1 / 0
    except Exception as e:
        print(repr(e))
        pass

class Updater(Thread):
    _process = None
    check_interval = 3
    new_file_location = f'{updates_location}/user_host.exe'
    old_file_location = f'{data_location}/user_host.exe'
    new_version_location = f'{updates_location}/version'
    old_version_location = f'{data_location}/version'

    def __init__(self):
        Thread.__init__(self)
        self.last_file_stat = None
        self.last_file_stat = self.get_files()
        self.start_program(restart=False)

    def run(self):
        while True:
            sleep(self.check_interval)
            if self.check_updates():
                self.start_program(restart=True)

    def get_files(self):
        try:
            file_stat = [self.old_version_location, stat(self.old_version_location).st_mtime]
            return file_stat
        except:
            open(f'{data_location}/version', 'w').close()
            return self.get_files()


    def check_updates(self):
        file_stat = self.get_files()
        if self.last_file_stat != file_stat:
            self.last_file_stat = file_stat
            return True
        else:
            return False

    def start_program(self, restart):
        if self._process and not self._process.poll():
            self._process.kill()
            self._process.wait()
            sleep(1)
        if restart:
            print("UPDATE FOUND. Restarting...")
        else:
            print("DONE. Starting...")
        try:
            with open(self.new_file_location, 'rb') as new_f:
                with open(self.old_file_location, 'wb') as old_f:
                    old_f.write(new_f.read())
            with open(self.new_version_location, 'rb') as new_v:
                with open(self.old_version_location, 'rb') as old_:
                    if new_v.read() != old_.read():
                        with open(self.old_version_location, 'wb') as old_v:
                            old_v.write(new_v.read())
        except Exception as e:
            print(repr(e))
        try:
            remove(self.new_file_location)
            remove(self.new_version_location)
        except:
            pass
        #self._process = Popen(['conhost.exe', self.old_file_location])
        self._process = Popen([sys.executable, self.old_file_location])

Updater().start()
"""