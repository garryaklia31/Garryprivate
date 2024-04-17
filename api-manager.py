import paramiko
import os
import json
import pysftp

def get_servers():
    with open('servers.json') as f:
        data = json.load(f)
    return data['servers']

def save_servers(servers):
    with open('servers.json', 'w') as f:
        json.dump({"servers": servers}, f, indent=4)

def get_api_keys():
    with open('keys.json') as f:
        keys = json.load(f)
    return keys

def save_api_keys(keys):
    with open('keys.json', 'w') as f:
        json.dump(keys, f, indent=4)

def get_methods():
    with open('methods.json') as f:
        methods = json.load(f)
    return methods

def save_methods(methods):
    with open('methods.json', 'w') as f:
        json.dump(methods, f, indent=4)

def ssh_login(server_info):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=server_info['hostname'], port=server_info['port'], username=server_info['username'], password=server_info['password'], allow_agent=False, look_for_keys=False)
        return ssh
    except Exception as e:
        print(f"Failed to connect to {server_info['hostname']}: {e}")
        return None

def add_server():
    hostname = input("Enter server hostname: ")
    port = int(input("Enter server port: "))
    username = input("Enter server username: ")
    password = input("Enter server password: ")
    servers = get_servers()
    servers.append({
        "hostname": hostname,
        "port": port,
        "username": username,
        "password": password
    })
    save_servers(servers)
    print("Server added successfully.")

def remove_server():
    servers = get_servers()
    for i, server in enumerate(servers):
        print(f"{i+1}. {server['hostname']}")
    choice = int(input("Enter the number of the server to remove: ")) - 1
    if 0 <= choice < len(servers):
        removed_server = servers.pop(choice)
        save_servers(servers)
        print(f"Server {removed_server['hostname']} removed successfully.")
    else:
        print("Invalid selection.")

def list_servers():
    servers = get_servers()
    print("List of Servers:")
    for server in servers:
        print(f"- {server['hostname']}")

def upload_file():
    servers = get_servers()
    for i, server in enumerate(servers):
        print(f"{i+1}. {server['hostname']}")
    server_choice = int(input("Choose server to upload file: ")) - 1

    if 0 <= server_choice < len(servers):
        file_path = input("Enter the path of the file to upload: ")
        remote_path = input("Enter the remote path to upload to: ")

        with pysftp.Connection(servers[server_choice]['hostname'], username=servers[server_choice]['username'], password=servers[server_choice]['password'], port=servers[server_choice]['port']) as sftp:
            sftp.chdir(remote_path)
            sftp.put(file_path)
            print("File uploaded successfully.")

    else:
        print("Invalid server selection.")

def delete_file():
    servers = get_servers()
    for i, server in enumerate(servers):
        print(f"{i+1}. {server['hostname']}")
    server_choice = int(input("Choose server to delete file from: ")) - 1

    if 0 <= server_choice < len(servers):
        remote_path = input("Enter the remote path of the file to delete: ")

        ssh = ssh_login(servers[server_choice])
        if ssh:
            try:
                stdin, stdout, stderr = ssh.exec_command(f"rm {remote_path}")
                print("File deleted successfully.")
            except Exception as e:
                print(f"Failed to delete file: {e}")
            ssh.close()
    else:
        print("Invalid server selection.")

def add_api_key():
    keys = get_api_keys()
    new_key = input("Enter the new API key: ")
    keys.append(new_key)
    save_api_keys(keys)
    print("API key added successfully.")

def remove_api_key():
    keys = get_api_keys()
    print("Current API Keys:")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key}")
    choice = int(input("Enter the number of the key to remove: ")) - 1
    if 0 <= choice < len(keys):
        removed_key = keys.pop(choice)
        save_api_keys(keys)
        print(f"API key '{removed_key}' removed successfully.")
    else:
        print("Invalid selection.")

def add_method():
    methods = get_methods()
    name = input("Enter method name: ")
    command = input("Enter method command: ")
    methods[name] = command
    save_methods(methods)
    print("Method added successfully.")

def remove_method():
    methods = get_methods()
    print("Current Methods:")
    for name, command in methods.items():
        print(f"{name}: {command}")
    name = input("Enter the name of the method to remove: ")
    if name in methods:
        del methods[name]
        save_methods(methods)
        print(f"Method '{name}' removed successfully.")
    else:
        print("Invalid method name.")

def main_menu():
    print("API MANAGER BY KYOURA\n")
    print("01. ADD FILE TO SERVER")
    print("02. REMOVE FILE FROM SERVER")
    print("03. LIST SERVER")
    print("04. ADD SERVER")
    print("05. REMOVE SERVER")
    print("06. ADD KEY FOR API")
    print("07. REMOVE KEY FOR API")
    print("08. ADD METHOD")
    print("09. REMOVE METHOD")

    choice = input("\nPilih menu: ")

    if choice == '01':
        upload_file()
    elif choice == '02':
        delete_file()
    elif choice == '03':
        list_servers()
    elif choice == '04':
        add_server()
    elif choice == '05':
        remove_server()
    elif choice == '06':
        add_api_key()
    elif choice == '07':
        remove_api_key()
    elif choice == '08':
        add_method()
    elif choice == '09':
        remove_method()
    else:
        print("Pilihan tidak valid.")

if __name__ == '__main__':
    main_menu()
