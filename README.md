# PktmonNetworkTrace
> PktmonNetworkTrace is used to capture all tcp-ip requests from specific process in the current computer.
> The repository is based on [pktmon](https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon).

# Usage

## Prework
1. Make sure there is`ktmon.exe` on your windows;
2. Both two methods program should be ran in administrator privilege;

## cmd

Example:

1. `-p`: Name of target process
2. `-o`: Path of output file
3. `-v`: verbose

```shelll
python pktmon.py -p python.exe -o D:\desktop\data.txt -v
```

The format of `data.txt` is:
1. `local=`: local ip
2. `remote=`: remote ip
3. `pid=`: PID of target process

```
2023/04/06-12:34:25 local=127.0.0.1:65432 remote=127.0.0.1:62365 pid=14716
2023/04/06-12:34:25 local=127.0.0.1:65432 remote=127.0.0.1:62366 pid=14716
2023/04/06-12:34:25 local=127.0.0.1:65432 remote=127.0.0.1:62368 pid=14716
2023/04/06-12:34:25 local=127.0.0.1:65432 remote=127.0.0.1:62369 pid=14716
```

## intergration
`main.py`:
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