import paramiko  # type: ignore
from Backend_Files.UILoadingWindow import show_loading_ui
from Backend_Files.logger_config import logger

sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def establishConnection(IP, userName, password, root=None):
    try:
        loading_window, progress_bar = show_loading_ui(
            root=root, title="Processing", msg="Connecting...")
        sshClient.connect(hostname=IP, port=22,
                          username=userName, password=password, timeout=0.5)
        progress_bar.stop()
        loading_window.destroy()
        return sshClient
    except Exception as e:
        logger.info(f"Failed to establish SSH connection: {e}")
        progress_bar.stop()
        loading_window.destroy()
        show_loading_ui(
            root=root, title="Error", msg=f"An error occurred: Check Credentials!", type='Error Message')
        # messagebox.showerror("Error", f"An error occurred: Check Credentials!")
        return None


def closeSSHConnection():
    global channel
    if sshClient.get_transport() and sshClient.get_transport().is_active():
        sshClient.close()
        channel = None
