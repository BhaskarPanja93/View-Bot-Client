from random import choice
from requests import get
from os import mkdir, path
from subprocess import Popen
from time import sleep
from threading import Thread
from os import stat

global_host_page = ''
adfly_data_location = "C://adfly_files"

if not path.exists(adfly_data_location):
    mkdir(adfly_data_location)
    mkdir(adfly_data_location+'/updates')
    with open(f'{adfly_data_location}/DO NOT MODIFY!!.txt', 'w') as file:
        file.write("Do not modify any file in this directory. It can cause conflicts and/or security bugs")
    print('Directories made!\n')

def verify_global_host_site():
    global global_host_page
    while True:
        try:
            print(f'Trying to connect to {global_host_page=}\n')
            if get(f"{global_host_page}/ping").text == 'ping':
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
                print("Unable to connect to github. Maybe recheck VM's internet connection?\n")
                sleep(1)

while True:
    try:
        verify_global_host_site()
        response = get(f"{global_host_page}/py_files?file_code=8").content
        if response[0] == 123 and response[-1] == 125:
            print("Data received. Preparing files...\n")
            response = eval(response)
            if response['file_code'] == '8':
                with open(f'{adfly_data_location}/updates/user_host.exe', 'wb') as file:
                    file.write(response['data'])
                break
        else:
            _ = 1/0
    except:
        pass

class Updater(Thread):
    _process = None
    check_interval = 3 ## time to wait (in seconds) before every check is run
    file_to_check = f'{adfly_data_location}/updates/user_host.exe' ## name of file to check for changes
    program_to_rerun = f'{adfly_data_location}/user_host.exe' ## name of program to restart

    def __init__(self):
        Thread.__init__(self)
        self.last_file_stat = self.get_files()
        self.start_program(restart= False)

    def run(self):
        while True:
            sleep(self.check_interval)
            if self.check_updates():
                self.start_program(restart= True)

    def get_files(self):
        file_stat = [self.file_to_check, stat(self.file_to_check).st_mtime]
        return file_stat

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
        if restart:
            print("UPDATE FOUND. Restarting...")
        else:
            print("DONE. Starting...")
        with open(self.file_to_check, 'rb') as updated_file:
            with open(self.program_to_rerun, 'wb') as old_file:
                old_file.write(updated_file.read())
        self._process = Popen(self.program_to_rerun)

Updater().start()