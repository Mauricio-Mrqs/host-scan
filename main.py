import os, subprocess, ipaddress

def ping_ip(ip_address) -> bool: # Function to execute the command ping
    # If the OS is windows than the parameter will be "-n" else will be "-c"
    parameters = '-c' if os.name.lower() == 'posix' else '-n'
    # Creating the ping command, '1' is the amount of packages
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
        print()
    except Exception as e:
        print(f'[-] An error occurred: {e}')

def main() -> None:
    network = input('Type here the network [ex: 0.0.0.0/24] : ')

# Creating an object of type IPv4 and Defining the list of all hosts 
    all_hosts = list(ipaddress.ip_network(network).hosts())
    hosts_on: list = []

    for host in all_hosts:
        if ping_ip(str(host)):
            print(f'{host} -> on')
            hosts_on.append(host) # Adding every host that is on
        else:
            print(f'{host} -> no answer')

    create_directory()

    # Creating and writing the IPs in the result file
    with open('result_scan/scan.txt', 'w', encoding='utf-8') as file:
        file.write('- HOSTS ON -')
        for host in hosts_on:
            file.write(f'\n{host}')

    print('[+] Finished successfully\n')

if __name__ == '__main__':
    main()

