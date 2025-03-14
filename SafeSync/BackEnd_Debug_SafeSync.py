import logging
import re
import time
from tkinter import messagebox
from BackEnd_Backup_SafeSync import establishConnection, sshClient

logging.basicConfig(
    filename='app.log',  
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
            "systemctl --failed --no-legend | awk '{print $2}'"
]
formattedCommands = {
    'cat /version': 'Firmware Version',
    'mvdb-get cardinfo.app.name': 'App Name',
    'mvdb-get cardinfo.license.serial_num': 'Serial Number',
    'mvdb-get cardinfo.license.mac_addr': 'MAC Address',
    'mvdb-get cardinfo.platform' : 'Hardware Type',
    'mvdb-get cardinfo.prod': 'Product Name',
    'sudo dmidecode -t 0x0002': 'Hardware Configuration',
    'uptime': "Card's uptime",
    "systemctl --failed --no-legend | awk '{print $2}'": 'Failed Services',
}

def readMultiLines(out): # function to read multiline outputs and sends it as a list
    lines = out.split('\n')
    capturing = False
    services = []
    for line in lines:
        if "systemctl --failed --no-legend | awk " in line:
            capturing = True
            continue
        if capturing and line.strip().endswith(':~$'):
            capturing = False
            break
        if capturing:
            services.append(line.strip())
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
    elif command == "systemctl --failed --no-legend | awk '{print $2}'":
        return readMultiLines(out) if readMultiLines(out) else None
    elif command == 'sudo dmidecode -t 0x0002':
        match = re.search(r'Manufacturer:\s*([^\r\n]+)', out)
        if not match:
            print("Debug: Manufacturer pattern not found in output")
            print("Output was:", out)
    elif command == 'uptime':
        match = re.search(r'uptime\s*(.*)', out)
        if not match:
            print("Debug: Uptime pattern not found in output")
            print("Output was:", out)
    else:
        match = None
    if match:
        result = match.group(1).strip()
        return result
    else:
        print(f"Desired output not found for command: {command}")
        return None

def runCommand(command, channel,password=None):
    if password and command.startswith('sudo'):
        channel.send(f'{command}\n')
        time.sleep(0.5)
        if channel.recv_ready():
            output = channel.recv(65535).decode('utf-8')
            if 'password for' in output:
                channel.send(f'{password}\n')
                time.sleep(0.5)
                output += channel.recv(65535).decode('utf-8')
        output = remove_escape_sequences(output)
        results[command] = formattedOutput(output, command)
    else: 
        channel.send(f'{command}\n')
        time.sleep(0.3)
        output = channel.recv(65535).decode('utf-8')
        logging.debug(output)
        output = remove_escape_sequences(output)
        results[command] = formattedOutput(output, command)


def cardInfoD(info):
    deviceIP, deviceUsername, devicePassword = info if info is not None else (None, None, None)
    try:
        print("Establishing connection...")
        establishConnection(deviceIP, deviceUsername, devicePassword)
        print("Connection established.")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
    
    if not sshClient.get_transport() or not sshClient.get_transport().is_active():
        raise Exception("SSH connection is not established.")
    
    channel = sshClient.invoke_shell()
    for command in commands:
        runCommand(command, channel,devicePassword)
        if results.get('mvdb-get cardinfo.license.mac_addr'):
            name = results.get('mvdb-get cardinfo.app.name')
            sn_num = results.get('mvdb-get cardinfo.license.serial_num')
            mac_addr = results.get('mvdb-get cardinfo.license.mac_addr')

            if name and sn_num and mac_addr:
                if name == 'sVIP':
                    vipType = 'vip-svr'
                elif name == 'cVIP':
                    vipType = 'vip-sw'
                    sn_num = 'None'
                    results['mvdb-get cardinfo.license.serial_num'] = 'None'
                else:
                    vipType = 'vip'
                final_command = f'license-decode /etc/mvx/{vipType}/license.key {name} {sn_num} {mac_addr}'
                channel.send(f'{final_command}\n')
                time.sleep(0.3)
                out = ansiEscape.sub('', channel.recv(65535).decode('utf-8'))
                logging.debug(out)
                results['Decoded License'] = formattedOutput(out, final_command)
                if not results['Decoded License']:
                    print("Required values for the final command are missing.")
                    results['final_command'] = None
            formatted_results = {formattedCommands.get(cmd, cmd): res for cmd, res in results.items()}
            logging.debug(formatted_results)
     
    return formatted_results





