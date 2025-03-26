from tkinter import messagebox
from Backend_Files.Backup import closeSSHConnection, downloadFolder
from Backend_Files.Connection import establishConnection



def uploadFiles(deviceIP, deviceUsername, devicePassword, remotePaths, localPath, loadingLabel):
    try:
        print("Establishing connection...")
        establishConnection(deviceIP, deviceUsername, devicePassword)
        print("Connection established.")
        flag = True
        for remotePath in remotePaths:
            print(f"Downloading folder: {remotePath}")
            success = downloadFolder(remotePath, localPath)
            if not success:
                flag == False
                print(f"Failed to download folder: {remotePath}")
                messagebox.showerror("Error", f"Failed to download folder: {remotePath}")
                break
        if flag:
            print(f"Successfully downloaded folders to {localPath}")
            messagebox.showinfo("Success", f"Successfully downloaded folders to {localPath}")
            
    except Exception as e:
        flag == False
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        print("Closing connection...")
        closeSSHConnection()
        print("Connection closed.")
        loadingLabel.destroy()