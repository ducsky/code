from constrant import *
from pc_get_info import *
from pc_test_info import *
import threading
import subprocess
import sys
import os

py_dir_result_folder=PY_DIR_ROOT+sys.argv[1]+"/"
os.system("mkdir -p "+py_dir_result_folder)
py_dir_result_csv=py_dir_result_folder+"_summary.csv"
py_dir_result_text=py_dir_result_folder+"_summary.txt"
py_dir_result_final=PY_DIR_ROOT+"_final.txt"
py_dir_info_ont=py_dir_result_folder+"_info.txt"
# time_chu_ky=sys.argv[2]
brc_ont_save_info(dir=py_dir_info_ont)
time_start=time.time()
i=0
while(i<3):
# while ((time.time()-time_start)<(25*HOUR)):
    file=open(py_dir_result_text,"a+")
    time_start_2=time.time()
    check_net=0
    p=subprocess.getoutput("date +%x_%X")
    thoi_gian.append(p)
    file.write("\n***###***=>Check lan thu: "+str(i+1)+"\n"+p+"\n")
    print("\n\n[**********##**Thoi diem thu ",i+1, "**##************]")
    print(p)
    print("____Step 1: Check Ping IP Internet and IP Iperf Server")
    file.write("____Step 1: Check ping Internet and Iperf Server"+"\n")
    t1=threading.Thread(target=test_ping, \
                        args=(file, result_ping, valid_result_ping, IF_LAN_CARD,))
    t2=threading.Thread(target=brc_test_info_optical, \
                        args=(file, result_rx_optical,valid_result_rx_optical,\
                      result_tx_optical,valid_result_tx_optical,\
                      result_temperature_optical,valid_result_temperature_optical,\
                      result_bias_optical,result_vol_optical,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    file.write("____Step 8: Validate parameters"+"\n")
    test_parameters(file, thoi_gian, valid_parameters)
    print("\n\n=>Summary____: ",valid_parameters[i])
    print("<======+++=====>")
    print("DONE in :",int(time.time()-time_start_2),"(s)")
    print("===========================================")
    file.close()
    write_csv_2(py_dir_result_csv, thoi_gian)
    time.sleep(1)
#     delta_time=int(0.5+time_chu_ky-time.time()+time_start_2)
#     if delta_time>0:
#         print("------>Lan tiep theo se tiep tuc sau: ",delta_time,"(s)")
#         time.sleep(delta_time)
    i=i+1
    os.system("clear")
valid_summary(py_dir_result_final,valid_parameters)

