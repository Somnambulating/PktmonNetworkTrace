import signal
import sys
import os
import subprocess
import threading
import time
import argparse
import re
import psutil
import time

TARGET_PROCESS_NAME = 0
IPv4_REGEX_PATTERN = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}"
PID_TAG = "PID = "
LOCAL_TAG = "local="
REMOTE_TAG = "remote="
UNKNOWN_CONNECTION_TAG = "unknown"
DATA_DIR_PATH = "./data/"

class PktmonClient():
    def __init__(self, cmd, target_process, output_file = "pktmon_output") -> None:
        self.cmd_ = cmd
        self.target_process_name = target_process
        self.target_process_pids = []
        self.output_file_path_ = DATA_DIR_PATH + output_file + "_" + self.target_process_name + "_" + str(int(time.time()))  + ".txt"
        self.output_file_handler_ = None
        self.ip_dict_ = {}

    def write_file(self):
        lines = []
        for item in self.ip_dict_.items():
            line = ""
            print(item)
            
            for pid in self.target_process_pids:
                # print("pid: {0} items[1]: {1}".format(pid, item[1]))
                if pid == item[1]:
                    line = "local=" + item[0][0] + " remote=" + item[0][1] + " pid=" + item[1]
                    line += "\n"
                    lines.append(line)
                    break

        self.output_file_handler_.writelines(lines)
        self.output_file_handler_.flush()

    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        self.write_file()
        self.output_file_handler_.close()
        sys.exit(0)
    
    def init(self):
        global PID_TAG

        try:
            self.output_file_handler_ = open(self.output_file_path_ , "w+")
        except Exception as e:
            print("Error with open")
            exit(-1)
        
        self.target_process_pids = self.get_pid_by_name(self.target_process_name)

        signal.signal(signal.SIGINT, self.signal_handler)

    def get_pid_by_name(self, process_name):
        pids = []
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pids.append(str(proc.pid))
        
        return pids

    def parser_ip_address(self, line):
        global IPv4_REGEX_PATTERN
        global LOCAL_TAG
        global REMOTE_TAG
        global PID_TAG
        global UNKNOWN_CONNECTION_TAG

        local_tag_index = line.find(LOCAL_TAG)
        remote_tag_index = line.find(REMOTE_TAG)
        pid_tag_index = line.find(PID_TAG)

        if local_tag_index == -1 and remote_tag_index == -1:
            return None
        
        # get local address and remote address
        info = re.findall(IPv4_REGEX_PATTERN, line)

        if len(info) == 1:
            print("Error: {0}".format(line))
            return None

        if len(info) == 0:
            print(line)
            return None

        if pid_tag_index == -1:
            info.append(UNKNOWN_CONNECTION_TAG)
            return info
        
        pid = line[pid_tag_index + len(PID_TAG): -4]

        info.append(pid)
        return info


    def loop(self):

        proc = subprocess.Popen(self.cmd_,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        
        time.sleep(2)
        while True:

            line = proc.stdout.readline().decode()
            # print(line)
            
            info = self.parser_ip_address(line)
            if info != None:
                try:
                    print("info:")
                    print(info)
                    self.ip_dict_.update({(info[0], info[1]): info[2]})
                except Exception as e:
                    print("Error!")
                    print(info)
                    exit(-1)

def parse_argument():
    global TARGET_PROCESS_NAME

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, required=True, help='Name of target process')
    args = parser.parse_args()

    TARGET_PROCESS_NAME = args.p

def main():
    # TODO: check the exists of pktmon
    parse_argument()
    cmd = "pktmon start --trace -p Microsoft-Windows-TCPIP -p Microsoft-Windows-NDIS -m real-time"
    pktmonClient = PktmonClient(cmd, TARGET_PROCESS_NAME)
    pktmonClient.init()
    pktmonClient.loop()

if __name__ == "__main__":
    main()