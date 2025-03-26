import tkinter as tk
from tkinter import messagebox
import os
import threading
from Backend_Files.Backup import download, closeSSHConnection
from Backend_Files.Debug import cardInfoD
from Backend_Files.Upload import uploadFiles

def create_ui(remotePaths, localPath):
    
    def getInfo(): # this is to get the device communication info 
        deviceIP = deviceIPEntry.get()
        deviceUsername = deviceUsernameEntry.get()
        devicePassword = devicePasswordEntry.get()
        if not deviceIP or not deviceUsername or not devicePassword:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        else:
            return deviceIP, deviceUsername, devicePassword
    
    def startBackup():
        info = getInfo()
        deviceIP, deviceUsername, devicePassword = info if info is not None else (None, None, None)
        if info:
            loadingLabel = tk.Label(auth_info_frame, text="Downloading, please wait...", fg="blue")
            loadingLabel.grid(row=5, column=0, columnspan=2, pady=10)
            threading.Thread(target=download, args=(deviceIP, deviceUsername, devicePassword, remotePaths, localPath, loadingLabel)).start()

    def startUpload():
        info = getInfo()
        deviceIP, deviceUsername, devicePassword = info if info is not None else (None, None, None)
        if info:
            loadingLabel = tk.Label(auth_info_frame, text="Uploading, please wait...", fg="blue")
            loadingLabel.grid(row=5, column=0, columnspan=2, pady=10)
            threading.Thread(target=uploadFiles, args=(deviceIP, deviceUsername, devicePassword, remotePaths, localPath, loadingLabel)).start()    
    
    def startDebug():
        if debug_frame.winfo_ismapped():
            debug_frame.pack_forget()
        else:
            debug_frame.pack(fill='both', expand=True)
        info = getInfo()
        if info is None:
            return
        print(info)
        debug_output.delete(1.0, tk.END)
        debug_info = cardInfoD(info)
        if debug_info:
            formatDebugInfo(debug_info)
        closeSSHConnection()
    
    def formatDebugInfo(debug_info):
        # Debug - general information section  
        debug_output.insert(tk.END, "\n Card's General Information \n\n", ('bold', 'center'))
        for key, value in debug_info.items():
            debug_output.insert(tk.END, f"{key}: ", 'bold')
            debug_output.insert(tk.END, f"{value}\n")
                  
    def startDebugMore():
        print('debug more was pressed')

            
    root = tk.Tk()
    root.title("SafeSync")
    root.iconbitmap("assets/Icon/SafeSync.ico")
    

    container = tk.Frame(root)
    container.grid(row=0, column=0, sticky='nsew')
    
    auth_info_frame = tk.Frame(container)
    auth_info_frame.grid(row=0, column=0, sticky='nsew')

    actn_button_frame = tk.Frame(container)
    actn_button_frame.grid(row=1, column=0, sticky='nsew')

    debug_frame = tk.Frame(container)
    debug_frame.grid(row=2, column=0, sticky='nsew')
    
    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)
    container.grid_rowconfigure(2, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
        
    auth_info_frame.grid_rowconfigure(0, weight=1)
    auth_info_frame.grid_rowconfigure(1, weight=1)
    auth_info_frame.grid_rowconfigure(2, weight=1)
    auth_info_frame.grid_rowconfigure(3, weight=1)
    auth_info_frame.grid_rowconfigure(4, weight=1)
    auth_info_frame.grid_rowconfigure(5, weight=1)
    auth_info_frame.grid_columnconfigure(0, weight=1)
    auth_info_frame.grid_columnconfigure(1, weight=1)
    auth_info_frame.grid_columnconfigure(2, weight=1)

    actn_button_frame.grid_rowconfigure(0, weight=1)
    actn_button_frame.grid_columnconfigure(0, weight=1)
    actn_button_frame.grid_columnconfigure(1, weight=1)
    actn_button_frame.grid_columnconfigure(2, weight=1)
    
    tk.Label(auth_info_frame, text="----------     Author - Shiv Ahir     ----------").grid(row=0, column=1, pady=10, sticky='nsew')

    
    tk.Label(auth_info_frame, text="Device IP Address:").grid(row=1, column=0, padx=10, pady=10,sticky='nsew')
    deviceIPEntry = tk.Entry(auth_info_frame, width=50)
    deviceIPEntry.grid(row=1, column=1, padx=10, pady=10,sticky='nsew')
    tk.Label(auth_info_frame, text="Device Username:").grid(row=2, column=0, padx=10, pady=10,sticky='nsew')
    deviceUsernameEntry = tk.Entry(auth_info_frame, width=50)
    deviceUsernameEntry.grid(row=2, column=1, padx=10, pady=10,sticky='nsew')
    tk.Label(auth_info_frame, text="Device Password:").grid(row=3, column=0, padx=10, pady=10,sticky='nsew')
    devicePasswordEntry = tk.Entry(auth_info_frame, width=50, show='*')
    devicePasswordEntry.grid(row=3, column=1, padx=10, pady=10,sticky='nsew')
    
    # UI for backup Section
    backupBtn = tk.Button(actn_button_frame, text="Start Backup", command=startBackup)
    backupBtn.grid(row=0, column=0, padx=10, pady=20, sticky='e')
    # Button for uploading backed up data to a card
    uploadBtn = tk.Button(actn_button_frame, text="Start Upload", command=startUpload)
    uploadBtn.grid(row=0, column=1, padx=10, pady=20)
    # UI for debugging Section
    debug_button = tk.Button(actn_button_frame, text="Debug", command=startDebug)
    debug_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')
    
    tk.Label(debug_frame, text="Debugging Section").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    debug_output = tk.Text(debug_frame, height=20, width=100, wrap='word')
    debug_output.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    debug_more_button = tk.Button(debug_frame, text="Debug More", command=startDebugMore)
    debug_more_button.grid(row=2, column=0, padx=100, pady=10, sticky='nsew')
    
    debug_output.tag_configure('bold', font=('Helvetica', 10, 'bold'))
    debug_output.tag_configure('center', justify='center')
    
    debug_frame.grid_rowconfigure(1, weight=1)
    debug_frame.grid_columnconfigure(0, weight=1)
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    deviceIPEntry.focus_set()
    root.mainloop()

def main():
    remotePaths = [
        '/udata/etc/network',
        '/udata/etc/mvx',
    ]
    localPath = os.path.join(os.getcwd(), "Backup")
    os.makedirs(localPath, exist_ok=True)
    create_ui(remotePaths, localPath)
    closeSSHConnection()

if __name__ == "__main__":
    main()



