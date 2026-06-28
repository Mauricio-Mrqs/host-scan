import os, subprocess, ipaddress, datetime

def ping_ip(ip_address) -> bool:
    # If the OS is windows than the parameter will be "-n" else will be "-c"
    parameters = '-c' if os.name.lower() == 'posix' else '-n'
    # '1' is the amount of packages
    command = ['ping', parameters, '1', ip_address]
    try:
        subprocess.check_output(command, timeout=0.1)
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
        print()
    except Exception as e:
        print(f'[-] An error occurred: {e}')

def main() -> None:
    # Creating an object of type IPv4 and Defining the list of all hosts 
    try:
        network = input('Type here the network [ex: 0.0.0.0/24] : ')
        all_hosts = list(ipaddress.ip_network(network).hosts())
    except Exception as e:
        print(f'\n[-] An error occurred: {e}\n')
        network = input('Try again: ')
        all_hosts = list(ipaddress.ip_network(network).hosts())

    all_hosts_on: list = []
    offline_hosts: int = 0
    online_hosts: int = 0
    file_name: str = str(datetime.datetime.now())

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
        file.write('- HOSTS ON -')
        for host in all_hosts_on:
            file.write(f'\n{host}')

    print('\n[+] Finished successfully\n')

    print(f'Hosts scanned: {offline_hosts + online_hosts}')
    print(f'Hosts active: {online_hosts}')
    print(f'Hosts inactive: {offline_hosts}\n')

if __name__ == '__main__':
    main()

