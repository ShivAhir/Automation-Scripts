import tkinter as tk
from tkinter import messagebox
import os
import threading
from BackEnd_Backup_SafeSync import downloadFolder, establishConnection, closeSSHConnection
from BackEnd_Debug_SafeSync import cardInfoD

def create_ui(remotePaths, localPath):
    
    def getInfo():
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
        loadingLabel = tk.Label(backup_frame, text="Downloading, please wait...", fg="blue")
        loadingLabel.grid(row=4, column=0, columnspan=2, pady=10)
        
        def download():
            try:
                print("Establishing connection...")
                establishConnection(deviceIP, deviceUsername, devicePassword)
                print("Connection established.")
                for remotePath in remotePaths:
                    print(f"Downloading folder: {remotePath}")
                    success = downloadFolder(remotePath, localPath)
                    if not success:
                        print(f"Failed to download folder: {remotePath}")
                        messagebox.showerror("Error", f"Failed to download folder: {remotePath}")
                        break
                else:
                    print(f"Successfully downloaded folders to {localPath}")
                    messagebox.showinfo("Success", f"Successfully downloaded folders to {localPath}")
            except Exception as e:
                print(f"An error occurred: {e}")
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                print("Closing connection...")
                closeSSHConnection()
                print("Connection closed.")
                loadingLabel.destroy()
        threading.Thread(target=download).start()
        
    
    def startDebug():
        if debug_frame.winfo_ismapped():
            debug_frame.pack_forget()
        else:
            debug_frame.pack(fill='both', expand=True)
        displayCardInfoD()
        
    def displayCardInfoD():
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
        for key, value in debug_info.items():
            debug_output.insert(tk.END, f"{key}: ", 'bold')
            debug_output.insert(tk.END, f"{value}\n")
    
            
    root = tk.Tk()
    root.title("SafeSync")
    
    container = tk.Frame(root)
    container.grid(row=0, column=0, sticky='nsew')
    
    backup_frame = tk.Frame(container)
    backup_frame.grid(row=0, column=0, sticky='nsew')

    debug_frame = tk.Frame(container)
    debug_frame.grid(row=1, column=0, sticky='nsew')
    
    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    # backup_frame = tk.Frame(container)
    # backup_frame.pack(fill='both', expand=True)
    # debug_frame = tk.Frame(container)
    # debug_frame.grid(row=0, column=0, sticky='nsew')
        
    backup_frame.grid_rowconfigure(0, weight=1)
    backup_frame.grid_rowconfigure(1, weight=1)
    backup_frame.grid_rowconfigure(2, weight=1)
    backup_frame.grid_rowconfigure(3, weight=1)
    backup_frame.grid_rowconfigure(4, weight=1)
    backup_frame.grid_columnconfigure(0, weight=1)
    backup_frame.grid_columnconfigure(1, weight=1)
    
    
    tk.Label(backup_frame, text="Device IP Address:").grid(row=0, column=0, padx=10, pady=10,sticky='nsew')
    deviceIPEntry = tk.Entry(backup_frame, width=50)
    deviceIPEntry.grid(row=0, column=1, padx=10, pady=10,sticky='nsew')
    tk.Label(backup_frame, text="Device Username:").grid(row=1, column=0, padx=10, pady=10,sticky='nsew')
    deviceUsernameEntry = tk.Entry(backup_frame, width=50)
    deviceUsernameEntry.grid(row=1, column=1, padx=10, pady=10,sticky='nsew')
    tk.Label(backup_frame, text="Device Password:").grid(row=2, column=0, padx=10, pady=10,sticky='nsew')
    devicePasswordEntry = tk.Entry(backup_frame, width=50, show='*')
    devicePasswordEntry.grid(row=2, column=1, padx=10, pady=10,sticky='nsew')
    
    # UI for backup Section
    backupBtn = tk.Button(backup_frame, text="Start Backup", command=startBackup)
    backupBtn.grid(row=3, column=0, padx=10, pady=20, sticky='e')
    # UI for debugging Section
    debug_button = tk.Button(backup_frame, text="Debug", command=startDebug)
    debug_button.grid(row=3, column=1, padx=10, pady=10, sticky='w')
    
    tk.Label(debug_frame, text="Debugging Section").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    debug_output = tk.Text(debug_frame, height=20, width=80)
    debug_output.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    
    debug_output.tag_configure('bold', font=('Helvetica', 10, 'bold'))
    
    debug_frame.grid_rowconfigure(1, weight=1)
    debug_frame.grid_columnconfigure(0, weight=1)
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
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



