from cx_Freeze import setup, Executable # type: ignore
import sys

build_exe_options = {
    "packages": ["os", "tkinter", "paramiko", "scp"],
    "excludes": [],
    "include_files": ['assets\Icon\SafeSync.ico']
}
base = None # to hide the console
if sys.platform == 'win32':
    base = "Win32GUI"
executables = [
    Executable(
        script = "SafeSync.py",
        base=base,
        icon='assets\Icon\SafeSync.ico'
    )
]


setup(
    name="SafeSync",
    version="1.0",
    description="SafeSync Application",
    options={"build_exe": build_exe_options},
    executables=executables,
)