import serial
from time import strftime, gmtime
import subprocess  

# Use hackrf_transfer to log data collected by the HackRF
op_freq_1 = str(100000000) # 100 MHz
op_freq_2 = str(400000000) # 400 MHz
data_dir = "/home/pi/Desktop/hackrf_data"
num_samples = str(1000)
    
# Store the raw IQ in a timestamped data file
stamp = strftime('%Y-%m-%d-%H_%M_%S', gmtime())
cmd = "hackrf_transfer -f " + op_freq_1 + " -n " + num_samples + " -r" + data_dir + "/LOG_IQ_" + op_freq_1 + "_" + stamp
run_cmd = subprocess.call(cmd, shell=True)
    
    
stamp = strftime('%Y-%m-%d-%H_%M_%S', gmtime())
cmd = "hackrf_transfer -f " + op_freq_2 + " -n " + num_samples + " -r" + data_dir + "/LOG_IQ_" + op_freq_2 + "_" + stamp
run_cmd = subprocess.call(cmd, shell=True)
