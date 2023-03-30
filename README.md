# PktmonCheck
> PktmonCheck is used to capture all tcp-ip requests from one specific process, and all udp requests from the current computer.
> The tool is based on [pktmon](https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon).

# Usage

```python
from pktmon_monitor import PktmonMonitor
import time

def main():
    # Monitor the target process
    pktmonClient = PktmonMonitor("python.exe")
    
    # Launch the monitor
    pktmonClient.start()

    time.sleep(10)

    # Stop the monitor
    pktmonClient.stop()

if __name__ == "__main__":
    main()
```