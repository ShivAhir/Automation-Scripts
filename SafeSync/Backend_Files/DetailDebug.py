import logging
import re
import time
from tkinter import messagebox
from Backend_Files.Connection import establishConnection, sshClient
from Backend_Files.Overview import ansiEscape, failedServices
from Backend_Files.logger_config import logger

results = {}

def formatted_output(output):
    out = []
    for line in output.split('\n'):
        if re.search(r'error|failed', line, re.IGNORECASE):
            out.append(line)
    return '\n'.join(out)


def detail_debug(info):
    deviceIP, deviceUsername, devicePassword = info if info is not None else (None, None, None)
    try:
        establishConnection(deviceIP, deviceUsername, devicePassword)
        logger.info("Connection established in detailed debug.")
        print("Connection established in detailed debug.")
    except Exception as e:
        logger.error(f"An error occurred: {e} in detailed debug")
        print(f"An error occurred: {e} in detailed debug")
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
    
    if not sshClient.get_transport() or not sshClient.get_transport().is_active():
        logger.error("SSH connection is not established for detailed debug.")
        raise Exception("SSH connection is not established for detailed debug.")
    channel = sshClient.invoke_shell() 
    for service in failedServices:
        channel.send(f'journalctl -u {service} -n 35 --no-pager\n')
        time.sleep(0.2)
        out = ansiEscape.sub('', channel.recv(65535).decode('utf-8'))
        if not re.search(r'-- No entries --', out):
            out = formatted_output(out)
            print('detailed debug', service, "\n")
            print(out)
            print('----------------------------------------------------------------------------------------------------')
            results[service] = out
            logging.debug(out)
        print("Detailed debug results:", results)
    return results
