import requests, ast
import datetime
from requests.exceptions import Timeout
import config



TIME_OUT = 5


def send_simple_message(user_list, stats, failed):

    for user in user_list:
        return requests.post(
                "https://api.mailgun.net/v3/sandbox23b720d290024b17a5a52cc59b89b4e1.mailgun.org/messages",
                auth=("api", "key-a8814c29f0053956c33de3383f3a0e82"),
                data={"from": "Server Health<postmaster@sandbox23b720d290024b17a5a52cc59b89b4e1.mailgun.org>",
                "to": user,
                "subject": "Server status at : {}".format(datetime.datetime.now()),
                "text": "Server status \n Passed Status\n*************************\n {} \n Failed\n**************************\n {}".format(stats,failed)})
            #"html": "<html>str(stats.get_system_status())</html>"





def get_status_of_servers():
    servers = config.servers
    result_data = {}
    failed_data = []
    for server in servers:
        #import pdb;pdb.set_trace()
        try:
            server_stat_url = "http://{}:{}/stats/?source=internal".format(server,5000)
            data = requests.get(server_stat_url, timeout = TIME_OUT)
            data = ast.literal_eval(data.content.decode("utf-8"))
            print(data)
            result_data[server] = data
        except Timeout as t:
            print(t)
            failed_data.append(server)
            continue
        except Exception as e:
            print(e)
    return result_data, failed_data

def run():
    stats,failed = get_status_of_servers()
    send_simple_message(config.users,stats,failed)





if __name__ == "__main__":
    print("starting the driver to check the server status")
    run()
