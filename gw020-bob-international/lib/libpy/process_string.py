############################
########PYTHON VER2#########
############################
# import subprocess
# import os
import commands

def get_time_system():
#     time_sys=subprocess.Popen(['date','+%d%m%Y_%H%M%S'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     time_sys=subprocess.Popen(['date','+%N'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     return time_sys.stdout.read()
    result = commands.getoutput('date +%d%m%Y_%H%M%S')
    return result



