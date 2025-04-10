from pydoc import text
import tkinter as tk
from tkinter import messagebox, ttk
import os
import threading
from Backend_Files.Backup import download, closeSSHConnection
from Backend_Files.Coredump import enable_coredump
from Backend_Files.Overview import cardInfoD, readMultiLines
from Backend_Files.Overview import failedServices
from Backend_Files.DetailDebug import detail_debug
from Backend_Files.Upload import uploadFiles

overview_flag = True


def create_ui(remotePaths, localPath):

    def getInfo():  # this is to get the device communication info
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
        deviceIP, deviceUsername, devicePassword = info if info is not None else (
            None, None, None)
        if info:
            loadingWindow = tk.Toplevel(root)
            loadingWindow.title("Processing")
            loadingWindow.iconbitmap("assets\Icon\SafeSync.ico")
            loadingWindow.geometry("450x150")
            loadingWindow.transient(root)
            loadingWindow.grab_set()

            # Center the loading window within the main window
            root_x = root.winfo_rootx()
            root_y = root.winfo_rooty()
            root_width = root.winfo_width()
            root_height = root.winfo_height()
            loading_x = root_x + (root_width // 2) - 150
            loading_y = root_y + (root_height // 2) - 50
            loadingWindow.geometry(f"+{loading_x}+{loading_y}")

            loadingLabel = tk.Label(
                loadingWindow, text="Downloading, please wait...", fg="blue")
            loadingLabel.pack(expand=True, padx=20, pady=20)

            threading.Thread(target=download, args=(deviceIP, deviceUsername, devicePassword,
                             remotePaths, localPath, loadingWindow, loadingLabel, root)).start()

    def startUpload():
        info = getInfo()
        deviceIP, deviceUsername, devicePassword = info if info is not None else (
            None, None, None)
        if info:
            loadingLabel = tk.Label(
                auth_info_frame, text="Uploading, please wait...", fg="blue")
            loadingLabel.grid(row=5, column=0, columnspan=2, pady=10)
            threading.Thread(target=uploadFiles, args=(deviceIP, deviceUsername,
                             devicePassword, remotePaths, localPath, loadingLabel, root)).start()

    def startOverview():
        global overview_flag
        overview_flag = True
        if debug_frame.winfo_ismapped():
            debug_frame.pack_forget()
        else:
            debug_frame.pack(fill='both', expand=True)
        if getInfo() is None:
            return
        debug_output.delete(1.0, tk.END)
        debug_info = cardInfoD(getInfo(), root)
        if debug_info:
            separator = ttk.Separator(debug_frame, orient="horizontal")
            separator.grid(row=0, column=0, padx=30, sticky='nsew')
            tk.Label(debug_frame, text="Debugging Section",  font=('Chalkboard', 10, 'bold')).grid(
                row=0, column=0, padx=10, pady=(18, 3), sticky='nsew')
            debug_output.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
            formatDebugInfo(debug_info=debug_info)
            debug_output.config(state='disabled')

        closeSSHConnection()

    def formatDebugInfo(debug_info=None, res=None):
        # Debug - general information section
        separator = ttk.Separator(
            debug_frame, orient="horizontal")
        if debug_info:
            debug_output.insert(
                tk.END, "\n Card's General Information", ('bold', 'center'))
            debug_output.insert(
                tk.END, "\n-------------------------------------------------------------------- \n\n", ('bold', 'center'))
            for key, value in debug_info.items():
                debug_output.insert(tk.END, f"  {key}: ", 'bold')
                debug_output.insert(tk.END, f"{value}\n")
        if res:
            detail_debug_output.insert(
                tk.END, "\n Detailed Debug Information ", ('bold', 'center'))
            detail_debug_output.insert(
                tk.END, "\n-------------------------------------------------------------------- \n\n", ('bold', 'center'))
            if debug_output.get("1.0", "end-1c").strip() == "":
                tk.Label(debug_frame, text="Debugging Section",  font=('Chalkboard', 10, 'bold')).grid(
                    row=0, column=0, padx=10, pady=(18, 3), sticky='nsew')
                separator.grid(row=0, column=0, padx=30, sticky='nsew')
                detail_debug_output.insert(
                    tk.END, f" Failed Services: ", 'bold')
                detail_debug_output.insert(
                    tk.END, f"{', '.join(failedServices)} \n\n")
            for service, output in res.items():
                detail_debug_output.insert(tk.END, f"  {service}: \n", 'bold')
                detail_debug_output.insert(tk.END, f"{output}\n")
                detail_debug_output.insert(
                    tk.END, '  ----------------------------------------------------------------------------------------------------\n')

    def startDetailDebug():
        cardInfoD(getInfo(), root)
        if detail_debug_frame.winfo_ismapped():
            detail_debug_frame.pack_forget()
        else:
            detail_debug_frame.pack(fill='both', expand=True)
        if getInfo() is None:
            return
        detail_debug_output.delete(1.0, tk.END)
        detail_debug_info = detail_debug(getInfo(), root)
        if detail_debug_info:
            detail_debug_output.grid(
                row=1, column=0, padx=10, pady=10, sticky='nsew')
            formatDebugInfo(res=detail_debug_info)
            detail_debug_output.config(state='disabled')
            separator = ttk.Separator(detail_debug_frame, orient="horizontal")
            separator.grid(row=2, column=0, padx=30, sticky='nsew')
            dw_logs_button.grid(row=3, column=0, padx=30,
                                pady=10, sticky='nsew')

    def enable_coredumps():
        enable_coredump(getInfo(), root)

    root = tk.Tk()
    root.title("SafeSync")
    root.iconbitmap("assets\Icon\SafeSync.ico")

    container = tk.Frame(root)
    container.grid(row=0, column=0, sticky='nsew')

    contact_info_frame = tk.Frame(container)
    contact_info_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

    auth_info_frame = tk.Frame(container)
    auth_info_frame.grid(row=1, rowspan=3, column=0, sticky='nsew')

    actn_button_frame = tk.Frame(container)
    actn_button_frame.grid(row=1, column=1, sticky='nsew')

    coredump_button_frame = tk.Frame(container)
    coredump_button_frame.grid(row=2, column=1, sticky='nsew')

    debug_button_frame = tk.Frame(container)
    debug_button_frame.grid(row=4, column=0, columnspan=2, sticky='nsew')

    debug_frame = tk.Frame(container)
    debug_frame.grid(row=5, rowspan=4, column=0, columnspan=2, sticky='nsew')

    detail_debug_frame = tk.Frame(container)
    detail_debug_frame.grid(row=10, rowspan=4, column=0,
                            columnspan=2, sticky='nsew')

    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)
    container.grid_rowconfigure(2, weight=1)
    container.grid_rowconfigure(3, weight=1)
    container.grid_rowconfigure(4, weight=1)
    container.grid_rowconfigure(5, weight=1)
    container.grid_rowconfigure(6, weight=1)
    container.grid_rowconfigure(7, weight=1)
    container.grid_rowconfigure(8, weight=1)
    container.grid_rowconfigure(9, weight=1)
    container.grid_rowconfigure(10, weight=1)

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    contact_info_frame.grid_rowconfigure(0, weight=1)
    contact_info_frame.grid_columnconfigure(0, weight=1)

    auth_info_frame.grid_rowconfigure(0, weight=1)
    auth_info_frame.grid_rowconfigure(1, weight=1)
    auth_info_frame.grid_rowconfigure(2, weight=1)
    auth_info_frame.grid_rowconfigure(3, weight=1)
    auth_info_frame.grid_columnconfigure(0, weight=1)
    auth_info_frame.grid_columnconfigure(1, weight=1)
    auth_info_frame.grid_columnconfigure(2, weight=1)

    debug_frame.grid_rowconfigure(0, weight=1)
    debug_frame.grid_columnconfigure(0, weight=1)

    detail_debug_frame.grid_rowconfigure(0, weight=1)
    detail_debug_frame.grid_rowconfigure(1, weight=1)
    detail_debug_frame.grid_columnconfigure(0, weight=1)

    actn_button_frame.grid_rowconfigure(0, weight=1)
    actn_button_frame.grid_columnconfigure(0, weight=1)
    actn_button_frame.grid_columnconfigure(1, weight=1)
    actn_button_frame.grid_columnconfigure(2, weight=1)

    debug_button_frame.grid_rowconfigure(0, weight=1)
    debug_button_frame.grid_columnconfigure(0, weight=1)
    debug_button_frame.grid_columnconfigure(1, weight=1)
    debug_button_frame.grid_columnconfigure(2, weight=1)
    debug_button_frame.grid_columnconfigure(3, weight=1)

    coredump_button_frame.grid_rowconfigure(0, weight=1)
    coredump_button_frame.grid_columnconfigure(0, weight=1)
    coredump_button_frame.grid_columnconfigure(1, weight=1)

    tk.Label(contact_info_frame, text="                  Contact Shiv Ahir if you have any questions or concerns                  ", font=(
        'Lucida Console', 9)).grid(row=0, column=0, pady=10, sticky='nsew')

    tk.Label(auth_info_frame, text="Device IP Address:", font=(
        'Chalkboard', 10, 'bold')).grid(row=1, column=0, padx=10, pady=10, sticky='nse')
    deviceIPEntry = tk.Entry(auth_info_frame, width=50)
    deviceIPEntry.grid(row=1, column=1, padx=5, pady=10, sticky='nsew')
    tk.Label(auth_info_frame, text="Device Username:", font=(
        'Chalkboard', 10, 'bold')).grid(row=2, column=0, padx=10, pady=10, sticky='nse')
    deviceUsernameEntry = tk.Entry(auth_info_frame, width=50)
    deviceUsernameEntry.grid(row=2, column=1, padx=5, pady=10, sticky='nsew')
    tk.Label(auth_info_frame, text="Device Password:", font=(
        'Chalkboard', 10, 'bold')).grid(row=3, column=0, padx=10, pady=10, sticky='nse')
    devicePasswordEntry = tk.Entry(auth_info_frame, width=50, show='*')
    devicePasswordEntry.grid(row=3, column=1, padx=5, pady=10, sticky='nsew')

    # UI for backup/upload Section
    backupBtn = tk.Button(actn_button_frame, text="Start Backup", font=(
        'Chalkboard', 10), command=startBackup, width=25, height=2)
    backupBtn.grid(row=0, column=0, padx=5, pady=5)
    uploadBtn = tk.Button(actn_button_frame, text="Start Upload", font=(
        'Chalkboard', 10), command=startUpload, width=25, height=2)
    uploadBtn.grid(row=0, column=1, padx=5, pady=5)
    # UI for coredump section
    enable_coredumps_button = tk.Button(coredump_button_frame, text="Enable Coredumps", font=(
        'Chalkboard', 10), command=enable_coredumps, width=25, height=2)
    enable_coredumps_button.grid(row=0, column=0, padx=5, pady=5)
    dump_coredumps_button = tk.Button(coredump_button_frame, text="Extract Coredumps", font=(
        'Chalkboard', 10), command=enable_coredumps, width=25, height=2)
    dump_coredumps_button.grid(row=0, column=1, padx=5, pady=5)
    # UI for debugging Section
    overview_button = tk.Button(debug_button_frame, text="Overview", font=(
        'Chalkboard', 10), command=startOverview, height=2)
    overview_button.grid(row=0, column=0, columnspan=2,
                         padx=40, pady=15, sticky='nsew')
    detailed_debug_button = tk.Button(debug_button_frame, text="Detailed Debug", font=(
        'Chalkboard', 10), command=startDetailDebug, height=2)
    detailed_debug_button.grid(
        row=0, column=2, columnspan=2, padx=40, pady=15, sticky='nsew')

    dw_logs_button = tk.Button(
        detail_debug_frame, text="Download Logs", font=(
            'Chalkboard', 10), command=startDetailDebug, height=2)

    debug_output = tk.Text(debug_frame, height=15, width=100, wrap='word')
    debug_output.tag_configure('bold', font=('Helvetica', 10, 'bold'))
    debug_output.tag_configure('center', justify='center')

    detail_debug_output = tk.Text(
        detail_debug_frame, height=15, width=100, wrap='word')
    detail_debug_output.tag_configure('bold', font=('Helvetica', 10, 'bold'))
    detail_debug_output.tag_configure('center', justify='center')

    debug_frame.grid_rowconfigure(1, weight=1)
    debug_frame.grid_columnconfigure(0, weight=1)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    deviceIPEntry.focus_set()
    root.resizable(False, False)
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
