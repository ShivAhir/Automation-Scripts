import threading
import time
from tkinter import filedialog
from Backend_Files.Connection import establishConnection, sshClient
from Backend_Files.Overview import ansiEscape
from Backend_Files.UILoadingWindow import show_loading_ui
from Backend_Files.LoggerConfig import logger


def download_logs(root, deviceIP, deviceUsername, devicePassword, overview=None, detail_debug_res=None):
    logger.info(
        "Attempting to download the logs captured on overview and detail debug")
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save File"
    )

    if not file_path:
        logger.warning("No file path selected. Operation canceled.")
        return None

    def download():

        try:
            establishConnection(deviceIP, deviceUsername, devicePassword, root)
            logger.info("SSH connection established successfully.")
            print("SSH connection established successfully.")
        except Exception as e:
            logger.error(
                f"An error occurred while establishing SSH connection: {e}")
            print(f"An error occurred while establishing SSH connection: {e}")
            show_loading_ui(
                root=root, title="Error", msg=f"An error occurred: {e}", type='Error Message'
            )
            return None

        if not sshClient.get_transport() or not sshClient.get_transport().is_active():
            logger.error("SSH connection is not active.")
            raise Exception("SSH connection is not active.")

        try:
            channel = sshClient.invoke_shell()
            channel.send('journalctl --no-pager\n')
            time.sleep(2)

            output = ""
            while channel.recv_ready():
                output += channel.recv(65535).decode('utf-8')

            cleaned_output = ansiEscape.sub('', output)

            with open(file_path, "w") as file:
                if overview:
                    file.write(overview + "\n")
                if detail_debug_res:
                    file.write(detail_debug_res + "\n\n\n\n\n")
                file.write(cleaned_output)
            progress_bar.stop()
            loading_window.destroy()

            show_loading_ui(
                root=root, title="Success", msg=f"Logs file has been saved to {file_path}", type='Success Message'
            )
            logger.info(f"Logs file has been saved to {file_path}")
            print(f"File saved to {file_path}")
        except Exception as e:
            logger.error(f"An error occurred while capturing logs: {e}")
            print(f"An error occurred while capturing logs: {e}")
            show_loading_ui(
                root=root, title="Error", msg=f"An error occurred: {e}", type='Error Message'
            )
            return None
    thread = threading.Thread(target=download)
    thread.start()
    loading_window, progress_bar = show_loading_ui(
        root=root, title="Processing", msg="Downloading logs, please wait...", type=None
    )
