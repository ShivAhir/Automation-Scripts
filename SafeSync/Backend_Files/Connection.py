import paramiko # type: ignore
from tkinter import messagebox

sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
channel = None
def establishConnection(IP, userName, password):
    global channel
    try:
        sshClient.connect(hostname=IP, port=22, username=userName, password=password, timeout=2)
        channel = sshClient.invoke_shell() 
        return sshClient
    except Exception as e:
        print(f"Failed to establish SSH connection: {e}")
        messagebox.showerror("Error", f"An error occurred: Check Credentials!")
        return None
    

def closeSSHConnection():
    global channel
    if sshClient.get_transport() and sshClient.get_transport().is_active():
        sshClient.close()
        channel = None