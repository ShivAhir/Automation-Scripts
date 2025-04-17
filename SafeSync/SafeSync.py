import tkinter as tk
from tkinter import ttk
import threading
from Backend_Files.Backup import download, closeSSHConnection
from Backend_Files.Coredump import enable_coredump
from Backend_Files.DownloadLogs import download_logs
from Backend_Files.Overview import cardInfoD
from Backend_Files.Overview import failedServices
from Backend_Files.DetailDebug import detail_debug
from Backend_Files.Upload import uploadFiles
from Backend_Files.UILoadingWindow import show_loading_ui


def on_enter(event):
    event.widget.config(bg="#2A68A2", fg='black')


def on_leave(event):
    event.widget.config(bg="#1A5082", fg="white")


def create_ui(remotePaths):

    def getInfo():  # this is to get the device communication info
        deviceIP = deviceIPEntry.get()
        deviceUsername = deviceUsernameEntry.get()
        devicePassword = devicePasswordEntry.get()
        if not deviceIP or not deviceUsername or not devicePassword:
            loading_window = show_loading_ui(
                root=root, title="Error", msg="Please fill in all fields.", type='Error Message')
            return
        else:
            return deviceIP, deviceUsername, devicePassword

    def startBackup():
        info = getInfo()
        deviceIP, deviceUsername, devicePassword = info if info is not None else (
            None, None, None)
        if info:
            threading.Thread(target=download, args=(deviceIP, deviceUsername, devicePassword,
                             remotePaths, root)).start()

    def startUpload():
        info = getInfo()
        deviceIP, deviceUsername, devicePassword = info if info is not None else (
            None, None, None)
        if info:
            loadingLabel = tk.Label(
                auth_info_frame, text="Uploading, please wait...", fg="blue")
            loadingLabel.grid(row=5, column=0, columnspan=2, pady=10)
            threading.Thread(target=uploadFiles, args=(deviceIP, deviceUsername,
                             devicePassword, remotePaths, loadingLabel, root)).start()

    def startOverview():
        def process_overview():
            overview_output.config(state='normal')
            detail_debug_output.config(state='normal')
            if overview_frame.winfo_ismapped():
                overview_frame.pack_forget()
            else:
                overview_frame.pack(fill='both', expand=True)
            if getInfo() is None:
                return
            overview_output.delete(1.0, tk.END)
            detail_debug_output.delete(1.0, tk.END)
            if detail_debug_frame.winfo_ismapped():
                detail_debug_frame.pack_forget()
                detail_debug_output.delete(1.0, tk.END)

            debug_info = cardInfoD(getInfo(), root)
            if debug_info:
                separator = ttk.Separator(overview_frame, orient="horizontal")
                separator.grid(row=0, column=0, padx=30, sticky='nsew')
                tk.Label(overview_frame, text="Debugging Section",  font=('Lucida Sans', 10, 'bold')).grid(
                    row=0, column=0, padx=10, pady=(18, 3), sticky='nsew')
                overview_output.grid(row=1, column=0, padx=10,
                                     pady=10, sticky='nsew')
                formatDebugInfo(debug_info=debug_info)
                overview_output.config(state='disabled')
                separator_dw_btn.grid(
                    row=2, column=0, padx=30, sticky='nsew')
                dw_logs_button.grid(row=3, column=0, padx=30,
                                    pady=10, sticky='nsew')
        threading.Thread(target=process_overview).start()

    def formatDebugInfo(debug_info=None, res=None):
        # Debug - general information section
        separator = ttk.Separator(
            overview_frame, orient="horizontal")
        if debug_info:
            overview_output.insert(
                tk.END, "\n Card's General Information", ('bold', 'center'))
            overview_output.insert(
                tk.END, "\n-------------------------------------------------------------------- \n\n", ('bold', 'center'))
            for key, value in debug_info.items():
                overview_output.insert(tk.END, f"  {key}: ", 'bold')
                overview_output.insert(tk.END, f" {value}\n")
        if res:
            detail_debug_output.insert(
                tk.END, "\n Detailed Debug Information ", ('bold', 'center'))
            detail_debug_output.insert(
                tk.END, "\n-------------------------------------------------------------------- \n\n", ('bold', 'center'))
            if overview_output.get("1.0", "end-1c").strip() == "":
                tk.Label(overview_frame, text="Debugging Section",  font=('Chalkboard', 10, 'bold')).grid(
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
        if getInfo():
            def process_detail_debug():
                detail_debug_output.config(state='normal')
                cardInfoD(getInfo(), root)
                if detail_debug_frame.winfo_ismapped():
                    detail_debug_frame.pack_forget()
                else:
                    detail_debug_frame.pack(fill='both', expand=True)
                if getInfo() is None:
                    return
                detail_debug_output.delete(1.0, tk.END)
                detail_debug_info = detail_debug(getInfo(), root)[0]
                if detail_debug_info:
                    detail_debug_output.grid(
                        row=1, column=0, padx=(10, 0), pady=10, sticky='nsew')
                    scrollbar.grid(row=1, column=1, pady=10, sticky="ns")
                    detail_debug_output.config(yscrollcommand=scrollbar.set)
                    formatDebugInfo(res=detail_debug_info)
                    detail_debug_info = ''
                    detail_debug_output.config(state='disabled')
                    separator_dw_btn.grid(
                        row=2, column=0, padx=30, sticky='nsew')
                    dw_logs_button.grid(row=3, column=0, padx=30,
                                        pady=10, sticky='nsew')
            threading.Thread(target=process_detail_debug).start()

    def enable_coredumps():
        info = getInfo()
        deviceIP, deviceUsername, devicePassword = info if info is not None else (
            None, None, None)
        if info:
            enable_coredump(deviceIP, deviceUsername, devicePassword, root)

    def start_downloading_logs():
        overview = overview_output.get("1.0", "end-1c")
        detail_debug_res = detail_debug(getInfo(), root)[1]

        # detail_debug_res = detail_debug_output.get("1.0", "end-1c")
        download_logs(root, overview, detail_debug_res)

    root = tk.Tk()
    root.title("SafeSync")
    root.configure(bg="#3E3E3E")
    root.iconbitmap("assets\Icon\SafeSync.ico")
    root.option_add("*Frame.background", "#3E3E3E")  # Dark gray for frames

    root.option_add("*Title.background", "#3E3E3E")  # Match frame background
    root.option_add("*Title.foreground", "#FFFFFF")
    root.option_add("*Label.background", "#3E3E3E")  # Match frame background
    root.option_add("*Label.foreground", "#FFFFFF")  # White text for labels
    root.option_add("*Button.background", "#1A5082")  # Blue for buttons
    root.option_add("*Button.foreground", "#FFFFFF")  # White text for buttons
    root.option_add("*Separator.background", "#3E3E3E")
    root.option_add("*Separator.foreground", "#FFFFFF")
    # # Darker blue when hovered
    root.option_add("*Button.activebackground", "#357ABD")
    # # White text when hovered
    root.option_add("*Button.activeforeground", "#FFFFFF")

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

    overview_frame = tk.Frame(container)
    overview_frame.grid(row=5, rowspan=4, column=0,
                        columnspan=2, sticky='nsew')

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

    overview_frame.grid_rowconfigure(0, weight=1)
    overview_frame.grid_columnconfigure(0, weight=1)

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
        'Lucida Sans', 10, 'bold')).grid(row=1, column=0, padx=10, pady=10, sticky='nse')
    deviceIPEntry = tk.Entry(auth_info_frame, width=50)
    deviceIPEntry.grid(row=1, column=1, padx=5, pady=10, sticky='nsew')
    tk.Label(auth_info_frame, text="Device Username:", font=(
        'Lucida Sans', 10, 'bold')).grid(row=2, column=0, padx=10, pady=10, sticky='nse')
    deviceUsernameEntry = tk.Entry(auth_info_frame, width=50)
    deviceUsernameEntry.grid(row=2, column=1, padx=5, pady=10, sticky='nsew')
    tk.Label(auth_info_frame, text="Device Password:", font=(
        'Lucida Sans', 10, 'bold')).grid(row=3, column=0, padx=10, pady=10, sticky='nse')
    devicePasswordEntry = tk.Entry(auth_info_frame, width=50, show='*')
    devicePasswordEntry.grid(row=3, column=1, padx=5, pady=10, sticky='nsew')

    # UI for backup/upload Section
    backupBtn = tk.Button(actn_button_frame, text="Start Backup", font=(
        'Lucida Sans', 10, 'bold'), cursor="hand2", command=startBackup, width=25, height=2)
    backupBtn.grid(row=0, column=0, padx=(5, 11), pady=(9, 11))
    uploadBtn = tk.Button(actn_button_frame, text="Start Upload", font=(
        'Lucida Sans', 10, 'bold'), cursor="hand2", command=startUpload, width=25, height=2)
    uploadBtn.config(state="disabled")
    uploadBtn.grid(row=0, column=1, padx=(5, 10), pady=(9, 11))
    # UI for coredump section
    enable_coredumps_btn = tk.Button(coredump_button_frame, text="Enable Coredumps", font=(
        'Lucida Sans', 10, 'bold'), cursor="hand2",  command=enable_coredumps, width=25, height=2)
    enable_coredumps_btn.grid(row=0, column=0, padx=(5, 11), pady=5)
    extract_coredumps_btn = tk.Button(coredump_button_frame, text="Extract Coredumps", font=(
        'Lucida Sans', 10, 'bold'), cursor="hand2",  command=enable_coredumps, width=25, height=2)
    extract_coredumps_btn.grid(row=0, column=1, padx=(5, 10), pady=5)
    extract_coredumps_btn.config(state="disabled")
    # UI for debugging Section
    overview_btn = tk.Button(debug_button_frame, text="Overview", font=(
        'Lucida Sans', 10, 'bold'), cursor="hand2",  command=startOverview, height=2)
    overview_btn.grid(row=0, column=0, columnspan=2,
                      padx=40, pady=15, sticky='nsew')
    detailed_debug_btn = tk.Button(debug_button_frame, text="Detailed Debug", font=(
        'Lucida Sans', 10, 'bold'), cursor="hand2",  command=startDetailDebug, height=2)
    detailed_debug_btn.grid(
        row=0, column=2, columnspan=2, padx=40, pady=15, sticky='nsew')

    separator_dw_btn = ttk.Separator(
        detail_debug_frame, orient="horizontal")
    dw_logs_button = tk.Button(
        detail_debug_frame, text="Download Logs", font=(
            'Lucida Sans', 10, 'bold'), cursor="hand2",  command=start_downloading_logs, height=2)
    backupBtn.bind("<Enter>", on_enter)
    backupBtn.bind("<Leave>", on_leave)
    uploadBtn.bind("<Enter>", on_enter)
    uploadBtn.bind("<Leave>", on_leave)

    enable_coredumps_btn.bind("<Enter>", on_enter)
    enable_coredumps_btn.bind("<Leave>", on_leave)
    extract_coredumps_btn.bind("<Enter>", on_enter)
    extract_coredumps_btn.bind("<Leave>", on_leave)
    overview_btn.bind("<Enter>", on_enter)
    overview_btn.bind("<Leave>", on_leave)
    detailed_debug_btn.bind("<Enter>", on_enter)
    detailed_debug_btn.bind("<Leave>", on_leave)
    dw_logs_button.bind("<Enter>", on_enter)
    dw_logs_button.bind("<Leave>", on_leave)
    overview_output = tk.Text(
        overview_frame, height=16, width=100, wrap='word')
    overview_output.tag_configure('bold', font=('Helvetica', 10, 'bold'))
    overview_output.tag_configure('center', justify='center')

    detail_debug_output = tk.Text(
        detail_debug_frame, height=15, width=100, wrap='word')
    detail_debug_output.tag_configure('bold', font=('Helvetica', 10, 'bold'))
    detail_debug_output.tag_configure('center', justify='center')
    scrollbar = tk.Scrollbar(
        detail_debug_frame, command=detail_debug_output.yview)

    overview_frame.grid_rowconfigure(1, weight=1)
    overview_frame.grid_columnconfigure(0, weight=1)

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
    create_ui(remotePaths)
    closeSSHConnection()


if __name__ == "__main__":
    main()
