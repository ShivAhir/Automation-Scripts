import os
import time
import re
import paramiko  # type: ignore

# change the IP as per your unit
IP = '172.16.176.136'
userName = 'mvx'
password = 'mvx'


inputVariable = input("Enter which input are you configuring to record Nielson Data: ")
while True:
    print("\nMake Your Choice\n1. Enable\n2. Dump Logs\n3. Clear Logs\n0. Disable\n")
    key = int(input("Enter your choice:"))  # key is to set the enable or disable or dump deep logging (1 = enable, 0 = disable, 2 = dump logs)
    print("\n")

    sshCLient = paramiko.SSHClient()
    sshCLient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshCLient.connect(hostname=IP, port=22, username=userName, password=password) 
    ansiEscape = re.compile(r'\x1b\[.*?m')
    output = []

    channel = sshCLient.invoke_shell()
    channel.send('menu\n')
    time.sleep(0.3)

    # this snippet is to select the correct option that allows us to select the correct option 
    option = ansiEscape.sub('',channel.recv(65535).decode('utf-8'))
    for line in option.splitlines():
        if 'Nielsen Monitoring Menu' in line:
            result = line.replace(') Nielsen Monitoring Menu', '')
            result = result.replace('(', '')
    channel.send(result+'\n')  # this is for selecting the Nielson Monitoring menu option on the menu
    time.sleep(0.3)
    channel.send('14\n')
    time.sleep(0.3)

    # this is a function that saves the output to a file
    def save_output_to_file(filePath, output):
        with open(filePath, 'w') as file:
            for line in output:
                file.write(line)
                
    # this is a function that dumps the logs 
    def dumpLogs(type,channelCounter, filePath):
        channel.send(str(type) + "\n")
        channel.send(inputVariable + '\n')
        channel.send(str(channelCounter)+'\n') 
        time.sleep(0.3)
        out = ansiEscape.sub('',channel.recv(65535).decode('utf-8'))
        if type == "2":
            start_printing = False
            for line in out.splitlines():
                if start_printing:
                    output.append(line)
                    output.append('\n')
                    if "----------------------------------------------------------------" in line:
                        start_printing = False  
                else:
                    if "Deep log for" in line or "Nielsen Hybrid Decoder" in line:
                        start_printing = True  
                        output.append(line)
                        output.append('\n')
            save_output_to_file(filePath, output)
            output.clear()
            
        elif type == "3":
            start_printing = False
            for line in out.splitlines():
                if start_printing:
                    output.append(line)
                    output.append('\n')
                    if "----------------------------------------------------------------" in line:
                        start_printing = False  
                else:
                    if "Deep log for" in line or "NAES 6 decoder" in line:
                        start_printing = True  
                        output.append(line)
                        output.append('\n')
            save_output_to_file(filePath, output)
            output.clear()
                
        elif type == "4":
            start_printing = False
            for line in out.splitlines():
                if start_printing:
                    output.append(line)
                    output.append('\n')
                    if "----------------------------------------------------------------" in line:
                        start_printing = False
                else:
                    if "Deep log for" in line or "Nielsen CBET decoder" in line:
                        start_printing = True 
                        output.append(line)
                        output.append('\n')
            save_output_to_file(filePath, output)
            output.clear()
            
        
    if key == 0: # it disables the recording on channels 
        for i in range(8):
            channel.send('1\n')
            channel.send(inputVariable + '\n')
            channel.send(str(i)+'\n')
            channel.send('0\n')
        time.sleep(0.2)
        output = channel.recv(65535).decode('utf-8')
        for line in output.splitlines():
            if f"deep logging for input {inputVariable}, channel" in line:
                print(line)
        
    if key == 1: # it enables the recording on channels 
        for i in range(8):
            channel.send('1\n')
            channel.send(inputVariable + '\n') # input
            channel.send(str(i)+'\n')
            channel.send('1\n') 
        time.sleep(0.2)
        output = channel.recv(65535).decode()
        for line in output.splitlines():
            if f"deep logging for input {inputVariable}, channel" in line:
                print(line)
                
    if key == 2: # it enables dumping logs
        streamFolderName = input("Enter the stream folder name: ")
        streamName = input("Enter the stream name: ")
        nielsenTypes = ["NAESII", "NW", "CBET"]
        
        for type in nielsenTypes:
            folderName = f"{streamFolderName}/{streamName}/{type}--{streamName}"
            os.makedirs(folderName, exist_ok=True)    
            for i in range(8):
                fileName = f"Channel-{i}.txt"
                filePath = os.path.join(folderName, fileName)
                if type == "NAESII":
                    print(f"dumping NAESII channel {i}")
                    dumpLogs("2",i,filePath)
                elif type == "NW":
                    print(f"dumping NW channel {i}")
                    dumpLogs("3",i,filePath)
                elif type == "CBET":
                    print(f"dumping CBET channel {i}")
                    dumpLogs("4",i,filePath) 
    if key == 3: # it clears all the logs
        for i in range(8):
            channel.send('5\n')
            channel.send(inputVariable + '\n')
            channel.send(str(i)+'\n')
            time.sleep(0.2)
            output = channel.recv(65535).decode('utf-8')
            for line in output.splitlines():
                if f"Cleared deep log for input {inputVariable}, channel" in line:
                    print(line)
    
    choice = input('Do you want to continue again? (Y/N): ').upper().strip()
    if choice == 'N':
        break
channel.close()
sshCLient.close()
