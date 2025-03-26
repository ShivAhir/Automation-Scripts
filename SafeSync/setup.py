from cx_Freeze import setup, Executable # type: ignore
import sys

build_exe_options = {
    "packages": ["os", "tkinter", "paramiko", "scp"],
    "excludes": [],
    "include_files": ['SafeSync/assets/Icon/SafeSync.ico']
}
base = None # to hide the console
if sys.platform == 'win32':
    base = "Win32GUI"

setup(
    name="SafeSync",
    version="1.0",
    description="SafeSync Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("SafeSync.py", base=base)],
)
