import os
import paramiko # type: ignore
from scp import SCPClient # type: ignore
import logging


sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def establishConnection(IP, userName, password):
    try:
        sshClient.connect(hostname=IP, port=22, username=userName, password=password) 
        return sshClient
    except Exception as e:
        print(f"Failed to establish SSH connection: {e}")
        return None

# to log if something goes wrong while we run the app
logging.basicConfig(
    filename='app.log',  
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# to show the progression of how much a file has been downloaded on the logs
def progress(filename, size, sent):
    print(f"Transferring {filename}: {float(sent)/ float(size)*100:.2f}%")

def downloadFolder(remote_path, local_path):
    try:
        os.makedirs(local_path, exist_ok=True)
        
        scp = SCPClient(sshClient.get_transport(), progress=progress) # type: ignore
        stdin, stdout, stderr = sshClient.exec_command(f"test -d {remote_path} && echo 'Directory' || echo 'Not a directory'")
        result = stdout.read().decode().strip()
        
        if result != "Directory":
            print(f"Error: {remote_path} is not a directory or doesn't exist on the remote server.")
            return False
        
        # Getting the list of files in remote directory
        stdin, stdout, stderr = sshClient.exec_command(f"find {remote_path} -type f | sort")
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

def closeSSHConnection():
    if sshClient.get_transport() and sshClient.get_transport().is_active():
        sshClient.close()
