import paramiko  # type: ignore 
import socket
import time

flag = True
rebootCounter = 0

check_lsblk_str = """
NAME             MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda                8:0    0 223.1G  0 disk
├─sda1             8:1    0     2M  0 part
├─sda2             8:2    0   256M  0 part
├─sda3             8:3    0 222.7G  0 part
│ ├─evertz-app1  252:0    0    32G  0 lvm
│ ├─evertz-app2  252:1    0    32G  0 lvm  /
│ └─evertz-udata 252:2    0 158.7G  0 lvm  /udata
└─sda4             8:4    0    48M  0 part
sdb                8:16   0 893.8G  0 disk
"""

def normalize_lsblk_output(output):
    return '\n'.join(line.strip() for line in output.strip().splitlines())

def is_server_online(hostname, port, timeout=5):
    try:
        sock = socket.create_connection((hostname, port), timeout)
        sock.close()
        return True
    except socket.error:
        return False

def wait_for_server(hostname, port, timeout=90, interval=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_server_online(hostname, port):
            return True
        time.sleep(interval)
    return False


def ssh_connect_and_execute(hostname, port, username, password, commands):
    global flag, rebootCounter
    try:
        print("trying to connect now!")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
        ssh_client.connect(hostname, port, username, password)
        print(f"Connected to {hostname}")
        
        for command in commands:
            print(f"Executing command: {command}")
            stdin, stdout, stderr = ssh_client.exec_command(command)            
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"Output:\n{output}")
            if error:
                print(f"Error:\n{error}")
            
            if command == 'lsblk':
                normalized_output = normalize_lsblk_output(output)
                normalized_check_lsblk_str = normalize_lsblk_output(check_lsblk_str)
                if normalized_output == normalized_check_lsblk_str:
                    print('The lsblk output is the same as the check_lsblk_str value.')
                else:
                    print('The lsblk output is different from the check_lsblk_str value.')
                    print('Saw this error after '+ str(rebootCounter) + 'reboots.')
                    flag = False
                    ssh_client.close()
                    print("Connection closed")
                    break

            if command == "sudo reboot":
                print("Server is rebooting...")
                ssh_client.close()
                print("Connection closed. Waiting for the server to come back online...")
                rebootCounter + 1
                print("Reboot Counter" + str(rebootCounter))
                time.sleep(3)
                if wait_for_server(hostname, port):
                    print("Server is back online. Reconnecting...")
                    while True:
                        try:
                            ssh_client.connect(hostname, port, username, password)
                            print(f"Reconnected to {hostname}")
                            break
                        except paramiko.ssh_exception.NoValidConnectionsError:
                            print("Server is not ready yet. Retrying...")
                            time.sleep(5)
                else:
                    print("Server did not come back online within the timeout period.")
                    return
        ssh_client.close()
        print("Connection closed")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    hostname = "172.16.177.179"
    port = 22
    username = "mvx"
    password = "mvx"
    commands = [
        "lsblk",
        "sudo reboot",
        "lsblk",
    ]

    while flag:
        # Connect to the server and execute the commands
        ssh_connect_and_execute(hostname, port, username, password, commands)