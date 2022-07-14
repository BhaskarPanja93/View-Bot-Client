import socket
import webbrowser
from os import popen, system as system_caller, mkdir, path
from random import randrange
from time import time, localtime
from random import choice
from time import sleep
from threading import Thread
from cryptography.fernet import Fernet
from flask import Flask, request, redirect, make_response, render_template_string
from ping3 import ping
from turbo_flask import Turbo
from psutil import virtual_memory, cpu_percent as cpu
from requests import get


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

if not path.exists(data_location):
    mkdir(data_location)
    mkdir(updates_location)
    with open(f'{data_location}/DO NOT MODIFY!!.txt', 'w') as file:
        file.write("Do not modify any file in this directory. It can cause conflicts and/or security bugs")

vbox_manage_binary_location = "VBoxManage.exe"
possible_vbox_locations = ["C://Program Files/Oracle/VirtualBox/VBoxManage.exe",
                           "D://Programas/Virtual Box",
                           "C:\Program Files\Oracle\VirtualBox"]

for location in possible_vbox_locations:
    if path.exists(location):
        vbox_manage_binary_location = location
        break
else:
    print("VirtualBox path not found, make sure you have Oracle Virtualbox installed, else create a github issue here: https://github.com/BhaskarPanja93/Adfly-View-Bot-Client/discussions")
    input()

start_time = time()
bot_metrics_written = False
vms_to_use_written = False
vm_manager_start_vm = True
vm_manager_working = True
per_vm_memory = default_per_vm_memory = 1228
max_vm_count = default_max_vm_count = 0
max_memory_percent = default_max_memory_percent = 70
rtc_start = default_rtc_start = ['00','00']
rtc_stop = default_rtc_stop = ['23','59']
total_system_memory = virtual_memory()[0]
PRIVATE_HOST_PORT = 59999
PUBLIC_HOST_PORT = 60000
LOCAL_CONNECTION_PORT = 59998
global_host_address = ()
global_host_page = ''
host_cpu_percent, host_ram_percent = 0, 0
vm_stop_queue = []
vms_to_use = []
all_vms = []
vm_to_mac_address = {}
available_asciis = [].__add__(list(range(97, 122 + 1))).__add__(list(range(48, 57 + 1))).__add__(list(range(65, 90 + 1)))
reserved_u_names_words = ['invalid', 'bhaskar', 'eval(', ' ', 'grant', 'revoke', 'commit', 'rollback', 'select','savepoint', 'update', 'insert', 'delete', 'drop', 'create', 'alter', 'truncate', '<', '>', '.', '+', '-', '@', '#', '$', '&', '*', '\\', '/']
public_vm_data = {}
vm_stat_connections = {}
windows_img_files = {}
py_files = {}
global_host_auth_data = {}
messages_for_all = {'severe_info':[],
                    'notification_info':[{'message': "If you want to change the username this Host is serving, Re-Login <a href='http://127.0.0.1:59999'>> HERE <</a>.</br>NOTE: This page can only be opened from the Host PC's browsers!!", "duration":10}],
                    'success_info':[]}
messages_for_host = {'severe_info':[{'message':"If you want to host this page globally, only use <a href='https://ngrok.com/'>> ngrok <</a> else it can be a security risk!!", 'duration':10}],
                     'notification_info':[],
                     'success_info':[]}

def reprint_screen():
    adapters = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]
    while True:
        system_caller('cls')
        print("""
To change host account, login Here
(only from current PC): 
http://127.0.0.1:59999

To manage VMs and your account, login Here
(from any device in the network):""")
        for ip in adapters:
            print(f"http://{ip}:60000")
        sleep(10)


def verify_global_host_site():
    global global_host_page
    while True:
        try:
            if type(ping('8.8.8.8')) == float:
                break
        except:
            print("Please check your internet connection")
    while True:
        try:
            if get(f"{global_host_page}/ping").text == 'ping':
                break
            else:
                print("Unable to connect to global host...")
                _ = 1 / 0
        except:
            try:
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                global_host_page = choice(link_dict['adfly_host_page_list'])
            except:
                sleep(1)


def verify_global_host_address():
    global global_host_address
    while True:
        try:
            if type(ping('8.8.8.8')) == float:
                break
        except:
            print("Please check your internet connection")
    while True:
        try:
            text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
            link_dict = eval(text)
            host_ip, host_port = choice(link_dict['adfly_user_tcp_connection_list']).split(':')
            host_port = int(host_port)
            global_host_address = (host_ip, host_port)
            break
        except:
            sleep(1)


def force_connect_global_server():
    while True:
        try:
            if type(ping('8.8.8.8')) == float:
                break
        except:
            print("Please check your internet connection")
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            token = get(f"{global_host_page}/token_for_tcp_connection").text
            connection.connect(global_host_address)
            break
        except Exception:
            verify_global_host_site()
            sleep(1)
            verify_global_host_address()
    return connection, token


def __send_to_connection(connection, data_bytes: bytes):
    connection.sendall(str(len(data_bytes)).zfill(8).encode()+data_bytes)


def __receive_from_connection(connection):
    data_bytes = b''
    length = b''
    for _ in range(12000):
        if len(length) != 8:
            length += connection.recv(8 - len(length))
            sleep(0.01)
        else:
            break
    else:
        return b''
    if len(length) == 8:
        length = int(length)
        for _ in range(12000):
            data_bytes += connection.recv(length - len(data_bytes))
            sleep(0.01)
            if len(data_bytes) == length:
                break
        else:
            return b''
        return data_bytes
    else:
        return b''


def __try_closing_connection(connection):
    for _ in range(10):
        sleep(0.1)
        try:
            connection.close()
        except :
            pass


def return_all_vms():
    return_list = []
    return_dict = {}
    for line in popen(f'"{vbox_manage_binary_location}" list vms').readlines():
        if line:
            line = line.split()
            line.pop()
            name = ''
            for _ in line:
                name += _ + ' '
            uuid = get_vm_info(eval(name), 'UUID')
            return_list.append(uuid)
            return_dict[eval(name)] = get_vm_info(eval(name), 'macaddress1')
    global vm_to_mac_address
    vm_to_mac_address = return_dict
    return return_list


def return_running_vms():
    return_list = []
    for line in popen(f'"{vbox_manage_binary_location}" list runningvms').readlines():
        if line:
            line = line.split()
            line.pop()
            name = ''
            for _ in line:
                name += _ + ' '
            return_list.append(get_vm_info(eval(name), 'UUID'))
    return sorted(return_list)


def return_stopped_vms():
    return sorted((set(return_all_vms()) - set(return_running_vms())))


def start_vm(_id):
    if _id not in vm_stop_queue:
        system_caller(f'"{vbox_manage_binary_location}" startvm {_id} --type headless')


def queue_vm_stop(_id, user_delay, real_delay=0):
    if user_delay:
        Thread(target=queue_vm_stop, args=(_id, 0, user_delay,)).start()
        return
    if real_delay:
        sleep(real_delay)
    if _id not in vm_stop_queue:
        vm_stop_queue.append(_id)
        for _ in range(40):
            system_caller(f'"{vbox_manage_binary_location}" controlvm {_id} acpipowerbutton')
            sleep(1)
            if _id not in return_running_vms():
                vm_stop_queue.remove(_id)
                break
        else:
            system_caller(f'"{vbox_manage_binary_location}" controlvm {_id} poweroff')
            vm_stop_queue.remove(_id)


def get_vm_info(vm_name, info):
    for line in popen(f'"{vbox_manage_binary_location}" showvminfo "{vm_name}" --machinereadable').readlines():
        if info in line:
            try:
                key, value = line.split('=')
                return value.replace('\n','').replace('\"','').replace('\'','')
            except:
                pass

def randomise_mac_address(_id):
    system_caller(f'"{vbox_manage_binary_location}" modifyvm {_id} --macaddress1 auto')


def check_and_fix_repeated_mac_addresses(vm=None):
    write_vms_to_use()
    allocated_mac_addresses = []
    if not vm:
        for vm in vms_to_use:
            mac_address = get_vm_info(vm, 'macaddress1')
            while mac_address in allocated_mac_addresses:
                queue_vm_stop(vm, 0)
                randomise_mac_address(vm)
                mac_address = get_vm_info(vm, 'macaddress1')
            allocated_mac_addresses.append(mac_address)
    else:
        for _ in vms_to_use:
            mac_address = get_vm_info(_, 'macaddress1')
            allocated_mac_addresses.append(mac_address)
        mac_address = get_vm_info(vm, 'macaddress1')
        while mac_address in allocated_mac_addresses:
            queue_vm_stop(vm, 0)
            randomise_mac_address(vm)
            mac_address = get_vm_info(vm, 'macaddress1')


def u_name_matches_standard(u_name: str):
    for reserved_word in reserved_u_names_words:
        if reserved_word in u_name:
            return False
    return True


def password_matches_standard(password: str):
    has_1_number = False
    has_1_upper =False
    has_1_lower = False
    for _ in password:
        if _.islower():
            has_1_lower = True
        if _.isupper():
            has_1_upper = True
        if _.isdigit():
            has_1_number = True
    if has_1_number and has_1_lower and has_1_upper and len(password) >= 8:
        return True
    else:
        return False


def generate_random_string(_min, _max):
    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(choice(available_asciis))
    return string


def write_bot_metrics_to_file():
    global bot_metrics_written
    if bot_metrics_written:
        return
    global vm_manager_start_vm, per_vm_memory, max_vm_count, max_memory_percent, rtc_start, rtc_stop
    try:
        last_vm_metrics = eval(open(f'{data_location}/adfly_vm_metrics', 'r').read())
        per_vm_memory = last_vm_metrics['per_vm_memory']
        max_vm_count = last_vm_metrics['max_vm_count']
        max_memory_percent = last_vm_metrics['max_memory_percent']
        rtc_start = last_vm_metrics['rtc_start']
        rtc_stop = last_vm_metrics['rtc_stop']
    except:
        per_vm_memory = default_per_vm_memory
        max_vm_count = default_max_vm_count
        max_memory_percent = default_max_memory_percent
        rtc_start = default_rtc_start
        rtc_stop = default_rtc_stop
        open(f'{data_location}/adfly_vm_metrics', 'w').write(str({'per_vm_memory': per_vm_memory, 'max_vm_count': max_vm_count, 'max_memory_percent': max_memory_percent, 'rtc_start': rtc_start, 'rtc_stop': rtc_stop}))
    bot_metrics_written = True


def write_vms_to_use():
    global all_vms, vms_to_use, vms_to_use_written
    if vms_to_use_written:
        return
    all_vms = return_all_vms()
    try:
        vms_to_use = []
        last_vms_to_use = eval(open(f'{data_location}/adfly_vm_manager', 'r').read())['vms_to_use']
        for vm_uuid in all_vms:
            if vm_uuid in last_vms_to_use:
                vms_to_use.append(vm_uuid)
    except:
        vms_to_use = []
        open(f'{data_location}/adfly_vm_manager', 'w').write(str({'vms_to_use': vms_to_use}))
    vms_to_use_written = True


def vm_manager_time_manager():
    global vm_manager_start_vm
    current = [int(localtime()[3]), int(localtime()[4])]
    start = [int(rtc_start[0]), int(rtc_start[1])]
    stop = [int(rtc_stop[0]), int(rtc_stop[1])]
    if stop[0] > start[0]:
        if stop[0] > current[0] > start[0]:
            vm_manager_start_vm = True
        elif stop[0] == current[0]:
            if stop[1] > current[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        elif current[0] == start[0]:
            if current[1] >= start[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False

    elif stop[0] < start [0]:
        if stop[0] > current[0] > 0 or 24 > current[0] > start[0]:
            vm_manager_start_vm = True
        elif stop[0] == current[0]:
            if stop[1] > current[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        elif current[0] == start[0]:
            if current[1] >= start[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False

    elif stop[0] == start[0]:
        if stop[1] < current[1] >= start[1]:
            vm_manager_start_vm = True
        else:
            vm_manager_start_vm = False


def vm_manager():
    check_and_fix_repeated_mac_addresses()
    while True:
        sleep(5)
        if vm_manager_working:
            vm_manager_time_manager()
            if vm_manager_start_vm:
                total_system_memory, current_memory_percent = virtual_memory()[0], virtual_memory()[2]
                per_vm_memory_percent = int((per_vm_memory*1024*1024/total_system_memory)*100)+1
                _ = return_running_vms()
                working_vms = []
                write_vms_to_use()
                for vm in _:
                    if vm in vms_to_use:
                        working_vms.append(vm)
                _ = return_stopped_vms()
                stopped_vms = []
                for vm in _:
                    if vm in vms_to_use:
                        stopped_vms.append(vm)
                if working_vms and len(working_vms) > max_vm_count:
                    vms_count_to_stop = len(working_vms) - max_vm_count
                    while vms_count_to_stop:
                        if working_vms:
                            chosen_vm = choice(working_vms)
                            if chosen_vm not in vm_stop_queue:
                                queue_vm_stop(chosen_vm, 0)
                                #Thread(target=queue_vm_stop, args=(chosen_vm, 0,)).start()
                                vms_count_to_stop -= 1
                                sleep(0.5)
                        else:
                            break

                elif working_vms and current_memory_percent > max_memory_percent:
                    vms_count_to_stop = ((current_memory_percent - max_memory_percent)//per_vm_memory_percent) + 1
                    while vms_count_to_stop:
                        if working_vms:
                            chosen_vm = choice(working_vms)
                            if chosen_vm not in vm_stop_queue:
                                queue_vm_stop(chosen_vm, 0)
                                # Thread(target=queue_vm_stop, args=(chosen_vm, 0,)).start()
                                vms_count_to_stop -= 1
                                sleep(0.5)
                        else:
                            break
                else:
                    vms_count_to_start = min((max_memory_percent - current_memory_percent)//per_vm_memory_percent, max_vm_count - len(working_vms))
                    while stopped_vms and vms_count_to_start:
                        chosen_vm = choice(stopped_vms)
                        if chosen_vm not in vm_stop_queue:
                            start_vm(chosen_vm)
                            queue_vm_stop(chosen_vm, 3600)
                            # Thread(target=queue_vm_stop, args=(chosen_vm, 3600,)).start()
                            vms_count_to_start -= 1
                            sleep(0.5)
            else:
                _ = return_running_vms()
                working_vms = []
                for vm in _:
                    if vm in vms_to_use:
                        working_vms.append(vm)
                for vm in working_vms:
                    Thread(target=queue_vm_stop, args=(vm, 0)).start()


def global_host_peering_authenticator():
    global global_host_auth_data
    global_host_auth_data = {}
    try:
        last_global_host_peering_data = eval(open(f'{data_location}/adfly_local_host_authenticator', 'r').read())
        for u_name in last_global_host_peering_data:
            global_host_auth_data[u_name] = {'auth_token': last_global_host_peering_data[u_name]}
    except:
        pass
    if global_host_auth_data:
        for u_name in global_host_auth_data:
            connection, binding_token = force_connect_global_server()
            data_to_be_sent = {'purpose': 'host_authentication', 'binding_token':binding_token}
            __send_to_connection(connection, str(data_to_be_sent).encode())
            data_to_send = {'purpose': 'auth_token', 'u_name':u_name, 'auth_token': global_host_auth_data[u_name]['auth_token'], 'network_adapters': [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]}
            __send_to_connection(connection, str(data_to_send).encode())
            response = __receive_from_connection(connection)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    pass
                elif response['status_code'] < 0:
                    webbrowser.open(f'http://127.0.0.1:59999/?reason={u_name} authentication Revoked. Please Relogin!', new=2)
    else:
        webbrowser.open(f'http://127.0.0.1:59999/?reason=Login with your account. Controlling the VMs in this PC will only be possible by this account.', new=2)


def keep_user_global_host_connection_alive(viewer_id):
    while viewer_id in turbo_app.clients and viewer_id in active_viewers:
        prev_token = active_viewers[viewer_id]['global_host_send_token']
        sleep(30)
        if viewer_id in turbo_app.clients and viewer_id in active_viewers and '' != active_viewers[viewer_id]['global_host_send_token'] == prev_token:
            while viewer_id in active_viewers:
                try:
                    token = active_viewers[viewer_id]['global_host_send_token']
                    if token:
                        active_viewers[viewer_id]['global_host_send_token'] = ''
                        break
                except:
                    sleep(0.1)
            else:
                return
            send_data = {'token': token, 'purpose': 'ping'}
            connection = active_viewers[viewer_id]['global_host_connection']
            try:
                __send_to_connection(connection, str(send_data).encode())
                response_string = __receive_from_connection(connection)
                if response_string[0] == 123 and response_string[-1] == 125:
                    response_dict = eval(response_string)
                    active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            except:
                force_send_flask_data(f"[FAILURE] server connection error", 'severe_info', viewer_id, 'new_div', 0, 5)
                account_div_manager(viewer_id, reconnect=True)
                break


def remove_viewer(viewer_id):
    while viewer_id in turbo_app.clients:
        sleep(1)
    else:
        print(f'{viewer_id[0:4]}...{viewer_id[len(viewer_id) - 4:len(viewer_id)]} disconnected')
        for _ in range(10):
            try:
                active_viewers[viewer_id]['global_host_connection'].close()
                sleep(0.1)
            except:
                pass
        try:
            del active_viewers[viewer_id]
        except:
            pass


def process_form_action(viewer_id:str, form:dict):
    if form['purpose'] == 'base_form':
        if form['choice'] == 'create_new_account':
            force_send_flask_data(public_templates['create_new_account_form'], 'private_div', viewer_id, 'update', 0, 0)
            send_new_csrf_token('create_new_account', viewer_id)
        elif form['choice'] == 'login':
            force_send_flask_data(public_templates['login_form'], 'private_div', viewer_id, 'update', 0, 0)
            send_new_csrf_token('login', viewer_id)


    elif form['purpose'] == 'create_new_account':
        username = form['username'].strip().lower()
        password1 = form['password1']
        password2 = form['password2']
        if not u_name_matches_standard(username):
            force_send_flask_data("Username not allowed(has unwanted characters or words)", 'severe_info', viewer_id, 'new_div', 0, 3)
            return
        if password2 != password1:
            force_send_flask_data("Password don't match", 'severe_info', viewer_id, 'new_div', 0, 3)
            return
        elif not password_matches_standard(password2):
            force_send_flask_data("Password too easy.", 'severe_info', viewer_id, 'new_div', 0, 3)
            return
        else:
            password = password1
        div_name = force_send_flask_data(f'[WAITING] [Create New Account] Waiting for previous operations!', 'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Create New Account] Waiting for server to respond!', div_name, viewer_id, 'update', 0, 0)
        send_data = {'token':token, 'purpose':'create_new_account', 'u_name':username, 'password':password}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Create New Account] server connection error", 'severe_info', viewer_id, 'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Create New Account] Account Created", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                active_viewers[viewer_id]['additional_data'] = additional_data
                active_viewers[viewer_id]['u_name'] = username
            elif response_dict['status_code'] < 0:
                send_new_csrf_token('create_new_account', viewer_id)
                force_send_flask_data(f"[DENIED] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
        else:
                force_send_flask_data(f"[ERROR] [Create New Account] Something went wrong", 'severe_info', viewer_id, 'new_div', 0, 3)


    elif form['purpose'] == 'login':
        username = form['username'].strip().lower()
        password = form['password']
        div_name = force_send_flask_data(f'[WAITING] [Login] Waiting for previous operations!', 'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Login] Waiting for server to respond!', div_name, viewer_id, 'update', 0, 0)
        send_data = {'token':token, 'purpose':'login', 'u_name':username, 'password':password}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Login] server connection error", 'severe_info', viewer_id, 'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Login] Logged in!", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                active_viewers[viewer_id]['additional_data'] = additional_data
                active_viewers[viewer_id]['u_name'] = username
            elif response_dict['status_code'] < 0:
                send_new_csrf_token('login', viewer_id)
                force_send_flask_data(f"[DENIED] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
        else:
            force_send_flask_data(f"[ERROR] [Login] Something went wrong", 'severe_info', viewer_id, 'new_div', 0, 3)


    elif form['purpose'] == 'remove_account':
        acc_id = form['acc_id']
        div_name = force_send_flask_data(f'[WAITING] [Remove Account] Waiting for previous operations!', 'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Remove Account] Waiting for server to respond!', div_name, viewer_id, 'update', 0, 0)
        send_data = {'token':token, 'purpose':'remove_account', 'acc_id': acc_id}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Remove Account] server connection error", 'severe_info', viewer_id, 'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Remove Account] Account Removed", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                render_account_manage_table(viewer_id, additional_data['self_ids'])
            elif response_dict['status_code'] < 0:
                force_send_flask_data(f"[DENIED] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                render_account_manage_table(viewer_id, additional_data['self_ids'])
        else:
            force_send_flask_data(f"[ERROR] [Remove Account] Something went wrong", 'severe_info', viewer_id, 'new_div', 0, 3)


    elif form['purpose'] == 'add_account':
        send_new_csrf_token('add_account', viewer_id)
        acc_id = int(form['acc_id'])
        identifier = form['identifier']
        div_name = force_send_flask_data(f'[WAITING] [Add Account] Waiting for previous operations!', 'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Add Account] Waiting for server to respond!', div_name, viewer_id, 'update', 0, 0)
        send_data = {'token':token, 'purpose':'add_account', 'acc_id': acc_id, 'identifier': identifier}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Add Account] server connection error", 'severe_info', viewer_id, 'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Add Account] Account Added", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                active_viewers[viewer_id]['additional_data'] = additional_data
                render_account_manage_table(viewer_id, additional_data['self_ids'])
            elif response_dict['status_code'] < 0:
                force_send_flask_data(f"[DENIED] [Add Account] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] [Add Account] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                render_account_manage_table(viewer_id, additional_data['self_ids'])
        else:
            force_send_flask_data(f"[ERROR] [Add Account] Something went wrong", 'severe_info', viewer_id, 'new_div', 0, 3)


    elif form['purpose'] == 'add_vm':
        vm_uuid = form['vm_uuid']
        check_and_fix_repeated_mac_addresses()
        if vm_uuid not in vms_to_use:
            vms_to_use.append(vm_uuid)
            open(f'{data_location}/adfly_vm_manager', 'w').write(str({'vms_to_use': vms_to_use}))
        render_vms_manage_tables(viewer_id)


    elif form['purpose'] == 'remove_vm':
        vm_uuid = form['vm_uuid']
        write_vms_to_use()
        if vm_uuid in vms_to_use:
            vms_to_use.remove(vm_uuid)
            open(f'{data_location}/adfly_vm_manager', 'w').write(str({'vms_to_use': vms_to_use}))
        render_vms_manage_tables(viewer_id)


    elif form['purpose'] == 'vms_metric_update':
        global per_vm_memory, max_vm_count, max_memory_percent, rtc_start, rtc_stop
        per_vm_memory = int(form['per_vm_memory'])
        max_vm_count = int(form['max_vm_count'])
        if 0 <= int(form['max_memory_percent']) <= default_max_memory_percent:
            max_memory_percent = int(form['max_memory_percent'])
        else:
            force_send_flask_data(f"[ERROR] [Max memory] Invalid Range. Allowed range: 0-{default_max_memory_percent}", 'severe_info', viewer_id, 'new_div', 0, 3)
        time_format_correct = False
        if 0 <= int(form['bot_start_time_hour']) <= 23:
            bot_start_time_hour = form['bot_start_time_hour']
            if len(bot_start_time_hour) == 1:
                bot_start_time_hour = '0' + bot_start_time_hour
            if 0 <= int(form['bot_start_time_minute']) <= 59:
                bot_start_time_minute = form['bot_start_time_minute']
                if len(bot_start_time_minute) == 1:
                    bot_start_time_minute = '0'+bot_start_time_minute
                rtc_start = [bot_start_time_hour, bot_start_time_minute]
                if 0 <= int(form['bot_stop_time_hour']) <= 23:
                    bot_stop_time_hour = form['bot_stop_time_hour']
                    if len(bot_stop_time_hour) == 1:
                        bot_stop_time_hour = '0'+bot_stop_time_hour
                    if 0 <= int(form['bot_stop_time_minute']) <= 59:
                        bot_stop_time_minute = form['bot_stop_time_minute']
                        if len(bot_stop_time_minute) == 1:
                            bot_stop_time_minute = '0'+bot_stop_time_minute
                        rtc_stop = [bot_stop_time_hour, bot_stop_time_minute]
                        time_format_correct = True
        if not time_format_correct:
            force_send_flask_data(f"[ERROR] [Bot Time Set] Time format wrong. Allowed range: 00:00 - 23:59", 'severe_info', viewer_id, 'new_div', 0, 3)
        open(f'{data_location}/adfly_vm_metrics', 'w').write(str({'per_vm_memory': per_vm_memory, 'max_vm_count': max_vm_count, 'max_memory_percent': max_memory_percent, 'rtc_start': rtc_start, 'rtc_stop': rtc_stop}))
        render_bot_metrics_table(viewer_id)


    elif form['purpose'] == 'turn_on_vm':
        vm_uuid = form['vm_uuid']
        start_vm(vm_uuid)


    elif form['purpose'] == 'turn_off_vm':
        vm_uuid = form['vm_uuid']
        queue_vm_stop(vm_uuid, 0)


def force_send_flask_data(new_data: str, expected_div_name: str, viewer_id: str, method:str, user_delay:int, duration:int, actual_delay:int=0):
    try:
        if viewer_id not in turbo_app.clients:
            return
        if user_delay:
            Thread(target=force_send_flask_data, args=(new_data, expected_div_name, viewer_id, method, 0, duration, user_delay)).start()
            return
        if actual_delay:
            sleep(actual_delay)
            force_send_flask_data(new_data, expected_div_name, viewer_id, method, 0, duration)
            return
        if method == 'new_div':
            while True:
                div_counter = generate_random_string(5,10)
                new_div_name = f"{expected_div_name}_{div_counter}"
                if new_div_name not in active_viewers[viewer_id]['html_data']:
                    force_send_flask_data(f"""<div id='{new_div_name}'></div><div id='{expected_div_name}_create'></div>""", f'{expected_div_name}_create', viewer_id, 'replace', 0, 0)
                    active_viewers[viewer_id]['html_data'][new_div_name] = ''
                    force_send_flask_data(new_data, new_div_name, viewer_id, 'update', user_delay, duration)
                    break
                elif not active_viewers[viewer_id]['html_data'][new_div_name]:
                    force_send_flask_data(new_data, new_div_name, viewer_id, 'update', user_delay, duration)
                    break
            return new_div_name
        elif method == 'replace':
            while viewer_id in turbo_app.clients:
                try:
                    if active_viewers[viewer_id]['can_receive_flask_data']:
                        active_viewers[viewer_id]['can_receive_flask_data'] = False
                        turbo_app.push(turbo_app.replace(new_data, expected_div_name), to=viewer_id)
                        active_viewers[viewer_id]['can_receive_flask_data'] = True
                        break
                    else:
                        sleep(0.1)
                except:
                    sleep(0.1)
        elif method == 'remove':
            while viewer_id in turbo_app.clients:
                try:
                    if active_viewers[viewer_id]['can_receive_flask_data']:
                        active_viewers[viewer_id]['can_receive_flask_data'] = False
                        turbo_app.push(turbo_app.remove(expected_div_name), to=viewer_id)
                        active_viewers[viewer_id]['can_receive_flask_data'] = True
                        del active_viewers[viewer_id]['html_data'][expected_div_name]
                        break
                    else:
                        sleep(0.1)
                except:
                    sleep(0.1)
        elif method == 'update':
            if expected_div_name not in active_viewers[viewer_id]['html_data'] or active_viewers[viewer_id]['html_data'][expected_div_name] != new_data:
                while viewer_id in turbo_app.clients:
                    try:
                        if active_viewers[viewer_id]['can_receive_flask_data']:
                            active_viewers[viewer_id]['can_receive_flask_data'] = False
                            turbo_app.push(turbo_app.update(new_data, expected_div_name), to=viewer_id)
                            active_viewers[viewer_id]['can_receive_flask_data'] = True
                            active_viewers[viewer_id]['html_data'][expected_div_name] = new_data
                            break
                        else:
                            sleep(0.1)
                    except:
                        sleep(0.1)
                if duration:
                    user_delay = duration
                    Thread(target=force_send_flask_data, args=('', expected_div_name, viewer_id, 'remove', user_delay, 0)).start()
    except:
        pass


def __fetch_image_from_global_host(img_name):
    try:
        if img_name in windows_img_files:
            windows_img_files[img_name]['verified'] = None
            version = windows_img_files[img_name]['version']
        else:
            windows_img_files[img_name]={'verified': None, 'version': 0}
            version = 0
        verify_global_host_site()
        response = get(f"{global_host_page}/img_files?img_name={img_name}&version={version}").content
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['img_name'] == img_name:
                if response['version'] != version:
                    windows_img_files[img_name] = {'data': response['data'], 'img_size': response['size'],'version': response['version'], 'verified':True}
                else:
                    windows_img_files[img_name]['verified'] = True
        else:
            _ = 1/0
    except:
        sleep(1)
        __fetch_py_file_from_global_host(img_name)


def __fetch_py_file_from_global_host(file_code):
    try:
        if file_code in py_files:
            py_files[file_code]['verified'] = None
            version = py_files[file_code]['version']
        else:
            py_files[file_code]={'verified': None, 'version': 0}
            version = 0
        verify_global_host_site()
        response = get(f"{global_host_page}/py_files?file_code={file_code}&version={version}").content
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['file_code'] == str(file_code):
                if response['version'] != version:
                    py_files[file_code] = {'data':response['data'], 'verified':True}
                else:
                    py_files[file_code]['verified'] = True
        else:
            _ = 1/0
    except:
        sleep(1)
        __fetch_py_file_from_global_host(file_code)


def invalidate_all_images(interval):
    while True:
        sleep(interval)
        for img_name in windows_img_files:
            windows_img_files[img_name]['verified'] = False


def invalidate_all_py_files(interval):
    while True:
        sleep(interval)
        for file_code in windows_img_files:
            py_files[file_code]['verified'] = False


def vm_connection_manager():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', LOCAL_CONNECTION_PORT))
    sock.listen()

    def acceptor():
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        request_data = __receive_from_connection(connection)
        if request_data[0] == 123 and request_data[-1] == 125:
            request_data = eval(request_data)
        else:
            __try_closing_connection(connection)
            return
        purpose = request_data['purpose']

        if purpose == 'ping':
            data_to_be_sent = {'ping': 'ping'}
            __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'py_file_request':
            file_code = request_data['file_code']
            if file_code not in py_files or not py_files[file_code]['verified'] and not py_files[file_code]['verified'] is not None:
               Thread(target=__fetch_py_file_from_global_host, args=(file_code,)).start()
               sleep(0.5)
            while py_files[file_code]['verified'] is None:
                sleep(0.5)
            data_to_be_sent = {'file_code': file_code, 'py_file_data': py_files[file_code]['data']}
            __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'image_request':
            img_name = request_data['image_name']
            client_image_version = request_data['version']
            if img_name not in windows_img_files or not windows_img_files[img_name]['version'] and windows_img_files[img_name]['version'] is not None:
               Thread(target=__fetch_image_from_global_host, args=(img_name,)).start()
               sleep(0.5)
            while windows_img_files[img_name]['verified'] is None:
                sleep(0.5)
            if windows_img_files[img_name]['version'] == client_image_version:
                data_to_be_sent = {'image_name': str(img_name)}
            else:
                data_to_be_sent = {'image_name': str(img_name), 'image_data': windows_img_files[img_name]['data'], 'image_size': windows_img_files[img_name]['img_size'], 'version': windows_img_files[img_name]['version']}
            __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'stat_connection_establish':
            mac_address = request_data['mac_address']
            vm_stat_connections[mac_address] = connection

        else:
            __try_closing_connection(connection)

    for _ in range(10):
        Thread(target=acceptor).start()


def update_vm_responses():
    global public_vm_data, host_cpu_percent, host_ram_percent

    def receive_data(mac_address):
        try:
            data_to_send = {'purpose': 'stat'}
            __send_to_connection(vm_stat_connections[mac_address], str(data_to_send).encode())
            data = __receive_from_connection(vm_stat_connections[mac_address])
            if data and data[0] == 123 and data[-1] == 125:
                info = eval(data)
                current_vm_response_data[mac_address] = info
        except:
            __try_closing_connection(vm_stat_connections[mac_address])
            try:
                del vm_stat_connections[mac_address]
            except:
                pass

    def ping_vms(mac_address):
        try:
            data_to_send = {'purpose': 'ping'}
            __send_to_connection(vm_stat_connections[mac_address], str(data_to_send).encode())
        except:
            __try_closing_connection(vm_stat_connections[mac_address])
            try:
                del vm_stat_connections[mac_address]
            except:
                pass

    counter = 0
    while True:
        if turbo_app.clients:
            counter = 0
            current_vm_response_data = {}
            try:
                targets = sorted(vm_stat_connections)
                for mac_address in targets:
                    Thread(target=receive_data, args=(mac_address,)).start()
                last_data_sent = time()
                sleep(1)
                while time() - last_data_sent < 5 and len(current_vm_response_data) < len(targets):
                    sleep(0.1)
                return_all_vms()
                for mac_address in current_vm_response_data:
                    if mac_address in vm_to_mac_address.values():
                        for vm_name in vm_to_mac_address:
                            mac_address0 = vm_to_mac_address[vm_name]
                            if mac_address == mac_address0:
                                current_vm_response_data[mac_address]['vm_name'] = vm_name
                                break
                    else:
                        current_vm_response_data[mac_address]['vm_name'] = '--'
                public_vm_data = current_vm_response_data
                host_cpu_percent = cpu(percpu=False)
                host_ram_percent = virtual_memory()[2]
            except:
                pass
        else:
            sleep(0.1)
            counter += 0.1
            if counter >= 5:
                counter = 0
                targets = sorted(vm_stat_connections)
                for mac_address in targets:
                    Thread(target=ping_vms, args=(mac_address,)).start()


def render_account_manage_table(viewer_id, self_ids):
    account_manage_purpose_list = active_viewers[viewer_id]['account_manage_purpose_list']
    for purpose in account_manage_purpose_list:
        invalidate_csrf_token(purpose, viewer_id)
    account_manage_purpose_list = []
    if self_ids:
        account_manage_tbody = ""
        for account_id in self_ids:
            purpose = f'remove_account-{generate_random_string(20,30)}'
            account_manage_purpose_list.append(purpose)
            button_data = f"""<form id='base_form' method='post' action='/action/'>
            <div id='{purpose}_csrf_token'></div>
            <input type=hidden name='purpose' value='{purpose}'>
            <input type=hidden name='acc_id' value={account_id}>
            <button type=submit>Remove</button>
            </form>"""
            identifier = self_ids[account_id]
            if len(identifier) > 30:
                _, identifier = identifier, ''
                while len(_) > 30:
                    identifier += _[0:30] + '</br>'
                    _ = _[30::]
                identifier += _
            account_manage_tbody += f"<tr><td class='with_borders'>{account_id}</td><td class='with_borders'>{identifier}</td><td class='with_borders'>{button_data}</td></tr>"
        force_send_flask_data(public_templates['account_manage_remove_table'].replace('REPLACE_TBODY', account_manage_tbody), 'account_manage_remove_table', viewer_id, 'update', 0, 0)
        for purpose in account_manage_purpose_list:
            send_new_csrf_token(purpose, viewer_id)
        active_viewers[viewer_id]['account_manage_purpose_list'] = account_manage_purpose_list
    else:
        account_manage_tbody = "<tr><td colspan=2>None</td></tr>"
        force_send_flask_data(public_templates['account_manage_remove_table'].replace('REPLACE_TBODY', account_manage_tbody), 'account_manage_remove_table', viewer_id, 'update', 0, 0)


def render_vms_manage_tables(viewer_id):
    global all_vms, vms_to_use
    vms_manage_purpose_list = active_viewers[viewer_id]['vms_manage_purpose_list']
    for purpose in vms_manage_purpose_list:
        invalidate_csrf_token(purpose, viewer_id)
    write_vms_to_use()
    vms_to_skip = list(set(all_vms) - set(vms_to_use))
    vms_manage_purpose_list = []
    if vms_to_use:
        vms_remove_tbody = ""
        for vm_uuid in vms_to_use:
            vm_name = get_vm_info(vm_uuid, 'name')
            purpose = f'remove_vm-{generate_random_string(20, 30)}'
            vms_manage_purpose_list.append(purpose)
            button_data = f"""<form id='base_form' method='post' action='/action/'>
                        <div id='{purpose}_csrf_token'></div>
                        <input type=hidden name='purpose' value='{purpose}'>
                        <input type=hidden name='vm_name' value='{vm_name}'>
                        <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                        <button type=submit>Remove</button>
                        </form>"""
            vms_remove_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
    else:
        vms_remove_tbody = "<tr><td colspan=2>None</td></tr>"
    if vms_to_skip:
        vms_add_tbody = ""
        for vm_uuid in vms_to_skip:
            vm_name = get_vm_info(vm_uuid, 'name')
            purpose = f'add_vm-{generate_random_string(20, 30)}'
            vms_manage_purpose_list.append(purpose)
            button_data = f"""<form id='base_form' method='post' action='/action/'>
                                <div id='{purpose}_csrf_token'></div>
                                <input type=hidden name='purpose' value='{purpose}'>
                                <input type=hidden name='vm_name' value='{vm_name}'>
                                <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                                <button type=submit>Add</button>
                                </form>"""
            vms_add_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
    else:
        vms_add_tbody = "<tr><td colspan=2>None</td></tr>"
    force_send_flask_data(public_templates['vms_manage_remove_table'].replace('REPLACE_TBODY', vms_remove_tbody), 'vm_manage_remove_table', viewer_id, 'update', 0, 0)
    force_send_flask_data(public_templates['vms_manage_add_table'].replace('REPLACE_TBODY', vms_add_tbody), 'vm_manage_add_table', viewer_id, 'update', 0, 0)
    for purpose in vms_manage_purpose_list:
        send_new_csrf_token(purpose, viewer_id)
    active_viewers[viewer_id]['vms_manage_purpose_list'] = vms_manage_purpose_list


def render_bot_metrics_table(viewer_id):
    global vm_manager_start_vm, per_vm_memory, max_vm_count, max_memory_percent, rtc_start, rtc_stop
    write_bot_metrics_to_file()
    purpose = f'vms_metric_update-{generate_random_string(10,20)}'
    force_send_flask_data(public_templates['vms_metric_table'].replace('REPLACE_PURPOSE', purpose).replace('REPLACE_DEFAULT_PER_VM_MEMORY', str(default_per_vm_memory)).replace('REPLACE_DEFAULT_MAX_MEMORY','70').replace('REPLACE_PER_VM_MEMORY', str(per_vm_memory)).replace('REPLACE_MAX_VM_COUNT', str(max_vm_count)).replace('REPLACE_MAX_MEMORY_PERCENT', str(max_memory_percent)).replace('REPLACE_BOT_START_TIME_HOUR', rtc_start[0]).replace('REPLACE_BOT_START_TIME_MINUTE', rtc_start[1]).replace('REPLACE_BOT_STOP_TIME_HOUR', rtc_stop[0]).replace('REPLACE_BOT_STOP_TIME_MINUTE', rtc_stop[1]), 'vms_metric_table', viewer_id, 'update', 0, 0)
    send_new_csrf_token(purpose, viewer_id)


def render_running_bots_table(viewer_id):
    while viewer_id in active_viewers and viewer_id in turbo_app.clients:
        live_vm_manage_purpose_list = active_viewers[viewer_id]['live_vm_manage_purpose_list']
        for purpose in live_vm_manage_purpose_list:
            invalidate_csrf_token(purpose, viewer_id)
        live_vm_manage_purpose_list = []
        running_vms = return_running_vms()
        stopped_vms = return_stopped_vms()
        turn_off_vm_tbody = "<tr><td colspan=2>None</td></tr>"
        if running_vms:
            turn_off_vm_tbody = ""
            for vm_uuid in running_vms:
                vm_name = get_vm_info(vm_uuid, 'name')
                purpose = f'turn_off_vm-{generate_random_string(20, 30)}'
                live_vm_manage_purpose_list.append(purpose)
                button_data = f"""<form id='base_form' method='post' action='/action/'>
                            <div id='{purpose}_csrf_token'></div>
                            <input type=hidden name='purpose' value='{purpose}'>
                            <input type=hidden name='vm_name' value='{vm_name}'>
                            <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                            <button type=submit>Turn off</button>
                            </form>"""
                turn_off_vm_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
        turn_on_vm_tbody = "<tr><td colspan=2>None</td></tr>"
        if stopped_vms:
            turn_on_vm_tbody = ""
            for vm_uuid in stopped_vms:
                vm_name = get_vm_info(vm_uuid, 'name')
                purpose = f'turn_on_vm-{generate_random_string(20, 30)}'
                live_vm_manage_purpose_list.append(purpose)
                button_data = f"""<form id='base_form' method='post' action='/action/'>
                            <div id='{purpose}_csrf_token'></div>
                            <input type=hidden name='purpose' value='{purpose}'>
                            <input type=hidden name='vm_name' value='{vm_name}'>
                            <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                            <button type=submit>Turn on</button>
                            </form>"""
                turn_on_vm_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
        force_send_flask_data(public_templates['turn_on_vm_table'].replace('REPLACE_TBODY', turn_on_vm_tbody), 'turn_on_vm_table', viewer_id, 'update', 0, 0)
        force_send_flask_data(public_templates['turn_off_vm_table'].replace('REPLACE_TBODY', turn_off_vm_tbody), 'turn_off_vm_table', viewer_id, 'update', 0, 0)
        for purpose in live_vm_manage_purpose_list:
            send_new_csrf_token(purpose, viewer_id)
        active_viewers[viewer_id]['live_vm_manage_purpose_list'] = live_vm_manage_purpose_list
        while viewer_id in active_viewers and viewer_id in turbo_app.clients and running_vms == return_running_vms() and stopped_vms == return_stopped_vms():
            sleep(2)


def public_div_manager(real_cookie, viewer_id):
    for _ in range(100):
        sleep(0.1)
        if viewer_id in turbo_app.clients:
            break
    else:
        return
    default_csrf_tokens = {'account_choice':'', 'base_form': '', 'add_account': ''}
    default_html_data = {'logout':'', 'scripts':'', 'private_div':'', 'public_div':'', 'debug_data':'', 'severe_info':'', 'notification_info':'', 'success_info':'', 'welcome_username':'', 'total_views':''}
    active_viewers[viewer_id] = {'u_name': None,'need_vm_updates': True, 'real_cookie': real_cookie, 'flask_secret_key': flask_secret_key, 'turbo_app': turbo_app, 'html_data':default_html_data, 'csrf_tokens':default_csrf_tokens, 'can_receive_flask_data': True, 'account_manage_purpose_list':[], 'vms_manage_purpose_list':[], 'live_vm_manage_purpose_list':[]}
    Thread(target=remove_viewer, args=(viewer_id,)).start()
    Thread(target=account_div_manager, args=(viewer_id,)).start()
    for message_dict in messages_for_all['severe_info']:
        force_send_flask_data(message_dict['message'], 'severe_info', viewer_id, 'new_div', 0, message_dict['duration'])
    for message_dict in messages_for_all['notification_info']:
        force_send_flask_data(message_dict['message'], 'notification_info', viewer_id, 'new_div', 1, message_dict['duration'])
    for message_dict in messages_for_all['success_info']:
        force_send_flask_data(message_dict['message'], 'success_info', viewer_id, 'new_div', 0, message_dict['duration'])
    force_send_flask_data(public_templates['table_script'], 'scripts', viewer_id, 'new_div', 0, 0)
    while viewer_id in active_viewers and viewer_id in turbo_app.clients:
        if active_viewers[viewer_id]['need_vm_updates']:
            public_div_body = """"""
            if not public_vm_data:
                public_div_body += f'''<tr><td colspan=4 class='with_borders'>None</td></tr>'''
            else:
                for mac_address in sorted(public_vm_data):
                    public_div_body += f'''<tr><td class='with_borders'>{mac_address}</td>'''  # mac address
                    public_div_body += f'''<td class='with_borders'>{public_vm_data[mac_address]['vm_name']}</td>''' # vm name
                    public_div_body += f'''<td class='with_borders'>{public_vm_data[mac_address]['uptime']}</td>'''  # uptime
                    public_div_body += f'''<td class='with_borders'>{public_vm_data[mac_address]['views']}</td>'''  # views
            force_send_flask_data(public_templates['public_div'].replace("REPLACE_TBODY", public_div_body), 'public_div', viewer_id, 'update', 0, 0)
        elif active_viewers['html_data']['public_div'] != '':
            force_send_flask_data('', 'public_div', viewer_id, 'update', 0, 0)
        sleep(1.1)


def account_div_manager(viewer_id, reconnect=False):
    div_name = force_send_flask_data('[WAITING] Waiting for server!', 'notification_info', viewer_id, 'new_div', 0, 0)
    global_host_connection, binding_token = force_connect_global_server()
    data_to_be_sent = {'purpose': 'user_authentication', 'binding_token':binding_token}
    __send_to_connection(global_host_connection, str(data_to_be_sent).encode())
    received_data = __receive_from_connection(global_host_connection)
    if received_data[0] == 123 and received_data[-1] == 125:
        received_data = eval(received_data)
        global_host_send_token = received_data['token']
    else:
        global_host_send_token = ''
    if not global_host_send_token:
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        account_div_manager(viewer_id, reconnect=True)
    active_viewers[viewer_id]['global_host_connection'] = global_host_connection
    active_viewers[viewer_id]['global_host_send_token'] = global_host_send_token
    Thread(target=keep_user_global_host_connection_alive, args=(viewer_id,)).start()
    force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
    force_send_flask_data(public_templates['base_script'], 'scripts', viewer_id, 'new_div', 0, 0)
    force_send_flask_data(public_templates['base_form'], 'private_div', viewer_id, 'update', 0, 0)
    send_new_csrf_token('base_form', viewer_id)
    force_send_flask_data('[SUCCESS] Connected to server!', 'success_info', viewer_id, 'new_div', 0, 3)
    if reconnect:
        return
    while viewer_id in active_viewers:
        if 'additional_data' not in active_viewers[viewer_id]:
            sleep(0.1)
        else:
            break
    else:
        return
    additional_data = active_viewers[viewer_id]['additional_data']
    force_send_flask_data(public_templates['post_login'], 'private_div', viewer_id, 'update', 0, 0)
    force_send_flask_data(public_templates['logout_button'], 'logout', viewer_id, 'update', 0, 0)
    send_new_csrf_token('logout', viewer_id)
    force_send_flask_data(f"Welcome back {additional_data['u_name']}", 'welcome_username', viewer_id, 'update', 0, 0)
    force_send_flask_data(f"Total views: {additional_data['total_views']}", 'total_views', viewer_id, 'update', 0, 0)
    render_account_manage_table(viewer_id, additional_data['self_ids'])
    force_send_flask_data(public_templates['account_manage_add_table'], 'account_manage_add_table', viewer_id, 'update', 0, 0)
    send_new_csrf_token('add_account', viewer_id)
    if additional_data['u_name'] in global_host_auth_data:
        for message_dict in messages_for_host['severe_info']:
            force_send_flask_data(message_dict['message'], 'severe_info', viewer_id, 'new_div', 0, message_dict['duration'])
        for message_dict in messages_for_host['notification_info']:
            force_send_flask_data(message_dict['message'], 'notification_info', viewer_id, 'new_div', 0, message_dict['duration'])
        for message_dict in messages_for_host['success_info']:
            force_send_flask_data(message_dict['message'], 'success_info', viewer_id, 'new_div', 0, message_dict['duration'])
        render_vms_manage_tables(viewer_id)
        render_bot_metrics_table(viewer_id)
        render_running_bots_table(viewer_id)
    else:
        force_send_flask_data("<tr><td class='with_borders' colspan=2><font COLOR=RED>Management tools unavailable because current account is not host account</font></td></tr>", 'vm_manage_remove_table', viewer_id, 'replace', 0, 0)
        force_send_flask_data("", 'vms_metric_table', viewer_id, 'remove', 0, 0)
        force_send_flask_data("", 'running_vms_table', viewer_id, 'remove', 0, 0)


def send_new_csrf_token(purpose, viewer_id):
    csrf_token = generate_random_string(10, 20)
    force_send_flask_data(f'<input type="hidden" name="csrf_token" value="{csrf_token}">', f'{purpose}_csrf_token', viewer_id, 'update', 0, 0)
    active_viewers[viewer_id]['csrf_tokens'][purpose] = csrf_token


def invalidate_csrf_token(purpose, viewer_id):
    csrf_token = ''
    force_send_flask_data(f'<input type="hidden" name="csrf_token" value="{csrf_token}">', f'{purpose}_csrf_token', viewer_id, 'update', 0, 0)
    active_viewers[viewer_id]['csrf_tokens'][purpose] = csrf_token


active_viewers = {}
flask_secret_key = Fernet.generate_key()
turbo_app : Turbo()


def private_flask_operations():
    app = Flask("adfly user private host")
    app.secret_key = flask_secret_key
    app.SESSION_COOKIE_SECURE = True
    csrf_tokens = []
    def manage_csrf_tokens(token):
        csrf_tokens.append(token)
        sleep(60)
        if token in csrf_tokens:
            csrf_tokens.remove(token)

    @app.route('/favicon.ico')
    def private_favicon():
        return redirect('https://avatars.githubusercontent.com/u/101955196')


    @app.route('/', methods=['GET'])
    def private_root_url():
        if request.args.get("reason"):
            reason = request.args.get("reason")
        else:
            reason = ''
        if request.args.get("u_name"):
            u_name = request.args.get("u_name")
        else:
            u_name = ''
        csrf_token = generate_random_string(100,200)
        Thread(target=manage_csrf_tokens, args=(csrf_token,)).start()
        response = make_response(render_template_string(private_templates['base.html'].replace("REPLACE_CSRF_TOKEN", csrf_token).replace("REPLACE_REASON", reason).replace("REPLACE_U_NAME", u_name)))
        return response


    @app.route('/action/', methods=['GET'])
    def private_wrong_path():
        return redirect('/')


    @app.route('/action/', methods=['POST'])
    def private_action():
        form_dict = request.form.to_dict()
        if 'csrf_token' not in form_dict or 'purpose' not in form_dict or 'username' not in form_dict:
            return redirect('/?reason=Invalid Form')
        if form_dict['csrf_token'] not in csrf_tokens:
            return redirect('/?reason=Session Expired')
        csrf_tokens.remove(form_dict['csrf_token'])
        purpose = form_dict['purpose']
        if purpose == 'login':
            username = form_dict['username'].strip().lower()
            password = form_dict['password']
            connection, binding_token = force_connect_global_server()
            data_to_send = {'purpose': 'host_authentication', 'binding_token':binding_token}
            __send_to_connection(connection, str(data_to_send).encode())
            data_to_send = {'purpose': "login", "u_name": username, "password": password, 'network_adapters': [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]}
            __send_to_connection(connection, str(data_to_send).encode())
            response = __receive_from_connection(connection)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    auth_token = response['auth_token']
                    open(f'{data_location}/adfly_local_host_authenticator', 'w').write(str({username: auth_token}))
                    global_host_peering_authenticator()
                    return f"Host is now serving as {username}.</br>Please close this browser tab."
                elif response['status_code'] < 0:
                    return redirect(f"/?reason={response['reason']}")


        elif purpose == 'create_new_account':
            username = form_dict['username'].strip().lower()
            password1 = form_dict['password1']
            password2 = form_dict['password2']
            if not u_name_matches_standard(username):
                return redirect('/?reason=Username Not Allowed!!')
            elif password2 != password1:
                return redirect(f"/?reason=Passwords don't match!!&u_name={username}")
            elif not password_matches_standard(password2):
                return redirect(f"/?reason=Password too weak!!&u_name={username}")
            connection, binding_token = force_connect_global_server()
            data_to_send = {'purpose': 'host_authentication', 'binding_token':binding_token}
            __send_to_connection(connection, str(data_to_send).encode())
            data_to_send = {'purpose': "create_new_account", "u_name":username, "password": password2, 'network_adapters': [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]}
            __send_to_connection(connection, str(data_to_send).encode())
            response = __receive_from_connection(connection)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    auth_token = response['auth_token']
                    open(f'{data_location}/adfly_local_host_authenticator', 'w').write(str({username: auth_token}))
                    global_host_peering_authenticator()
                    return f"Account created successfully. Host is now serving: {username}.</br>Please close this browser tab."
                elif response['status_code'] < 0:
                    return redirect(f"/?reason={response['reason']}")

    app.run(port=PRIVATE_HOST_PORT, debug=False, use_reloader=False, threaded=True)


def public_flask_operations():
    global turbo_app
    app = Flask("adfly user public host")
    app.secret_key = flask_secret_key
    app.SESSION_COOKIE_SECURE = True
    turbo_app = Turbo(app)
    @turbo_app.user_id
    def get_user_id():
        cookie_data = {}
        verified = False
        real_cookie = request.cookies.get('VIEWER_ID')
        fernet = Fernet(flask_secret_key)
        cookie_dict_string = fernet.decrypt(real_cookie.encode())
        if cookie_dict_string[0] == 123 and cookie_dict_string[-1] == 125:
            cookie_data = eval(cookie_dict_string)
            if cookie_data['VIEWER_ID'] not in turbo_app.clients:
                if cookie_data['HTTP_USER_AGENT'] == request.environ['HTTP_USER_AGENT']:
                    if 'HTTP_X_FORWARDED_FOR' in cookie_data and cookie_data['HTTP_X_FORWARDED_FOR'] == request.environ['HTTP_X_FORWARDED_FOR']:
                        verified = True
                    elif 'REMOTE_ADDR' in cookie_data and cookie_data['REMOTE_ADDR'] == request.environ['REMOTE_ADDR']:
                        verified = True
                    else:
                        for key in request.environ:
                            if str(request.environ[key]).count('.') == 4 and cookie_data['IP'] == request.environ[key]:
                                verified = True
        if verified and cookie_data:
            return cookie_data['VIEWER_ID']


    @app.before_first_request
    def first_req():
        Thread(target=update_vm_responses).start()


    @app.route('/favicon.ico')
    def public_favicon():
        return redirect('https://avatars.githubusercontent.com/u/101955196')

    @app.route('/start_time')
    def return_start_time():
        return str(start_time)


    @app.route('/action/', methods=['GET'])
    def public_wrong_path():
        return redirect('/')


    @app.route('/', methods=['GET'])
    def public_root_url():
        while True:
            viewer_id = generate_random_string(10,20)
            if viewer_id not in turbo_app.clients:
                break
        cookie_data = {}
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            cookie_data['HTTP_X_FORWARDED_FOR'] = request.environ['HTTP_X_FORWARDED_FOR']
        if request.environ['REMOTE_ADDR'] != '127.0.0.1':
            cookie_data['REMOTE_ADDR'] = request.environ['REMOTE_ADDR']
        else:
            for key in request.environ:
                if str(request.environ[key]).count('.') == 4:
                    cookie_data['IP'] = request.environ[key]
                    break
        cookie_data['VIEWER_ID'] = viewer_id
        cookie_data['HTTP_USER_AGENT'] = request.environ['HTTP_USER_AGENT']
        fernet = Fernet(flask_secret_key)
        real_cookie = fernet.encrypt(str(cookie_data).encode()).decode()
        response = make_response(render_template_string(public_templates['base.html']))
        response.set_cookie('VIEWER_ID', real_cookie)
        Thread(target=public_div_manager, args=(real_cookie, viewer_id,)).start()
        return response


    @app.route('/action/', methods=['POST'])
    def public_action():
        verified = False
        real_cookie = request.cookies.get('VIEWER_ID')
        fernet = Fernet(flask_secret_key)
        cookie_dict_string = fernet.decrypt(real_cookie.encode())
        if cookie_dict_string[0] == 123 and cookie_dict_string[-1] == 125:
            cookie_data = eval(cookie_dict_string)
            viewer_id = cookie_data['VIEWER_ID']
            if not viewer_id:
                return ''
            if cookie_data['VIEWER_ID'] in turbo_app.clients and real_cookie == active_viewers[viewer_id]['real_cookie']:
                if cookie_data['HTTP_USER_AGENT'] == request.environ['HTTP_USER_AGENT']:
                    if 'HTTP_X_FORWARDED_FOR' in cookie_data and cookie_data['HTTP_X_FORWARDED_FOR'] == request.environ['HTTP_X_FORWARDED_FOR']:
                        verified = True
                    elif 'REMOTE_ADDR' in cookie_data and cookie_data['REMOTE_ADDR'] == request.environ['REMOTE_ADDR']:
                        verified = True
                    else:
                        for key in request.environ:
                            if str(request.environ[key]).count('.') == 4 and cookie_data['IP'] == request.environ[key]:
                                verified = True
            form = request.form.to_dict()
            if 'purpose' not in form:
                return ''
            purpose = form['purpose']
            if 'csrf_token' not in form or active_viewers[viewer_id]['csrf_tokens'][purpose] != form['csrf_token'] or form['csrf_token'] == '':
                return ''
            if verified:
                del form['csrf_token']
                form['purpose'] = form['purpose'].split('-')[0]
                invalidate_csrf_token(purpose, viewer_id)
                if form['purpose'] != 'logout':
                    Thread(target=process_form_action, args=(viewer_id, form,)).start()
                else:
                    for div_name in active_viewers[viewer_id]:
                        if 'script' in div_name:
                            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)

                    force_send_flask_data('Successfully logged out<meta http-equiv = "refresh" content = "1; url = /" />', 'private_div', viewer_id, 'update', 0, 0)
                    Thread(target=remove_viewer, args=(viewer_id,))
        return ''


    @app.route('/ip', methods=['GET'])
    def public_global_ip():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        return ip

    app.run(host='0.0.0.0', port=PUBLIC_HOST_PORT, debug=False, use_reloader=False, threaded=True)


private_templates = {

'base.html':
"""
<script>
table, th, td {
text-align: center;
}
</script>
<FONT COLOR="RED"></br>This webpage allows the user to control all VMs in this PC, do not at any cost let others have access to this page.</br></FONT>
<table>
<tr><td>
<h2>Create New Account</h2>
<form method='post' action='/action/'>
<input type="hidden" name="purpose" value="create_new_account">
<input type="hidden" name="csrf_token" value="REPLACE_CSRF_TOKEN">
Username: <input type="text" name="username" value="REPLACE_U_NAME"></br>
Password: <input type="password" name="password1"></br>
Re-enter Password: <input type="password" name="password2"></br>
</br><button type=submit>Create new Account</button>
</form></td></tr>
<tr><td></td></tr>
<tr><td><h2>OR</h2> </td></tr>
<tr><td></td></tr><tr><td>
<h2>Login</h2>
<form method='post' action='/action/'>
<input type="hidden" name="purpose" value="login">
<input type="hidden" name="csrf_token" value="REPLACE_CSRF_TOKEN">
Username: <input type="text" name="username" value="REPLACE_U_NAME"></br>
Password: <input id='password_entry' type="password" name="password"></br>
</br><button type=submit>Login</button>
</form></td></tr>
</table>
<FONT COLOR="RED"></br>REPLACE_REASON</FONT>
"""
}


public_templates = {

'base.html':
"""
<head>
<script type="module">
import * as Turbo from "https://cdn.skypack.dev/pin/@hotwired/turbo@v7.1.0-RBjb2wnkmosSQVoP27jT/min/@hotwired/turbo.js";
window.web_sock = new WebSocket(`ws${location.protocol.substring(4)}//${location.host}/turbo-stream`);
Turbo.connectStreamSource(window.web_sock);
window.web_sock.addEventListener('close', function() {
window.location.reload();
});
</script>
<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache, must-revalidate">
<meta name="turbo-cache-control" content="no-cache, must-revalidate">
<div id="scripts_create"></div></br>
<div id="private_div">If you are stuck in this page, please refresh</div></br>
<div id="debug_data_create"></div></br>
<FONT COLOR="RED"><div id="severe_info_create"></div></FONT></br>
<FONT COLOR="BLUE"><div id="notification_info_create"></div></FONT></br>
<FONT COLOR="GREEN"><div id="success_info_create"></div></FONT></br>
<div id="public_div"></div></br>
""",
###
'base_form':
"""
<form id='base_form' method='post' action='/action/'>
<div id='base_form_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<input type="hidden" name="purpose" value="base_form">
<input type="radio" name="choice" value='create_new_account'>
<label for="choice">Create New Account</label>
<input type="radio" name="choice" value='login'>
<label for="choice">Login</label>
</br><button type=submit>Submit</button>
</form>
""",
###
'base_script':
"""
<script type="text/javascript">
$(document).on('submit','#base_form',function(e) {
e.preventDefault();
$.ajax({
type:'POST',
url:'/action/',
success:function() {
}
})
});
</script>
""",
###
'create_new_account_form':
"""
<form id='base_form' method='post' action='/action/'>
<div id='create_new_account_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<h2>Create New Account</h2>
<input type="hidden" name="purpose" value="create_new_account">
Username: <input type="text" name="username"></br>
Password: <input type="password" name="password1"></br>
Re-enter Password: <input type="password" name="password2"></br>
</br><button type=submit>Create</button>
</form>
""",
###
'login_form':
"""
<form id='base_form' method='post' action='/action/'>
<div id='login_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<h2>Login</h2>
<input type="hidden" name="purpose" value="login">
Username: <input type="text" name="username"></br>
Password: <input id='password_entry' type="password" name="password"></br>
</br><button type=submit>Login</button>
</form>
""",
###
'logout_button':
f"""
<form id='base_form' method='post' action='/action/'>
<div id='logout_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<input type="hidden" name="purpose" value="logout">
<button type=submit>Logout</button>
</form>
""",
###
'post_login':
f"""
<div id='logout'></div>
<div id='welcome_username'></div>
<div id='total_views'></div>
<table>
<tr><td></br></td></tr>
<tr><th>Manage accounts:</th></tr>
<tr>
<td><div id='account_manage_remove_table'></div></td>
<td><div id='account_manage_add_table'></div></td>
</tr>
<tr><td></br></td></tr>
<tr><th>Manage VMs controlled by bot:</th></tr>
<tr>
<td><div id='vm_manage_remove_table'></div></td>
<td><div id='vm_manage_add_table'></div></td>
</tr>
<tr><td></br></td></tr>
<tr><th>Manage bot metrics:</th></tr>
<tr>
<td colspan=2><div id='vms_metric_table'></div></td>
</tr>
<tr><td></br></td></tr>
<tr><th>Manage running bots:</th></tr>
<tr>
<td><div id='turn_off_vm_table'></div></td>
<td><div id='turn_on_vm_table'></div></td>
</tr>
</table>
""",
###
'table_script':
"""
<style>
.with_borders {
border: 3px solid black;
}
</style>
<style>
td, th {
font-size: 18px;
}
table, th, td {
text-align: center;
}
</style>
""",
###
'account_manage_remove_table':
"""
<table class='with_borders'>
<tr><th class='with_borders'>Referral ID</th><th class='with_borders'>Identifier</th><th class='with_borders'>Remove?</th></tr>
REPLACE_TBODY
</table>
""",
###
'account_manage_add_table':
"""
<form id='base_form' method='post' action='/action/'>
<input type=hidden name='purpose' value='add_account'>
<div id='add_account_csrf_token'></div>
<table class='with_borders'>
<tr>
<th class='with_borders'>Referral ID
<th class='with_borders'>Identifier
<th class='with_borders'>Add?
</tr>
<tr>
<td><input type=number name='acc_id' placeholder='acc_id'>
<td><input type=text name='identifier' placeholder='Keep Notes'>
<td><button type=submit>Add Account</button>
</tr>
</table>
</form>
""",
###
'vms_manage_add_table':
"""
<table class='with_borders'>
<tr><th class='with_borders'>VMs that the bot skips</th><th class='with_borders'>Add control?</th></tr>
REPLACE_TBODY
</table>
""",
###
'vms_manage_remove_table':
"""
<table class='with_borders'>
<tr><th class='with_borders'>VMs that the bot controls</th><th class='with_borders'>Remove control?</th></tr>
REPLACE_TBODY
</table>
""",
###
'vms_metric_table':
"""
<form id="base_borm" method='post' action="/action/">
<table class='with_borders'>
<tr>
<th style="text-align: left">Per VM memory: </th>
<td style="text-align: left"><input style="width: 5em" type="number" name="per_vm_memory" value=REPLACE_PER_VM_MEMORY>MB</td>
<td style="text-align: left"><FONT color="blue">Change this only if you changed the memory values in VirtualBox settings! Default:REPLACE_DEFAULT_PER_VM_MEMORY</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Max VM count: </th>
<td style="text-align: left"><input style="width: 4em" type="number" name="max_vm_count" value=REPLACE_MAX_VM_COUNT></td>
<td style="text-align: left"><FONT color="blue">Max number of VMs you want to run at a time(Only if possible)</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Max Memory Percent:</th>
<td style="text-align: left"><input style="width: 4em" type="number" name="max_memory_percent" max=REPLACE_DEFAULT_MAX_MEMORY min=0 value=REPLACE_MAX_MEMORY_PERCENT></td>
<td style="text-align: left"><FONT color="blue">RAM % your system should reach before the bot starts shutting VMs down. Default:REPLACE_DEFAULT_MAX_MEMORY</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Bot Start Time: </th>
<td style="text-align: left"><input style="width: 3em" type="number" name="bot_start_time_hour" max=23 min=0 value=REPLACE_BOT_START_TIME_HOUR>h
<input  style="width: 3em" type="number" name="bot_start_time_minute" max=59 min=0 value=REPLACE_BOT_START_TIME_MINUTE>m</td>
<td style="text-align: left"><FONT color="blue">When should VM manager start VMs.</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Bot Stop Time:</th>
<td style="text-align: left"><input style="width: 3em" type="number" name="bot_stop_time_hour" max=23 min=0 value=REPLACE_BOT_STOP_TIME_HOUR>h 
<input style="width: 3em" type="number" name="bot_stop_time_minute" max=59 min=0 value=REPLACE_BOT_STOP_TIME_MINUTE>m</td>
<td style="text-align: left"><FONT color="blue">When should VM manager stop all VMs.</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<div id='REPLACE_PURPOSE_csrf_token'></div>
<input type=hidden name='purpose' value='REPLACE_PURPOSE'>
<td colspan="2"><button type=submit>Update</button></td>
</tr>
</table>
</form>
""",
###
'turn_on_vm_table':
"""
<table class='with_borders'>
<tr><th class='with_borders'>VMs currently off</th><th class='with_borders'>Turn on?</th></tr>
REPLACE_TBODY
</table>
""",
###
'turn_off_vm_table':
"""
<table class='with_borders'>
<tr><th class='with_borders'>VMs currently on</th><th class='with_borders'>Turn off?</th></tr>
REPLACE_TBODY
</table>
""",
###
'public_div':
"""
<table class='with_borders'>
<tr><th class='with_borders'>Mac Address</th><th class='with_borders'>VM Name</th><th class='with_borders'>Uptime</th><th class='with_borders'>Views</th></tr>
REPLACE_TBODY
</table>
"""
}

global_host_peering_authenticator()
Thread(target=private_flask_operations).start()
Thread(target=public_flask_operations).start()
Thread(target=vm_connection_manager).start()
Thread(target=vm_manager).start()
Thread(target=invalidate_all_py_files, args=(60*60,)).start()
Thread(target=invalidate_all_images, args=(60*60*24,)).start()
sleep(2)
Thread(target=reprint_screen).start()
