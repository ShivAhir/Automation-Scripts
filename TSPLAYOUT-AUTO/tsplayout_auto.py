import subprocess
import signal
import sys

# This script basically runs streams using tsplayout
# List of streams that is in /udata/home/mvx location
streams = [
    "/opt/evertz/bin/tsplayout /udata/home/mvx/420.ts udp://239.179.50.1:1234?miface=eno1",
    "/opt/evertz/bin/tsplayout /udata/home/mvx/DOne_15M_H264HD_12M_AC3.ts udp://239.179.50.2:1234?miface=eno1",
    "/opt/evertz/bin/tsplayout /udata/home/mvx/420.ts udp://239.179.50.3:1234?miface=eno1"
]

processes = []

def signal_handler(sig, frame):
    print("Terminating all streams...")
    for process in processes:
        process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Starting all streams
for stream in streams:
    print(f"Starting stream: {stream}")
    process = subprocess.Popen(stream, shell=True)
    processes.append(process)

for process in processes:
    process.wait()
