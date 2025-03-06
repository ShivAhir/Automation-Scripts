import tkinter as tk
from tkinter import messagebox
import os
import threading
from BackEnd_SafeSync import downloadFolder, establishConnection, closeSSHConnection

def create_ui(remotePaths, localPath):
    def start_download():
        deviceIP = deviceIPEntry.get()
        deviceUsername = deviceUsernameEntry.get()
        devicePassword = devicePasswordEntry.get()
        if not deviceIP or not deviceUsername or not devicePassword:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
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

        # Start download in a separate thread
        threading.Thread(target=download).start()
         
        # def download():
        #     establishConnection(deviceIP, deviceUsername, devicePassword)
        #     for remotePath in remotePaths:
        #         success = downloadFolder(remotePath, localPath)
        #         if not success:
        #             messagebox.showerror("Error", "Failed to download folder.")
        #     messagebox.showinfo("Success", f"Successfully downloaded folder to {localPath}")
        #     closeSSHConnection()
        #     loadingLabel.destroy()
        # threading.Thread(target=download).start()
        
    def show_frame(frame):
        frame.tkraise()
        
    root = tk.Tk()
    root.title("SafeSync")
    
    # the nav bar
    nav_frame = tk.Frame(root)
    nav_frame.pack(side='top', pady=10)
    backup_button = tk.Button(nav_frame, text="Backup", command=lambda: show_frame(backup_frame))
    backup_button.pack(side='left', padx=10)
    debug_button = tk.Button(nav_frame, text="Debug", command=lambda: show_frame(debug_frame))
    debug_button.pack(side='left', padx=10)
    
    container = tk.Frame(root)
    container.pack(expand=True, fill='both')
    
    backup_frame = tk.Frame(container)
    debug_frame = tk.Frame(container)
    
    for frame in (backup_frame, debug_frame):
        frame.grid(row=0, column=0, sticky='nsew')
    
    
    # UI for backup tab
    tk.Label(backup_frame, text="Device IP Address:").grid(row=0, column=0, padx=10, pady=10)
    deviceIPEntry = tk.Entry(backup_frame, width=50)
    deviceIPEntry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(backup_frame, text="Device Username:").grid(row=1, column=0, padx=10, pady=10)
    deviceUsernameEntry = tk.Entry(backup_frame, width=50)
    deviceUsernameEntry.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Label(backup_frame, text="Device Password:").grid(row=2, column=0, padx=10, pady=10)
    devicePasswordEntry = tk.Entry(backup_frame, width=50, show='*')
    devicePasswordEntry.grid(row=2, column=1, padx=10, pady=10)
    
    download_button = tk.Button(backup_frame, text="Start Download", command=start_download)
    download_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    # UI for debugging tab
    tk.Label(debug_frame, text="Debugging Section").grid(row=0, column=0, padx=10, pady=10)
    debug_output = tk.Text(debug_frame, height=20, width=80)
    debug_output.grid(row=1, column=0, padx=10, pady=10)
    
    show_frame(backup_frame)
    
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
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



