import os
from tkinter import filedialog
from Backend_Files.Connection import sshClient, establishConnection, closeSSHConnection
from Backend_Files.UILoadingWindow import show_loading_ui
from scp import SCPClient  # type: ignore
from Backend_Files.LoggerConfig import logger


# to show the progression of how much a file has been downloaded on the logs
def progress(filename, size, sent):
    logger.info(
        f"Transferring {filename}: {float(sent) / float(size)*100:.2f}%")
    print(f"Transferring {filename}: {float(sent) / float(size)*100:.2f}%")


def downloadFolder(remote_path, local_path):
    try:
        os.makedirs(local_path, exist_ok=True)

        scp = SCPClient(sshClient.get_transport(),
                        progress=progress)  # type: ignore
        stdin, stdout, stderr = sshClient.exec_command(
            f"test -d {remote_path} && echo 'Directory' || echo 'Not a directory'")
        result = stdout.read().decode().strip()

        if result != "Directory":
            logger.error(
                f"Error: {remote_path} is not a directory or doesn't exist on the remote server.")
            print(
                f"Error: {remote_path} is not a directory or doesn't exist on the remote server.")
            return False

        # Getting the list of files in remote directory
        stdin, stdout, stderr = sshClient.exec_command(
            f"find {remote_path} -type f | sort")
        files = stdout.read().decode().strip().split('\n')

        # Downloading each file in the directory
        logger.info(f"Downloading {len(files)} files from {remote_path}...")
        print(f"Downloading {len(files)} files from {remote_path}...")
        for remote_file in files:
            if not remote_file:
                continue
            rel_path = os.path.relpath(remote_file, remote_path)
            local_file_path = os.path.join(local_path, rel_path)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            scp.get(remote_file, local_file_path)
        scp.close()
        logger.info(
            f"\nSuccessfully downloaded folder from {remote_path} to {local_path}")
        print(
            f"\nSuccessfully downloaded folder from {remote_path} to {local_path}")
        return True
    except Exception as e:
        logger.error(f"Error downloading folder: {str(e)}")
        print(f"Error downloading folder: {str(e)}")
        return False


def download(deviceIP, deviceUsername, devicePassword, remotePaths, root):

    folder_path = filedialog.askdirectory(
        title="Select Folder to Save the Backup")
    flag = True
    if folder_path:
        try:
            if establishConnection(deviceIP, deviceUsername, devicePassword, root):
                establishConnection(
                    deviceIP, deviceUsername, devicePassword, root)
                logger.info("Connection established for backup.")
                print("Connection established for backup.")
                loading_window, progress_bar = show_loading_ui(
                    root=root, title="Processing", msg="Downloading the backup files, please wait...")
                for remotePath in remotePaths:
                    logger.info(f"Downloading folder: {remotePath}")
                    print(f"Downloading folder: {remotePath}")
                    success = downloadFolder(remotePath, folder_path)
                    if not success:
                        flag == False
                        logger.error(
                            f"Failed to download folder: {remotePath}")
                        print(f"Failed to download folder: {remotePath}")
                        progress_bar.stop()
                        loading_window.destroy()
                        show_loading_ui(
                            root=root, title="Error", msg=f"Failed to download folder: {remotePath}", type='Error Message')
                        break
                if flag:
                    logger.info(
                        f"Successfully downloaded folders to {folder_path}")
                    print(f"Successfully downloaded folders to {folder_path}")
                    progress_bar.stop()
                    loading_window.destroy()
                    loading_window = show_loading_ui(
                        root=root, title="Success", msg=f"Backup files has been saved to {folder_path}", type='Success Message')
        except Exception as e:
            flag == False
            logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
            loading_window = show_loading_ui(
                root=root, title="Error", msg=f"An error occurred: {e}", type='Error Message')
        finally:
            closeSSHConnection()
            logger.info("Connection closed for backup.")
            print("Connection closed.")
    else:
        return
