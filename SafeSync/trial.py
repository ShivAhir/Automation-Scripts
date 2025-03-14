# from BackEnd_Backup_SafeSync import establishConnection, sshClient
# import time

# channel = sshClient.invoke_shell()


# channel.send(f'{command}\n')
# time.sleep(0.5)
# if channel.recv_ready():
#     output = channel.recv(65535).decode('utf-8')
#     if 'password for' in output:
#         channel.send(f'{password}\n')
#         time.sleep(0.5)
#         output += channel.recv(65535).decode('utf-8')
# print(output)
# if command == "systemctl --failed --no-legend | awk '{print $2}'":         
#     print ("before remove escape:",output)