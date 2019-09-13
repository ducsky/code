*** Settings ***
# Library    libpy/module1.py
Library    libpy/process_string.py   WITH NAME    PS 
Library    OperatingSystem    WITH NAME    OS
Library    SSHLibrary    WITH NAME    SSHL
*** Variables ***
${SERVER}    10.2.14.192
${USER}    ubuntu
${PASSWORD}    123456
${DIR_FOLDER}   performance/
${DIR_SRC}   performance/lib/pynfc/
*** Keywords ***
abc
    ${time_sys}=    PS.Get Time System
    Log To Console    \n${time_sys}
    OS.Run    mkdir -p ./result_nfc/
    OS.Run    mkdir -p ./result_nfc/tar/
    OS.Run    tar -cvf pynfc.tar ./lib/pynfc
    SSHL.Open Connection    ${SERVER}    timeout=36000s   
	SSHL.Login    ${USER}    ${PASSWORD}
	SSHL.Execute Command    mkdir ${DIR_FOLDER}     
	SSHL.Put File    pynfc.tar   ${DIR_FOLDER}
	${out_put}=    SSHL.Execute Command    tar -xvf ${DIR_FOLDER}pynfc.tar -C ${DIR_FOLDER}    
	Log To Console    \n${out_put}
	${out_put}=    SSHL.Execute Command    pwd
	Log To Console    \n${out_put}
	Log To Console    \nRun file python
	SSHL.Execute Command    python3.5 ${DIR_SRC}main.py ${time_sys}   
	SSHL.Execute Command    tar -cvf ${DIR_FOLDER}${time_sys}.tar ${DIR_FOLDER}${time_sys}/*
	SSHL.Get File    ${DIR_FOLDER}${time_sys}.tar    ./result_nfc/tar/
	SSHL.Get File    ${DIR_FOLDER}${time_sys}/${time_sys}_final.txt    ./result_nfc/
	${out_put}=    SSHL.Execute Command    rm -rf ${DIR_FOLDER}
	${out_put}=    OS.RUN    tail ./result_nfc/${time_sys}_final.txt
    Should Be Equal    '${out_put}'    'OK'  
    SSHL.Close Connection       
*** Test Cases ***
test
    abc



