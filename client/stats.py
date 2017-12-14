from subprocess import Popen, PIPE, STDOUT




def run_command(cmd = None):
    print("Running the command")
    output = ""
    try:
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read().decode("ascii").strip().replace("\n","</br>")
    except Exception as e:
        print(e)
    return output



def get_system_status():
    print("getting system ststaus")
    sys_data = {}
    p = Popen("free -m | head -2 | tail -1 | awk {'print$3'}", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    sys_data["ram_used"] = p.stdout.read().decode("ascii").strip()
    p = Popen("free -m | head -2 | tail -1 | awk {'print$2'}", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    sys_data["total_ram"] = p.stdout.read().decode("ascii").strip()
    p = Popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    sys_data["cpu_usage"] = p.stdout.read().decode("ascii").strip()
    p = Popen("grep 'cpu ' /proc/stat ", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    sys_data["cpu_usage_info"] = p.stdout.read().decode("ascii").strip().split("\n")
    p = Popen("uname -a", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    sys_data["machine_details"] = p.stdout.read().decode("ascii").strip()
    return sys_data

    
def get_process_list(sort_by = "cpu", count = 10):
    print("getting processlist")
    if sort_by == "cpu":
        cmd = "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n {}".format(count)
    elif sort_by == "mem":
        cmd = "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -n {}".format(count)
    else:
        cmd = "ps -eo pid,ppid,cmd,%mem,%cpu"
    print(cmd)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read().decode("ascii").strip().replace("\n","</br>")
