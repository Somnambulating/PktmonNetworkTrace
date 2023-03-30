from pktmon_monitor import PktmonMonitor
import time

def main():
    pktmonClient = PktmonMonitor("python.exe")
    pktmonClient.start()
    
    time.sleep(10)
    pktmonClient.stop()

if __name__ == "__main__":
    main()