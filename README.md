# PktmonNetworkTrace
> PktmonNetworkTrace is used to capture all tcp-ip requests from specific process in the current computer.
> The repository is based on [pktmon](https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon).

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

## TODO
To capture the requests and responses of UDP.