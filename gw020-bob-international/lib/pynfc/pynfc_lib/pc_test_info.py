from pynfc_lib.pc_get_info import *
from constrant import *
import os
import time
import subprocess

###
def brc_test_info_optical(file,\
                      result_rx_optical,valid_result_rx_optical,\
                      result_tx_optical,valid_result_tx_optical,\
                      result_temperature_optical,valid_result_temperature_optical,\
                      result_bias_optical,result_vol_optical,check=0):
    'Valid Rx,tx and Temperature Optical Module'
    rx,tx,t,bias,vol=brc_get_info_optical(IP_ONT)
    result_bias_optical.append(bias)
    result_vol_optical.append(vol)
    print("Tx Bias Current: ",bias,"(uA)")
    file.write("Tx Bias Current: "+str(bias)+"(uA)"+"\n")
    print("Voltage Current: ",vol,"(mV)")
    file.write("Voltage Current: "+str(vol)+"(mV)"+"\n")
    file.write("Optical Rx:"+str(rx)+" dBm\n")
    file.write("Optical Tx:"+str(tx)+" dBm\n")
    file.write("Nhiet do: "+str(t)+"oC"+"\n")
    optical_valid_rx(rx,result_rx_optical,valid_result_rx_optical)
    optical_valid_tx(tx,result_tx_optical,valid_result_tx_optical)
    if check==0:
        optical_valid_temperature_thuong(t,result_temperature_optical,valid_result_temperature_optical)
    else:
        optical_valid_temperature_cao(t,result_temperature_optical,valid_result_temperature_optical)
###
def optical_valid_tx(tx,result_tx_optical,valid_result_tx_optical):
    if 0<tx<ONT_OPTICAL_WARINNG_TX_DOWN or 4.5<tx<ONT_OPTICAL_WARINNG_TX_UP:
        result_tx_optical.append(tx)
        valid_result_tx_optical.append(LEVEL[1])
        print("Optical Tx=",tx,"dBm,",LEVEL[1])
    elif ONT_OPTICAL_WARINNG_TX_DOWN<=tx<=ONT_OPTICAL_WARINNG_TX_UP:
        result_tx_optical.append(tx)
        valid_result_tx_optical.append(LEVEL[0])
        print("Optical Tx=",tx,"dBm,",LEVEL[0])
    else:
        result_tx_optical.append(tx)
        valid_result_tx_optical.append(LEVEL[2])
        print("Optical Tx=",tx,"dBm,",LEVEL[2])
###
def optical_valid_rx(rx,result_rx_optical,valid_result_rx_optical):
    if ONT_OPTICAL_WARINNG_RX_UP<rx<-8 or -28<rx<-ONT_OPTICAL_WARINNG_RX_DOWN:
        result_rx_optical.append(rx)
        valid_result_rx_optical.append(LEVEL[1])
        print("Optical Rx=",rx,"dBm,",LEVEL[1])
    elif ONT_OPTICAL_WARINNG_RX_DOWN<rx<ONT_OPTICAL_WARINNG_RX_UP:
        result_rx_optical.append(rx)
        valid_result_rx_optical.append(LEVEL[0])
        print("Optical Rx=",rx,"dBm,",LEVEL[0])
    else:
        result_rx_optical.append(rx)
        valid_result_rx_optical.append(LEVEL[2]) 
        print("Optical Rx=",rx,"dBm,",LEVEL[2])
###
def optical_valid_temperature_thuong(temp,result_temperature_optical,valid_result_temperature_optical):
    if 0<temp<ONT_OPTICAL_WARNING_T_THUONG:
        result_temperature_optical.append(temp)
        valid_result_temperature_optical.append(LEVEL[0])
        print("Optical temperature=",temp," oC,",LEVEL[0])
    elif ONT_OPTICAL_WARNING_T_THUONG<temp<=80:
        result_temperature_optical.append(temp)
        valid_result_temperature_optical.append(LEVEL[1])
        print("Optical temperature=",temp," oC,",LEVEL[1])
    else:
        result_temperature_optical.append(temp)
        valid_result_temperature_optical.append(LEVEL[2])
        print("Optical temperature=",temp," oC,",LEVEL[2])
###
def optical_valid_temperature_cao(temp,result_temperature_optical,valid_result_temperature_optical):
    if 0<temp<ONT_OPTICAL_WARNING_T_CAO:
        result_temperature_optical.append(temp)
        valid_result_temperature_optical.append(LEVEL[0])
        print("Optical temperature=",temp," oC,",LEVEL[0])
    elif ONT_OPTICAL_WARNING_T_CAO<temp<=80:
        result_temperature_optical.append(temp)
        valid_result_temperature_optical.append(LEVEL[1])
        print("Optical temperature=",temp," oC,",LEVEL[1])
    else:
        result_temperature_optical.append(temp)
        valid_result_temperature_optical.append(LEVEL[2])
        print("Optical temperature=",temp," oC,",LEVEL[2])        
###
def test_ping(file,result_ping,valid_result_ping,card_name=IF_LAN_CARD):
    i=check_ping(ip_ping=IP_GOOGLE_V4,if_name=card_name)
    if i==-1 or i==100:
        result_ping.append(i)
        valid_result_ping.append(LEVEL[2])
        print("Khong the thuc hien Ping den IP:",IP_GOOGLE_V4)
        file.write("Khong the thuc hien Ping den IP:"+IP_GOOGLE_V4+"\n")  
        j=check_ping(ip_ping=IP_ONT,count=4)
    elif 0<i<100:
        result_ping.append(i)
        valid_result_ping.append(LEVEL[1])
        print("Ping IP",IP_GOOGLE_V4,"loss",i,"%")
        file.write("Ping IP "+str(IP_GOOGLE_V4)+" loss: "+str(i)+"%"+"\n")
        j=check_ping(ip_ping=IP_ONT,count=4)
        if j==-1 or j==100:
            file.write("=====>Khong the thuc hien Ping den IP:"+IP_ONT+"\n")
        else:
            file.write("=====>Kiem tra ping lai voi IP ONT, loss: "+str(j)+"%"+"\n")
#         file.write("Kiem tra ping lai voi IP ONT, loss: "+str(j)+"%"+"\n")
    else:
        result_ping.append(i)
        valid_result_ping.append(LEVEL[0])
        print("Ping qua IP",IP_GOOGLE_V4,"OK, loss 0%")
        file.write("Ping qua "+str(IP_GOOGLE_V4)+" OK, loss 0%"+"\n")
###
def test_parameters(file,thoi_gian,valid_parameters):
    i=len(thoi_gian)
    index_parameters=[]
    list_parameters=[valid_result_ping[i-1],\
#                      valid_result_ping_iperf[i-1],\
                     valid_result_temperature_optical[i-1],\
                     valid_result_rx_optical[i-1],\
                     valid_result_tx_optical[i-1]
#                      valid_result_speed_download[i-1],\
#                      valid_result_speed_upload[i-1],\
#                      valid_result_iperf_down[i-1],\
#                      valid_result_ip_v4_public[i-1]
                     ]
    for x in list_parameters:
        index_parameters.append(list.index(LEVEL, x))
    result=max(index_parameters)
    valid_parameters.append(LEVEL[result])
    file.write("\n=>Summary____: "+LEVEL[result]+"\n")   
###   
def valid_summary(dir,valid_parameters):
    file=open(dir,'w+')
    index_parameters=[]
    for x in valid_parameters:
        index_parameters.append(list.index(LEVEL, x))
    result=max(index_parameters)
    valid_parameters.append(LEVEL[result])
    file.write(LEVEL[result])    
    file.close()
        

