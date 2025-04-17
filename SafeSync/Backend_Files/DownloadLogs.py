from tkinter import filedialog
from Backend_Files.UILoadingWindow import show_loading_ui
from Backend_Files.logger_config import logger


def download_logs(root, overview=None, detail_debug_res=None):
    logger.info(
        "Attempting to download the logs captured on overview and detail debug")

    if overview or detail_debug_res != None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"),
                       ("All Files", "*.*")],
            title="Save File"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(overview) if overview else None
                file.write(
                    "\n\n\n Detailed Debug Information \n-------------------------------------------------------------------- \n\n",)
                file.write(detail_debug_res)
            show_loading_ui(
                root=root, title="Success", msg=f"Logs file has been saved to {file_path}", type='Success Message')
            logger.info("Logs file has been saved to {file_path}")
            print(f"File saved to {file_path}")
