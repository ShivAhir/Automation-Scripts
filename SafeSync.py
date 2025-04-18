import os
import paramiko # type: ignore
import re
from scp import SCPClient # type: ignore

userName = 'mvx'
IP = '172.16.177.79'
sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshClient.connect(hostname=IP, port=22, username=userName, password='mvx') 
ansiEscape = re.compile(r'\x1b\[.*?m')

def progress(filename, size, sent):
    print(f"Transferring {filename}: {float(sent)/ float(size)*100:.2f}%")

def download_folder(ssh_client, remote_path, local_path):
    try:
        os.makedirs(local_path, exist_ok=True)
        
        scp = SCPClient(ssh_client.get_transport(), progress=progress) # type: ignore
        stdin, stdout, stderr = ssh_client.exec_command(f"test -d {remote_path} && echo 'Directory' || echo 'Not a directory'")
        result = stdout.read().decode().strip()
        
        if result != "Directory":
            print(f"Error: {remote_path} is not a directory or doesn't exist on the remote server.")
            return False
        
        # Getting the list of files in remote directory
        stdin, stdout, stderr = ssh_client.exec_command(f"find {remote_path} -type f | sort")
        files = stdout.read().decode().strip().split('\n')
        
        # Downloading each file in the directory
        print(f"Downloading {len(files)} files from {remote_path}...")
        for remote_file in files:
            if not remote_file:
                continue    
            rel_path = os.path.relpath(remote_file, remote_path)
            local_file_path = os.path.join(local_path, rel_path)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            scp.get(remote_file, local_file_path)
        scp.close()
        print(f"\nSuccessfully downloaded folder from {remote_path} to {local_path}")
        return True
    except Exception as e:
        print(f"Error downloading folder: {str(e)}")
        return False

def main():
    remote_paths = [
        '/udata/etc/network',
        '/udata/etc/mvx',
    ]
    new_local_path = os.path.join(os.getcwd(), "Backup")
    os.makedirs(new_local_path, exist_ok=True)

    for remote_path in remote_paths:
        download_folder(sshClient, remote_path, new_local_path)
    sshClient.close()

if __name__ == "__main__":
    main()
