from constrant import *
from pynfc_lib.pc_get_info import *
from pynfc_lib.pc_test_info import *
import threading
import subprocess
import sys
import os

py_dir_result_folder=PY_DIR_ROOT+sys.argv[1]+"/"
os.system("mkdir -p "+py_dir_result_folder)
py_dir_result_csv=py_dir_result_folder+"_summary.csv"
py_dir_result_text=py_dir_result_folder+"_summary.txt"
py_dir_result_final=py_dir_result_folder+sys.argv[1]+"_final.txt"
py_dir_info_ont=py_dir_result_folder+"_info.txt"
time_test=int(float(sys.argv[2])*3600)
brc_ont_save_info(dir=py_dir_info_ont)
file=open(py_dir_result_text,"a+")
write_csv_by_column(dir_file=py_dir_result_csv, col_0='[<SUMMARY>]',col_1='Time', \
                    col_2='ToC BOB', col_3='Valid ToC BOB', \
                    col_4='Rx Optical(dBm)', col_5='Valid Rx Optical', \
                    col_6='Tx Optical(dBm)', col_7='Valid Tx Optical', \
                    col_8='{Bias optical (uA)}', col_9='{Voltage optical (mV)}')
try:
    i=0
    time_start=time.time()
    while(int(time.time()-time_start)<time_test):
        p=subprocess.getoutput("date +%x_%X")
        thoi_gian.append(p)
        file.write("\n***###***=>Check lan thu: "+str(i+1)+"\n"+p+"\n")
        print("\n\n[*********##**Thoi diem thu ",i+1, "**##***********] ",p,"\n")
        print("____Step 1: Check Optical Info")
        file.write("____Step 1: Check Optical Info"+"\n")
        brc_test_info_optical(file,\
                          result_rx_optical,valid_result_rx_optical,\
                          result_tx_optical,valid_result_tx_optical,\
                          result_temperature_optical,valid_result_temperature_optical,\
                          result_bias_optical,result_vol_optical,check=0)
        file.write("____Step 2: Validate parameters"+"\n")
        list_valid_lan=get_list_valid_lan(i)
        valid_parameters.append(get_max_parameters(list_valid_lan))
        list_data_lan=get_list_data_lan(i)
        write_list_to_csv(py_dir_result_csv, list_data_lan)
        print("\n\n=>Summary____: ",valid_parameters[i])
        time.sleep(1)
        i=i+1
        os.system("clear")
    file.close()
    valid_summary(py_dir_result_final,valid_parameters)
except Exception as name_except:
    file=open(py_dir_result_text,"w+")
    file.write(LEVEL[3]+"\n"+name_except)
    file.close


