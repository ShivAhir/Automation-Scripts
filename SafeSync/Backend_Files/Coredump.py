import time
from tkinter import messagebox
from Backend_Files.Connection import closeSSHConnection, establishConnection, sshClient
from Backend_Files.UILoadingWindow import show_loading_ui
from Backend_Files.logger_config import logger


def enable_coredump(deviceIP, deviceUsername, devicePassword, root):
    # deviceIP, deviceUsername, devicePassword = info if info is not None else (
    #     None, None, None)
    try:
        if establishConnection(deviceIP, deviceUsername, devicePassword, root):
            establishConnection(deviceIP, deviceUsername, devicePassword, root)
            logger.info("Connection established in enable_coredump.")
            print("Connection established in enable coredump.")
            if not sshClient.get_transport() or not sshClient.get_transport().is_active():
                logger.error(
                    "SSH connection is not established for enable coredump.")
                raise Exception(
                    "SSH connection is not established for enable coredump.")

            response = messagebox.askyesno(
                "Confirmation", "Enabling Coredumps require a reboot, do you want to proceed? ", parent=root)
            if response:
                channel = sshClient.invoke_shell()
                channel.send(
                    f'sudo rm -rf /etc/sysctl.d/50-disable-coredump.conf\n')
                time.sleep(0.1)
                if channel.recv_ready():
                    output = channel.recv(65535).decode('utf-8')
                    if 'password for' in output:
                        channel.send(f'{devicePassword}\n')
                        logger.info(f'enable coredump output {output}')
                        print(f'enable coredump output {output}')
                        time.sleep(0.1)
                        output += channel.recv(65535).decode('utf-8')
                channel.send('sudo reboot\n')
                time.sleep(0.1)
                channel.send(f'{devicePassword}\n')
                logger.info('Coredumps were enabled.')
                logger.info(
                    'Closing the SSH connection after rebooting the card in enable coredumps.')
                closeSSHConnection()

    except Exception as e:
        logger.error(f"An error occurred: {e} in enable coredump")
        print(f"An error occurred: {e} in enable coredump")
        loading_window = show_loading_ui(
            root=root, title="Error", msg=f"An error occurred: {e}", type='Error Message')
        return None


def dump_coredumps(info, root):
    deviceIP, deviceUsername, devicePassword = info if info is not None else (
        None, None, None)
    try:
        establishConnection(deviceIP, deviceUsername, devicePassword, root)
        logger.info("Connection established in dump coredump.")
        print("Connection established in dump coredump.")
    except Exception as e:
        logger.error(f"An error occurred: {e} in dump coredump")
        print(f"An error occurred: {e} in dump coredump")
        loading_window = show_loading_ui(
            root=root, title="Error", msg=f"An error occurred: {e}", type='Error Message')
        return None

    if not sshClient.get_transport() or not sshClient.get_transport().is_active():
        logger.error("SSH connection is not established for dump coredump.")
        raise Exception("SSH connection is not established for dump coredump.")
    channel = sshClient.invoke_shell()
