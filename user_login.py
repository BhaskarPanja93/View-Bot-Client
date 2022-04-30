import socket
from os import system as system_caller
from platform import system

BUFFER_SIZE = 1024*100
host_ip, host_port = '', ''
full_file_path = __file__.replace('\\','/')
current_file_name = full_file_path.split('/')[-1].replace('.py','')

def force_connect_server(type_of_connection):
    global host_ip, host_port
    if type_of_connection == 'tcp':
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            connection.connect((host_ip, host_port))
            break
        except:
            from requests import get
            text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
            link_dict = eval(text)
            host_ip, host_port = link_dict['adfly_user_tcp_connection'].split(':')
            host_port = int(host_port)
    return connection


def __send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(str(data_byte_length).encode())
    if connection.recv(1) == b'-':
        connection.send(data_bytes)
    if connection.recv(1) == b'-':
        return


def __receive_from_connection(connection):
    length = int(connection.recv(BUFFER_SIZE))
    connection.send(b'-')
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(BUFFER_SIZE)
    connection.send(b'-')
    return data_bytes


def clear_screen():
    if system() == 'Windows':
        system_caller('cls')
    else:
        system_caller('clear')


self_update_connection = force_connect_server('tcp')
__send_to_connection(self_update_connection, b'8')
user_login_data = __receive_from_connection(self_update_connection)
if open(full_file_path, 'rb').read() != user_login_data:
    with open(full_file_path, 'wb') as user_login_file:
        user_login_file.write(user_login_data)
        print('Successfully updated from server.')
        from importlib import import_module
        import_module(current_file_name)


login_connection = force_connect_server('tcp')
__send_to_connection(login_connection, b'9')
print("""Enter 0 to Login
Enter 1 to Create a new account 
""")
while True:
    choice = input('>> ')
    if choice in ['0','1']:
        clear_screen()
        break

u_name = None
login_possible = False
signup_possible = False
login_success = False


def password_matches_standard(password: str):
    has_1_number = False
    has_1_upper = False
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


def post_login_function():
    clear_screen()
    print(f"Login successful, Welcome back {u_name}")
    while True:
        print("""
            Enter 1 to add new adfly ids to your account
            Enter 2 to choose adfly ids to remove from your account
            Enter 3 to change your password
            """)
        while True:
            action = input('>> ').strip()
            if action in ['1','2','3']:
                clear_screen()
                break
        if action == '1':
            while True:
                __send_to_connection(login_connection, b'3')
                old_ids = __receive_from_connection(login_connection).decode()
                print(f"Your previously added ID are: {old_ids.replace(' ',', ')}")
                _id = input("Enter a single ID you want to add to your account or type x to return to previous page: ").strip()
                if _id.lower() == 'x':
                    __send_to_connection(login_connection, b'x')
                    clear_screen()
                    break
                else:
                    __send_to_connection(login_connection, _id.encode())
                    response = __receive_from_connection(login_connection).decode()
                    if response == '0':
                        clear_screen()
                        print(f"ID {_id} successfully added")
                        print()
                    elif response == '-1':
                        clear_screen()
                        print(f"ID {_id} already present. ")
                        print()
                    elif response == '-2':
                        clear_screen()
                        print(f"ID {_id} seems wrong. Please recheck ")
                        print()
        elif action == '2':
            while True:
                __send_to_connection(login_connection, b'4')
                response = __receive_from_connection(login_connection).decode()
                if response == '-1':
                    print('You dont have any previously added account.')
                    print()
                    break
                old_ids = __receive_from_connection(login_connection).decode()
                print(f"Your previously added ID are: {old_ids.replace(' ', ', ')}")
                _id = input("Enter a single ID you want to add to your account or type x to return to previous page: ").strip()
                if _id.lower() == 'x':
                    __send_to_connection(login_connection, b'x')
                    clear_screen()
                    break
                else:
                    __send_to_connection(login_connection, _id.encode())
                    response = __receive_from_connection(login_connection).decode()
                    if response == '0':
                        clear_screen()
                        print(f"ID {_id} successfully removed")
                        print()
                    elif response == '-1':
                        clear_screen()
                        print(f"ID {_id} not present. ")
                        print()
                    elif response == '-2':
                        clear_screen()
                        print(f"ID {_id} seems wrong. Please recheck ")
                        print()
        elif action == '3':
            __send_to_connection(login_connection, b'5')
            response = __receive_from_connection(login_connection).decode()
            if response == '0':
                while True:
                    password = input(f'Create password for {u_name}: ').strip()
                    if not password_matches_standard(password):
                        clear_screen()
                        print("Try a stronger password with atleast 1 uppercase, 1 lowercase, 1 digit and 8 characters")
                        print()
                        continue
                    temp = input('Re enter your password: ').strip()
                    if temp == password:
                        break
                    else:
                        clear_screen()
                        print("Passwords dont match.")
                        print()
                __send_to_connection(login_connection, password.encode())
                response = __receive_from_connection(login_connection).decode()
            if response == '0':
                clear_screen()
                print('Password changed successfully')
                print()
            elif response == '-1':
                clear_screen()
                print('Password doesnt meet our standards. Password change failed ')
                print()

while True:
    if choice == '0':
        u_name = input('Enter your previous username: ').strip().lower()
        __send_to_connection(login_connection, choice.encode())
        __send_to_connection(login_connection, u_name.encode())
        response = __receive_from_connection(login_connection).decode()
        if response == '0':
            login_possible = True
            while not login_success:
                password = input(f'Enter password for {u_name}: ').strip()
                __send_to_connection(login_connection, b'2')
                __send_to_connection(login_connection, password.encode())
                response = __receive_from_connection(login_connection).decode()
                if response == '0' and login_possible:
                    login_success = True
                    post_login_function()
                else:
                    clear_screen()
                    print('Wrong password. Try again ')
                    print()
        else:
            clear_screen()
            print("Username not in database. Try again ")
            print()
    elif choice == '1':
        u_name = input('Enter new username: ').strip().lower()
        __send_to_connection(login_connection, choice.encode())
        __send_to_connection(login_connection, u_name.encode())
        response = __receive_from_connection(login_connection).decode()
        if response == '0':
            signup_possible = True
            while True:
                password = input(f'Create password for {u_name}: ').strip()
                if not password_matches_standard(password):
                    clear_screen()
                    print("Try a stronger password with atleast 1 uppercase, 1 lowercase, 1 digit and 8 characters")
                    print()
                    continue
                temp = input('Re enter your password: ').strip()
                if temp == password:
                    break
                else:
                    clear_screen()
                    print("Passwords dont match.")
                    print()
            __send_to_connection(login_connection, b'2')
            __send_to_connection(login_connection, password.encode())
            response = __receive_from_connection(login_connection).decode()
            if response == '0' and signup_possible:
                login_success = True
                post_login_function()
        elif response == '-1':
            clear_screen()
            print("Username already in use. Try a different Username ")
            print()
