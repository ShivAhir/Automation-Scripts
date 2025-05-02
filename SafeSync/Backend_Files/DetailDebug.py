import re
import time
from Backend_Files.Connection import establishConnection, sshClient
from Backend_Files.Overview import ansiEscape, failedServices
from Backend_Files.UILoadingWindow import show_loading_ui
from Backend_Files.LoggerConfig import logger

results = {}
raw_results = ''


def formatted_output(output):
    out = []
    for line in output.split('\n'):
        if re.search(r'error|failed', line, re.IGNORECASE):
            out.append(line)
    return '\n'.join(out)

# Function to read multiline outputs and send them as a string


def readMultiLines(out, service):
    lines = out.split('\n')
    global raw_results
    raw_results += service + "\n"
    for line in lines:
        logs = line.strip()
        if logs and not logs.startswith("journalctl") and not logs.endswith(":~$"):
            logger.info(
                f'This is inside download logs readMultiLines function - {logs}')
            raw_results += logs + "\n"
    raw_results += "\n"


def detail_debug(info, root):
    global results, raw_results
    raw_results = ''
    results.clear()
    deviceIP, deviceUsername, devicePassword = info if info is not None else (
        None, None, None)
    try:
        establishConnection(deviceIP, deviceUsername, devicePassword, root)
        logger.info("Connection established in detailed debug.")
        print("Connection established in detailed debug.")
        print(
            f"This is the list of failed services inside detail debug! {failedServices}")
    except Exception as e:
        logger.error(f"An error occurred: {e} in detailed debug")
        print(f"An error occurred: {e} in detailed debug")
        loading_window = show_loading_ui(
            root=root, title="Error", msg=f"An error occurred: {e}", type='Error Message')
        return None

    if not sshClient.get_transport() or not sshClient.get_transport().is_active():
        logger.error("SSH connection is not established for detailed debug.")
        raise Exception(
            "SSH connection is not established for detailed debug.")
    channel = sshClient.invoke_shell()
    for service in failedServices:
        print(
            f"This is the list of failed services inside for loop of detail debug! {failedServices}")
        channel.send(f'journalctl -u {service} -n 50 --no-pager\n')
        time.sleep(0.2)
        out = ansiEscape.sub('', channel.recv(65535).decode('utf-8'))
        if not re.search(r'-- No entries --', out):
            readMultiLines(out=out, service=service)
            out = formatted_output(out)
            results[service] = out
            logger.info(f"Detailed debug for {service}: {out}")
    print("this is the result of raw_result on detail debug: ", raw_results)
    return results, raw_results
