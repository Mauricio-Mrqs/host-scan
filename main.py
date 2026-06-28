import os, subprocess, ipaddress
from datetime import datetime

def ping_ip(ip_address) -> bool:
    # If the OS is windows than the parameter will be "-n" else will be "-c"
    parameters = '-c' if os.name.lower() == 'posix' else '-n'
    # '1' is the amount of packages
    command = ['ping', parameters, '1', ip_address]
    try:
        subprocess.check_output(command, timeout=0.2)
        #print(output.decode())
        return True
    # If the time runs out or an error occurs than returns false (unreacheble)
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError:
        return False

def create_directory() -> None: # creating directory for the ip files
    try:
        os.mkdir('result_scan')
    except FileExistsError:
        pass
    except Exception as e:
        print(f'[-] An error occurred: {e}')

def main() -> None:
    # Creating an object of type IPv4 and Defining the list of all hosts 
    while True:
        try:
            network = input('Type here the network [ex: 0.0.0.0/24] : ')
            all_hosts = list(ipaddress.ip_network(network).hosts())
        except Exception as e:
            print(f'\n[-] An error occurred: {e}\n')
        else:
            break

    all_hosts_on: list = []
    offline_hosts: int = 0
    online_hosts: int = 0
    file_name: str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    for host in all_hosts:
        if ping_ip(str(host)):
            print(f'[+] {host} -> online')
            online_hosts += 1
            all_hosts_on.append(host) # Adding every host that is on
        else:
            print(f'[-] {host} -> no response')
            offline_hosts += 1

    create_directory()

    # Creating and writing the IPs in the result file
    with open(f'result_scan/{file_name}.txt', 'w', encoding='utf-8') as file:
        file.write('- HOSTS ON -\n')
        for host in all_hosts_on:
            file.write(f'{host}\n')

    print('\n[+] Finished successfully\n')

    print(f'Hosts scanned: {offline_hosts + online_hosts}')
    print(f'Hosts active: {online_hosts}')
    print(f'Hosts inactive: {offline_hosts}\n')

if __name__ == '__main__':
    main()

