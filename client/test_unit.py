
import stats


def test_run_command():
    result = stats.run_command(cmd='pwd')
    assert result == '/home/sambit/Downloads/marax-master'


def test_get_process_list():
    result = stats.get_process_list(sort_by = "cpu", count = 2)
    assert result == 'PID  PPID CMD                         %MEM %CPU</br>21402  1469 /opt/google/chrome/chrome    7.6  5.3'


def test_get_system_status():
    result = stats.get_system_status()
    assert result == {'cpu_usage': '32.0827',
             'cpu_usage_info': ['cpu  16478975 267572 3264550 41795975 254542 0 89526 0 0 0'],
              'machine_details': 'Linux work-station 4.10.0-38-generic #42~16.04.1-Ubuntu SMP Tue Oct 10 16:32:20 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux',
               'ram_used': '2027',
                'total_ram': '3833'}




