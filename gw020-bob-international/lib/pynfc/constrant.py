### CONTROL_PC ####
PY_DIR_ROOT='/home/ubuntu/performance/'
PY_DIR_SRC='/home/ubuntu/performance/lib/pynfc/'
PY_DIR_SHELL='/home/ubuntu/performance/lib/pynfc/shell/'
IF_LAN_CARD="enp2s0"
IF_WIFI_CARD="wlp3s0"
USER_SYSTEM="ubuntu"
###################
IP_ONT="192.168.1.1"
DAY=86400
HOUR=3600
IP_GOOGLE_V4="8.8.8.8"
ID_VNPT_HN=6085
SSID_2G="040AC_2G"
PW_SSID_2H="123456789"
SSID_5G="040AC_5G"
PW_SSID_5H="123456789"
LEVEL=["OK","WARNING","CRITICAL","UNKNOW"]
#####Threshold warning#####
ONT_OPTICAL_WARNING_T_THUONG=60
ONT_OPTICAL_WARNING_T_CAO=75
ONT_OPTICAL_WARINNG_RX_DOWN=-27
ONT_OPTICAL_WARINNG_RX_UP=-9
ONT_OPTICAL_WARINNG_TX_DOWN=0.5
ONT_OPTICAL_WARINNG_TX_UP=4.5
SPEED_DOWN_WARNING=35
SPEED_UP_WARNING=35
# IP_SERVER_IPERF="10.84.107.106"
IP_SERVER_IPERF="1192.168.1.229"
COUNT_SAMPLE_IPERF=30
BW_LAN_DOWN=900
SPEED_IPERF_WARNING=650
GMAIL_USER="gponttcn@gmail.com"
GMAIL_RCV="gponttcn@gmail.com"
GMAIL_PW="ttcn@99CN"
GMAIL_PORT_SMTP=587
GMAIL_IP_SMTP="108.177.97.109"
WF_NET1="OLE"
WF_NET2="OLE"
WF_NET3="040H_5G"
LIST_WF_NET=[WF_NET1,WF_NET2,WF_NET3]
COUNT_CHANGE_IP4_PUBLIC=0
###
thoi_gian=[]
valid_parameters=[]
result_temperature_optical=[]
valid_result_temperature_optical=[]
result_ping=[]
valid_result_ping=[]
result_ping_iperf=[]
valid_result_ping_iperf=[]
result_speed_download=[]
valid_result_speed_download=[]
result_speed_upload=[]
valid_result_speed_upload=[]
result_rx_optical=[]
valid_result_rx_optical=[]
result_tx_optical=[]
valid_result_tx_optical=[]
result_iperf_down=[]
valid_result_iperf_down=[]
result_bias_optical=[]
result_vol_optical=[]
result_ip_v4_public=[]
valid_result_ip_v4_public=[]
###
list_all_paremeters_lan=[valid_parameters,thoi_gian,result_temperature_optical,valid_result_temperature_optical,\
                     result_ping,valid_result_ping,result_ping_iperf,valid_result_ping_iperf,\
                     result_speed_download,valid_result_speed_download,result_speed_upload,result_speed_upload,\
                     valid_result_speed_upload,valid_result_speed_upload,result_rx_optical,valid_result_rx_optical,\
                     result_tx_optical,valid_result_tx_optical,result_iperf_down,valid_result_iperf_down,\
                     result_bias_optical,result_vol_optical,result_ip_v4_public,valid_result_ip_v4_public]
###
list_all_valid_result_lan=[valid_result_temperature_optical,valid_result_ping,valid_result_ping_iperf,\
                       valid_result_speed_download,valid_result_speed_upload,valid_result_rx_optical,valid_result_tx_optical,\
                       valid_result_iperf_down,valid_result_ip_v4_public]



