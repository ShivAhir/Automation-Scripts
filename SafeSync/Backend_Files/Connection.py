import paramiko # type: ignore

sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def establishConnection(IP, userName, password):
    try:
        sshClient.connect(hostname=IP, port=22, username=userName, password=password) 
        return sshClient
    except Exception as e:
        print(f"Failed to establish SSH connection: {e}")
        return None
    
def closeSSHConnection():
    if sshClient.get_transport() and sshClient.get_transport().is_active():
        sshClient.close()