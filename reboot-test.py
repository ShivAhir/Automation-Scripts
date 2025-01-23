import paramiko  # type: ignore 
import socket
import time

flag = True
rebootCounter = 0


def server_status(hostname, port, timeout=5):
    try:
        sock = socket.create_connection((hostname, port), timeout)
        sock.close()
        return True
    except socket.error:
        return False

def wait_for_server(hostname, port, timeout=90, interval=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if server_status(hostname, port):
            return True
        time.sleep(interval)
    return False

def check_sdb_parts(output):
    lines = output.splitlines()
    sdb_partitions = [line for line in lines if line.startswith('sdb')]
    return len(sdb_partitions) > 1

# this function will create the connection and perform the commands
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
                if check_sdb_parts(output):
                    print('sdb has partitions')
                    print('Saw this error after '+ str(rebootCounter) + 'reboots.')
                    flag = False
                    ssh_client.close()
                    print("Connection closed")
                    break
                else:
                    print('sda has partitions')

            if command == "sudo reboot":
                print("Server is rebooting...")
                ssh_client.close()
                print("Connection closed. Waiting for the server to come back online...")
                rebootCounter += 1
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
    hostname = "172.16.177.179"     # the IP for whatever device you want to perform the reboot test on
    port = 22
    username = "mvx"                # username for it
    password = "mvx"                # the password for it   
    commands = [
        "lsblk",
        "sudo reboot",
        "lsblk",
    ]

    while flag:
        ssh_connect_and_execute(hostname, port, username, password, commands)
