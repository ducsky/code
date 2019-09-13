#!/usr/bin/env bash

usage="Usage: [Robot File] [XUnit File] [Output Directory]"

if [[ "${1}" == "" ]]; then
        echo "You did not input robot file path"
        echo "${usage}"
        exit 0
elif [[ "${2}" == "" ]]; then
        echo "You did not input xunit file path"
        echo "${usage}"
        exit 0
elif [[ "${3}" == "" ]]; then
        echo "You did not input output directory"
        echo "${usage}"
        exit 0
fi

robot_file=$1
xunit_file=$2
output_dir=$3

stop_before_start='yes'
test_config_file="../test_config.txt"
port_in=7000
port_out=7100

remote_appium_server_regex='APPIUM_REMOTE_SERVER:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$)'
remote_appium_username_regex='REMOTE_APPIUM_USERNAME:([a-zA-Z0-9]+$)'
remote_server_ip_regex='REMOTE_SERVER_IP:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$)'
remote_server_username_regex='REMOTE_SERVER_USERNAME:([a-zA-Z0-9]+$)'
ue_number_regex='UE_NUMBER:([0-9]+$)'

# Check test config file
if [[ ! -f "${test_config_file}" ]]; then
        echo "Test Config File Does Not Exist!"
        exit 0
fi

while read -r line; do
        if [[ ${line} =~ ${remote_appium_server_regex} ]]; then
                remote_appium_server="${BASH_REMATCH[1]}"
        elif [[ ${line} =~ ${remote_appium_username_regex} ]]; then
                remote_appium_username="${BASH_REMATCH[1]}"
        elif [[ ${line} =~ ${remote_server_ip_regex} ]]; then
                remote_server_ip="${BASH_REMATCH[1]}"
        elif [[ ${line} =~ ${remote_server_username_regex} ]]; then
                remote_server_username="${BASH_REMATCH[1]}"
        elif [[ ${line} =~ ${ue_number_regex} ]]; then
                ue_number="${BASH_REMATCH[1]}"
        fi
done < "${test_config_file}"

# Killall remote appium processes
ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "killall node"
if [[ "$?" -eq "0" ]]; then
        echo "Kill Appium Remote Processes"
else
        echo "No process of appium found"
fi


# We have 3 files:
# remote_script.sh: Shell script to get number of connected devices on remote Appium Server.
# total_device.txt: Text file contain total number of connected devices.
# run_appium.sh: Shell script to start remote Appium Server

echo -n "" > remote_script.sh
echo -n "" > run_appium.sh
echo -n "" > total_device.txt

if [[ `ls -l 70*.txt 2>/dev/null | wc -l` -gt 0 ]]; then
        rm -f 70*.txt
fi

cat <<"EOF" >> remote_script.sh
echo Device List Start
adb devices | awk '{ print $1 }' | printf '%s\n' "$(tail -n +2)"
EOF

ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} < remote_script.sh >> total_device.txt
device_list_start_line_number=$(awk '/Device List Start/{print NR}' total_device.txt)
sed -i "1,$device_list_start_line_number d" total_device.txt

total_lines=`wc -l < total_device.txt`

while read -r line; do
        if [[ -z "${line}" ]]; then
                isNoDevice=true
                break
        else
                isNoDevice=false
                break
        fi
done < total_device.txt

runCommand="pabot --processes 64 --verbose --pabotlib"

if [[ ${isNoDevice} || "${ue_number}" -eq "0" ]]; then
        echo "No need to run any UEs"
        runCommand+=" --argumentfile ${test_config_file} -x $xunit_file -d $output_dir $robot_file"
elif [[ ! ${isNoDevice} && "${ue_number}" -gt "0" ]]; then
        if [[ ${ue_number} -gt ${total_lines} ]]; then
                echo "[ERROR] Number of devices you want to executed is greater then the total number of connected devices. Please try again"
                exit 0
        fi

        head -n ${ue_number} total_device.txt > total_device_to_execute.txt

        echo "=====List of executed devices====="
        while read -r line; do
        	    echo "$line"
                port_in=`expr $port_in + 1`
                port_out=`expr $port_out + 1`
                echo "--variable DEVICE_NAME:$line" >> $port_in.txt
                echo "--variable APPIUM_REMOTE_PORT:$port_in" >> $port_in.txt
                cat "${test_config_file}" >> $port_in.txt
                echo "appium -p $port_in -bp $port_out -U $line &" >> run_appium.sh
        	    echo "sleep 1" >> run_appium.sh
        done < total_device_to_execute.txt

        chmod +x run_appium.sh
        ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "if [ -f /home/${remote_appium_username}/run_appium.sh ]; then rm -f /home/${remote_appium_username}/run_appium.sh; fi"
        scp run_appium.sh ${remote_appium_username}@${remote_appium_server}:/home/${remote_appium_username}

        ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "/home/${remote_appium_username}/run_appium.sh" > appium_log.out &

        rm -f remote_script.sh total_device.txt total_device_to_execute.txt run_appium.sh

        endTime=$((SECONDS+90))

        while [ $SECONDS -lt $endTime ]; do
                appium_server_num=$(ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "ps cax | grep node | wc -l")

                appium_node_num=$(ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "ps cax | grep appium_node | wc -l")
                selenium_node_num=$(ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "ps cax | grep selenium_node | wc -l")

                if [[ "${appium_node_num}" -gt "0" ]]; then
                    appium_server_num=$(expr "${appium_server_num}" - "${appium_node_num}")
                fi

                if [[ "${selenium_node_num}" -gt "0" ]]; then
                    appium_server_num=$(expr "${appium_server_num}" - "${selenium_node_num}")
                fi

                echo "Current appium servers are running: ${appium_server_num}"
                echo "Current appium node are running: ${appium_node_num}"
                echo "Current selenium node are running: ${selenium_node_num}"

                if [ "${appium_server_num}" -eq "${ue_number}" ]; then
                        echo "Current Appium server are running: ${appium_server_num}"
                        echo "All appium servers are READY!"
                        sleep 5
                        break
                fi
                echo "Current appium servers are running: ${appium_server_num}"
                echo "Expected appium servers number: ${ue_number}"
        done

        echo "Number of devices are going to be executed: ${ue_number}"

        for i in $(seq 1 ${ue_number})
        do
                runCommand+=" --argumentfile$i"
                runCommand+=" `expr 7000 + $i`"
                runCommand+=".txt "
        done
        runCommand+="-x $xunit_file -d $output_dir $robot_file"
fi

#################
# Pabot Process #
#################

#appium_server_num=$(ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "ps cax | grep node | wc -l")

#appium_node_num=$(ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "ps cax | grep appium_node | wc -l")
#selenium_node_num=$(ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "ps cax | grep selenium_node | wc -l")

#if [[ "${appium_node_num}" -gt "0" ]]; then
#    appium_server_num=$(expr "${appium_server_num}" - "${appium_node_num}")
#fi

#if [[ "${selenium_node_num}" -gt "0" ]]; then
#    appium_server_num=$(expr "${appium_server_num}" - "${selenium_node_num}")
#fi

#echo "Current appium servers are running: ${appium_server_num}"
#echo "Current appium node are running: ${appium_node_num}"
#echo "Current selenium node are running: ${selenium_node_num}"

echo $runCommand
$runCommand

if [[ ! ${isNoDevice} ]]; then
        echo "Kill remote appium server"
        ssh -o "StrictHostKeyChecking no" ${remote_appium_username}@${remote_appium_server} "killall node"
fi
exit 0
