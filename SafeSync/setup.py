from cx_Freeze import setup, Executable # type: ignore
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "tkinter", "paramiko", "scp"],
    "excludes": [],
    "include_files": []
}
base = None # to hide the console
if sys.platform == 'win32':
    base = "Win32GUI"

setup(
    name="SafeSync-trial",
    version="1.0",
    description="SafeSync Application-trial",
    options={"build_exe": build_exe_options},
    executables=[Executable("trial.py", base=base)],
)
