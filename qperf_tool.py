import os
import time
import json
import sys
import subprocess
from subprocess import run
from qperf_parser import qparser


def qperf(ip_address, set_time, connection, interval):
    
    cmd='qperf'
    input_params='-t '+set_time+' -vv '+ip_address+' '+connection+'_bw '+connection+'_lat'
    output=''
    flag_udp_bw=0
    while(True):
        try:
            if flag_udp_bw==0:
                output=output+(subprocess.getoutput(cmd+' '+input_params))
                flag_udp_bw=1
            else:
                output=output+'udp_bw:\n'+(subprocess.getoutput(cmd+' '+input_params))                
            time.sleep(int(interval))
        except KeyboardInterrupt:   
            qparser(output)
            sys.exit()

if __name__ == '__main__': 

	with open('qperf_tool_config.json','r') as f:
        
		f_data=json.load(f)
		ip_address=f_data["ip_address"]
		set_time=f_data["set_time"]
		connection=f_data["connection_type"]
		interval=f_data["interval_between_commands"]

	qperf(ip_address, set_time, connection, interval) 
