from constrant import *
from math import *
import os 
import subprocess
import time
import getpass
import telnetlib
import csv
import smtplib
import ssl
import numpy
###
def brc_get_info_optical(ip_ont=IP_ONT):
    "get info of module Optical ONT, return Rx, Tx and Temp agruments"
    p=subprocess.getoutput("expect "+PY_DIR_SHELL+"040BRC_shell/info_optical.sh "+ip_ont)
    p1=p.split('\n')
    index_rx_tx=[]
    rx_tx=[]
    index_temp=[]
    temp=[]
    index_bias=[]
    bias=[]
    index_vol=[]
    vol=[]
    for i in range(len(p1)):
        if 'dBm' in p1[i]:
            index_rx_tx.append(i)
            if len(index_rx_tx)==2:
                break
    for i in range(len(p1)):
        if 'Temperature' in p1[i]:
            index_temp.append(i)
            if len(index_rx_tx)==1:
                break
    for i in range(len(p1)):
        if 'Tx Bias' in p1[i]:
            index_bias.append(i)
            if len(index_rx_tx)==1:
                break
    for i in range(len(p1)):
        if 'Voltage' in p1[i]:
            index_vol.append(i)
            if len(index_rx_tx)==1:
                break 
    try:
        rx=p1[index_rx_tx[0]].replace(" ", "")
        rx=rx.replace("=", "")
        rx=round(float(rx.replace("dBm", "")),2)
        rx_tx.append(rx)
        tx=p1[index_rx_tx[1]].replace(" ", "")
        tx=tx.replace("=", "")
        tx=round(float(tx.replace("dBm", "")),2)
        rx_tx.append(tx)
    except:
        rx_tx.append(0)
        rx_tx.append(0)
    try:
        t=p1[index_temp[0]].replace(" ", "")
        t=t.replace("=", "")
        t=t.replace("c", "")
        t=t.replace("Temperature", "")
        t=int(t)
        temp.append(t)
    except:
        temp.append(-1)
    try:
        bi=p1[index_bias[0]].replace(" ", "")
        bi=bi.replace("=", "")
        bi=bi.replace("uA", "")
        bi=bi.replace("TxBiasCurrent", "")
        bi=int(bi)
        bias.append(bi)
    except:
        bias.append(-1)
    try:
        vo=p1[index_vol[0]].replace(" ", "")
        vo=vo.replace("=", "")
        vo=vo.replace("mV", "")
        vo=vo.replace("Voltage", "")
        vo=int(vo)
        vol.append(vo)
    except:
        vol.append(-1)
        
    if rx_tx[0]>0:
        return rx_tx[1],rx_tx[0],temp[0],bias[0],vol[0]
    else:
        return rx_tx[0],rx_tx[1],temp[0],bias[0],vol[0] 
###
def brc_ont_save_info(dir):
    file=open(dir,"a+")
    file.write("=======THONG SO CAC NGUONG========"+"\n")
    file.write("SPEED_DOWN_WARNING="+str(SPEED_DOWN_WARNING)+"(Mbps)\n")
    file.write("SPEED_UP_WARNING="+str(SPEED_UP_WARNING)+"(Mbps)\n")
    file.write("ID_VNPT_HN_SPEEDTEST="+str(ID_VNPT_HN)+"\n")
    file.write("COUNT_SAMPLE_IPERF="+str(COUNT_SAMPLE_IPERF)+"(s/chu ky)\n")
    file.write("IP_SERVER_IPERF="+str(IP_SERVER_IPERF)+"\n")
    file.write("IPERF BANDWIDTH="+str(BW_LAN_DOWN)+"(Mbps)\n")
    file.write("SPEED_IPERF_WARNING="+str(SPEED_IPERF_WARNING)+"(Mbps)\n")
    file.write("\n\n==================================\n")
    file.write("==========THONG TIN ONT==========="+"\n")
    p=subprocess.getoutput("expect "+PY_DIR_SHELL+"040BRC_shell/info_ont.sh "+IP_ONT)
    file.write(p+"\n")
    file.close

###
def check_ping(ip_ping="8.8.8.8", if_name=IF_WIFI_CARD, count=10):
    "return ratio loss when ping to an IP address"
    index=[]
    p=subprocess.getoutput("ping " +ip_ping+ " -I "+if_name+" -c "+str(count)+" | grep loss")
    for i in range(len(p)):
        if p[i]=='v' and p[i+1]=='e':
            index.append(i+4)
            break
    for i in range(len(p)):
        if p[i]=='%':
            index.append(i)
            break
    try: 
        result_ping=p[index[0]:index[1]]
        return int(result_ping)
    except:
        print("khong the ping")
        return -1
###
def get_speedtest(id_server=6085):
    index_download=[]
    index_upload=[]
    result=[]
    p=subprocess.getoutput("speedtest --server "+str(id_server)+" | grep bit/s")
    p1=p.split('\n')
    if len(p1)==2:
        for i in range(len(p1[0])):
            if p1[0][i]=='a' and p1[0][i+1]=='d':
                index_download.append(i+3)
                break
        for i in range(len(p1[0])):
            if p1[0][i]=='M' and p1[0][i+1]=='b':
                index_download.append(i-1)
                break
        for i in range(len(p1[1])):
            if p1[1][i]=='a' and p1[1][i+1]=='d':
                index_upload.append(i+3)
                break
        for i in range(len(p1[1])):
            if p1[1][i]=='M' and p1[1][i+1]=='b':
                index_upload.append(i-1)
                break
        if len(index_download)==2:
            try:  
                result_download=float(p1[0][index_download[0]:index_download[1]])
                result.append(result_download)
            except:
                result.append(-1)
        else:
            result.append(-1)
        if len(index_upload)==2:
            try:
                result_upload=float(p1[1][index_upload[0]:index_upload[1]])
                result.append(result_upload)
            except:
                result.append(-1)
        else:
            result.append(-1)
    else:
        result.append(-1)
        result.append(-1)
    return result

###
def pc_on_card_Wifi():
    os.system("nmcli radio wifi on")
###
def pc_off_card_wifi():
    os.system("nmcli radio wifi off")
###
def pc_rescan_wifi():
    os.system("nmcli dev wifi rescan")
###
def pc_off_card_ethernet():
    os.system("nmcli networking off")
###
def pc_on_card_ethernet():
    os.system("nmcli networking on")
###
def pc_check_ipv4_public(link="https://ipinfo.io/ip"):
    p=subprocess.getoutput("curl "+link)
    time.sleep(2)
    try:
        p1=p.split('\n')
        x=len(p1)
        return p1[x-1]
    except:
        return "NULL"
###
def pc_on_ethernet_off_wifi():
    pc_off_card_wifi()
    time.sleep(1)
    pc_on_card_ethernet()
    time.sleep(2)
###
def pc_off_ethernet_on_wifi():
    pc_off_card_ethernet()
    time.sleep(1)
    pc_on_card_Wifi()
    time.sleep(5)
    pc_rescan_wifi()
###
def pc_forget_ssid(ssid_name=SSID_5G):
    p=subprocess.getoutput("nmcli c delete "+ssid_name)
    return p
###
def pc_connect_to_ssid(ssid_name=SSID_5G,pw_ssid=PW_SSID_5H):
    p=subprocess.getoutput("nmcli dev wifi connect "+ssid_name+" password "+pw_ssid)
    count=p.count(" successfully")
    return count
###
def pc_switching_connection_ssid(ssid_name,if_card=IF_WIFI_CARD):
    try:
        p=subprocess.getoutput("nmcli connection up "+str(ssid_name))
        time.sleep(2)
        count=p.count("successfully activated")
        if count==0:
            return 0
        else:
            p1=subprocess.getoutput("iwconfig "+str(if_card)+" | grep ESSID")
            time.sleep(1)
            index=0
            try:
                for i in range(len(p1)):
                    if(p1[i]==':' and p1[i+1]=='"'):
                        index=i+2
                        break
                if p1[index:(index+len(ssid_name))]==ssid_name:
                    return 1
                else:
                    return 0
            except:
                return 0
                    
    except:
        return 0
###
def pc_switching_connection_ssid_2(ssid_name,if_card=IF_WIFI_CARD):
    time.sleep(1)
    os.system("nmcli connection up "+str(ssid_name))
    time.sleep(2)
    try:
        p1=subprocess.getoutput("iwconfig "+str(if_card)+" | grep ESSID")
        index=[]
        size=len(p1)
        for i in range(size):
            if(p1[i]==':' and p1[i+1]=='"'):
                index.append(i+2)
                break
        for i in range(size):
            if(p1[i]=='"' and p1[i+1]==' '):
                index.append(i)
                break
        if p1[index[0]:index[1]]==ssid_name:
            return 1
        else:
            return 0 
    except:
        return 0
###
def pc_download_tcp(ip_server=IP_SERVER_IPERF, countsample=COUNT_SAMPLE_IPERF, bandwidth=BW_LAN_DOWN):
    "format cli: (iperf3 -c ip_server -t count_sample -b bandwidth -f m -R)"
    id_line_start=0
    result_download=[]
    p=subprocess.getoutput("iperf3 -c "+ip_server+" -t "+str(countsample)+" -b "+str(bandwidth)+"m -f m -R")
    p1=p.split('\n')
    for i in range(len(p1)):
        check=0
        for j in range(len(p1[i])):
            if (p1[i][j]=='I' and p1[i][j+1]=='D'):
                check=check+1
                break
        if check==1:
            id_line_start=i+1
            break
    if id_line_start==0:
        return 0,p
    else:
        try:
            for k in p1[id_line_start:(id_line_start+countsample)]:
                index=[]
                for i in range(len(k)):
                    if(k[i]=='e' and k[i+1]=='s'):
                        index.append(i+4)
                        break
                for i in range(len(k)):
                    if(k[i]=='M' and k[i+1]=='b'):
                        index.append(i-1)
                        break
                if len(index)==2:
                    result_download.append(float(k[index[0]:index[1]]))
                else:
                    result_download.append(0.0)
            return round(numpy.average(result_download),2),p
        except:
            return 0,p
###
def write_csv(dir,thoi_gian,\
              result_ping,valid_result_ping,\
              result_ping_iperf,valid_result_ping_iperf,\
              result_temperature_optical,valid_result_temperature_optical,\
              result_rx_optical,valid_result_rx_optical,\
              result_tx_optical,valid_result_tx_optical,\
              result_speed_download,valid_result_speed_download,\
              result_speed_upload,valid_result_speed_upload,\
              result_iperf_down,valid_result_iperf_down,\
              result_ip_v4_public,valid_result_ip_v4_public,\
              valid_parameters,\
              result_bias_optical,result_vol_optical):
    "write data result after finish valid process"
    with open(dir, mode='w') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerow(['Time', \
                               'Loss Ping NET(%)', 'Valid Ping NET', \
                               'Loss Ping iperf(%)', 'Valid Ping iperf', \
                               'ToC BOB','Valid ToC BOB',\
                               'Rx Optical(dBm)','Valid Rx Optical',\
                               'Tx Optical(dBm)','Valid Tx Optical',\
                               'Down Speedtest(Mbps)','Valid Speed Download',\
                               'Up Speedtest(Mbps)','Valid Speed Upload',\
                               'iperf LAN Down(Mbps)','Valid iperf LAN',\
                               'IPv4 PPPoE','Valid IPv4 PPPoE',\
                               '[<SUMMARY>]',\
                               '{Bias optical (uA)}','{Voltage optical (mV)}'])
        for i in range(len(thoi_gian)):
            csv_file.writerow([thoi_gian[i],\
                           result_ping[i],valid_result_ping[i],\
                           result_ping_iperf[i],valid_result_ping_iperf[i],\
                           result_temperature_optical[i],valid_result_temperature_optical[i],\
                           result_rx_optical[i],valid_result_rx_optical[i],\
                           result_tx_optical[i],valid_result_tx_optical[i],\
                           result_speed_download[i],valid_result_speed_download[i],\
                           result_speed_upload[i],valid_result_speed_upload[i],\
                           result_iperf_down[i],valid_result_iperf_down[i],\
                           result_ip_v4_public[i],valid_result_ip_v4_public[i],\
                           valid_parameters[i],\
                           result_bias_optical[i],result_vol_optical[i]])
###
def write_csv_2(dir,thoi_gian):
    "Wrire data result in valid process"
    with open(dir, mode='a+') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        index=len(thoi_gian)
        if index==1:
            csv_file.writerow(['Time', \
                               'Loss Ping NET(%)', 'Valid Ping NET', \
#                                'Loss Ping iperf(%)', 'Valid Ping iperf', \
                               'ToC BOB','Valid ToC BOB',\
                               'Rx Optical(dBm)','Valid Rx Optical',\
                               'Tx Optical(dBm)','Valid Tx Optical',\
#                                'Down Speedtest(Mbps)','Valid Speed Download',\
#                                'Up Speedtest(Mbps)','Valid Speed Upload',\
#                                'iperf LAN Down(Mbps)','Valid iperf LAN',\
#                                'IPv4 PPPoE','Valid IPv4 PPPoE',\
                               '[<SUMMARY>]',\
                               '{Bias optical (uA)}','{Voltage optical (mV)}'])
        csv_file.writerow([thoi_gian[index-1],\
                           result_ping[index-1],valid_result_ping[index-1],\
#                            result_ping_iperf[index-1],valid_result_ping_iperf[index-1],\
                           result_temperature_optical[index-1],valid_result_temperature_optical[index-1],\
                           result_rx_optical[index-1],valid_result_rx_optical[index-1],\
                           result_tx_optical[index-1],valid_result_tx_optical[index-1],\
#                            result_speed_download[index-1],valid_result_speed_download[index-1],\
#                            result_speed_upload[index-1],valid_result_speed_upload[index-1],\
#                            result_iperf_down[index-1],valid_result_iperf_down[index-1],\
#                            result_ip_v4_public[index-1],valid_result_ip_v4_public[index-1],\
                           valid_parameters[index-1],\
                           result_bias_optical[index-1],result_vol_optical[index-1]])
###
def get_list_valid_lan(index):
    list_valid_lan=[]
    for j in list_all_valid_result_lan:
        if len(j)>0:
            list_valid_lan.append(j[index])
    return list_valid_lan
###
def get_list_data_lan(index):
    list_data_lan=[]
    for j in list_all_paremeters_lan:
        if len(j)>0:
            list_data_lan.append(j[index])
    return list_data_lan
###
def get_max_parameters(list_parameters):
    index_parameters=[]
    for x in list_parameters:
        index_parameters.append(list.index(LEVEL, x))
    result=max(index_parameters)
    return LEVEL[result]
###
def write_list_to_csv(dir_file_csv,list):
    with open(dir_file_csv, mode='a+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list)
###
def write_csv_by_column(dir_file, col_0='',col_1='', col_2='', col_3='', col_4='', col_5='', col_6='', col_7='', col_8='', col_9='', col_10='', col_11='', col_12='', col_13='', col_14=''):
    with open(dir_file, mode='a+') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerow([str(col_0),str(col_1), str(col_2), \
                           str(col_3), str(col_4), \
                           str(col_5), str(col_6), \
                           str(col_7), str(col_8), \
                           str(col_9), str(col_10), \
                           str(col_11), str(col_12), \
                           str(col_13), str(col_14)])


