while True:
    try:
        import requests
        break
    except:
        import pip
        pip.main(['install', 'requests'])


from random import choice
from requests import get
from os import mkdir, path
from subprocess import Popen
from time import sleep
from threading import Thread
from os import stat
global_host_page = 'http://10.10.77.118:65500'
adfly_data_location = "C://adfly_files"
if not path.exists(adfly_data_location):
    mkdir(adfly_data_location)
    mkdir(adfly_data_location+'/updates')
    with open(f'{adfly_data_location}/DO NOT MODIFY!!.txt', 'w') as file:
        file.write("Do not modify any file in this directory. It can cause conflicts and/or security bugs")
    print('Directories made!\n')

def verify_global_host_site():
    global global_host_page
    text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
    link_dict = eval(text)
    global_host_page = choice(link_dict['adfly_host_page_list'])

while get(f"{global_host_page}/ping").text != 'ping':
    print("Global host ping failed. Retrying... Maybe recheck your internet connection?")
    verify_global_host_site()
while True:
    try:
        print("Waiting for resources from global host.\n")
        response = get(f"{global_host_page}/py_files?file_code=8").content
        if response[0] == 123 and response[-1] == 125:
            print("Data received.\n")
            response = eval(response)
            if response['file_code'] == '8':
                with open(f'{adfly_data_location}/user_host.exe', 'wb') as file:
                    file.write(response['data'])
                with open(f'{adfly_data_location}/updates/user_host.exe', 'wb') as file:
                    file.write(response['data'])
                break
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
            print("Restarting...")
        else:
            print("Starting...")
        self._process = Popen(self.program_to_rerun)

Updater().start()