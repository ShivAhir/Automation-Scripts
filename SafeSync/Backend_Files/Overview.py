import re
import time
from tkinter import messagebox
from Backend_Files.Connection import establishConnection, sshClient
from Backend_Files.UILoadingWindow import show_loading_ui
from Backend_Files.logger_config import logger

failedServices = set()
ansiEscape = re.compile(r'\x1b\[.*?m')
results = {}
commands = ['cat /version',
            'mvdb-get cardinfo.app.name',
            'mvdb-get cardinfo.license.serial_num',
            'mvdb-get cardinfo.license.mac_addr',
            'mvdb-get cardinfo.platform',
            'mvdb-get cardinfo.prod',
            'sudo dmidecode -t 0x0002',
            'uptime',
            "systemctl list-units --state=failed --no-legend --plain | awk '/.service/ {print $1}'",
            ]
formattedCommands = {
    'cat /version': 'Firmware Version',
    'mvdb-get cardinfo.app.name': 'App Name',
    'mvdb-get cardinfo.license.serial_num': 'Serial Number',
    'mvdb-get cardinfo.license.mac_addr': 'MAC Address',
    'mvdb-get cardinfo.platform': 'Hardware Type',
    'mvdb-get cardinfo.prod': 'Product Name',
    'sudo dmidecode -t 0x0002': 'Hardware Configuration',
    'uptime': "Card's uptime",
    "systemctl list-units --state=failed --no-legend --plain | awk '/.service/ {print $1}'": 'Failed Services',
}


def readMultiLines(out):  # Function to read multiline outputs and send them as a list
    global failedServices
    failedServices.clear()
    lines = out.split('\n')
    services = []
    for line in lines:
        service_name = line.strip()
        if service_name and not service_name.startswith("systemctl") and not service_name.endswith(":~$"):
            logger.info(
                f'This is inside readMultiLines function - {service_name}')
            if service_name not in services:
                services.append(service_name)
                failedServices.add(service_name)
    return ','.join(services)


def remove_escape_sequences(output):
    ansi_escape = re.compile(r'\x1b\[.*?[@-~]')
    cleaned_output = ansi_escape.sub('', output)
    return cleaned_output


def formattedOutput(out, command):
    if command == 'cat /version':
        match = re.search(r'(\d+\.\d+\.\d+-\d+-[a-f0-9]+-\d+)', out)
    elif command.startswith('license-decode'):
        match = re.search(r'(\+[\w\+\|]+)', out)
    elif command.startswith('mvdb-get'):
        match = re.search(r'Result:\s*(.*)', out)
    elif command == "systemctl list-units --state=failed --no-legend --plain | awk '/.service/ {print $1}'":
        logger.info(f"This is the output of systemctl {out}")
        return readMultiLines(out) if readMultiLines(out) else None
    elif command == 'sudo dmidecode -t 0x0002':
        match = re.search(r'Manufacturer:\s*([^\r\n]+)', out)
        if not match:
            logger.info("Overview: Manufacturer pattern not found in output")
            print("Overview: Manufacturer pattern not found in output")
    elif command == 'uptime':
        match = re.search(r'uptime\s*(.*)', out)
        if not match:
            logger.info("Overview: Uptime pattern not found in output")
            print("Overview: Uptime pattern not found in output")
    else:
        match = None
    if match:
        result = match.group(1).strip()
        return result
    else:
        logger.error(f"Desired output not found for command: {command}")
        print(f"Desired output not found for command: {command}")
        return None


def runCommand(command, channel, password=None):
    if password and command.startswith('sudo'):
        channel.send(f'{command}\n')
        time.sleep(0.1)
        if channel.recv_ready():
            output = channel.recv(65535).decode('utf-8')
            if 'password for' in output:
                channel.send(f'{password}\n')
                time.sleep(0.1)
                output += channel.recv(65535).decode('utf-8')
        output = remove_escape_sequences(output)
        results[command] = formattedOutput(output, command)
    else:
        channel.send(f'{command}\n')
        time.sleep(0.2)
        output = channel.recv(65535).decode('utf-8')
        logger.debug(output)
        output = remove_escape_sequences(output)
        results[command] = formattedOutput(output, command)\



def cardInfoD(info, root):
    global results
    results.clear()
    deviceIP, deviceUsername, devicePassword = info if info is not None else (
        None, None, None)
    try:
        if establishConnection(deviceIP, deviceUsername, devicePassword,root):
            loading_window, progress_bar = show_loading_ui(
                root=root, title='Loading', msg="Loading results, please wait...")
            establishConnection(deviceIP, deviceUsername, devicePassword,root)
            logger.info("Connection established for overview.")
            print("Connection established for overview.")
            if not sshClient.get_transport() or not sshClient.get_transport().is_active():
                logger.error("SSH connection is not established for overview.")
                raise Exception(
                    "SSH connection is not established for overview.")
            channel = sshClient.invoke_shell()
            for command in commands:
                runCommand(command, channel, devicePassword)
                if results.get('mvdb-get cardinfo.license.mac_addr'):
                    name = results.get('mvdb-get cardinfo.app.name')
                    sn_num = results.get(
                        'mvdb-get cardinfo.license.serial_num')
                    mac_addr = results.get(
                        'mvdb-get cardinfo.license.mac_addr')

                    if name and sn_num and mac_addr:
                        if name == 'sVIP':
                            vipType = 'vip-svr'
                        elif name == 'cVIP':
                            vipType = 'vip-sw'
                            sn_num = 'None'
                            results['mvdb-get cardinfo.license.serial_num'] = 'None'
                        elif name == 'evVIP-SDI':
                            vipType = 'vip-sdi'
                        elif name == 'evVIP-J2K':
                            vipType = 'vip-j2k'
                        elif name == 'evUDX-IP':
                            vipType = 'udx-ip'
                        else:
                            vipType = 'vip'
                        final_command = f'license-decode /etc/mvx/{vipType}/license.key {name} {sn_num} {mac_addr}'
                        if not results.get('Decoded License'):
                            channel.send(f'{final_command}\n')
                            time.sleep(0.1)
                            out = ansiEscape.sub(
                                '', channel.recv(65535).decode('utf-8'))
                            logger.debug(out)
                            results['Decoded License'] = formattedOutput(
                                out, final_command)
                            if not results['Decoded License']:
                                logger.error(
                                    "Required values for the final command are missing.")
                                print(
                                    "Required values for the final command are missing.")
                                results['final_command'] = None
                    formatted_results = {formattedCommands.get(
                        cmd, cmd): res for cmd, res in results.items()}
                    logger.info("Fomatted results in overview",
                                formatted_results)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}", parent=root)
        return None

    progress_bar.stop()
    loading_window.destroy()
    return formatted_results
