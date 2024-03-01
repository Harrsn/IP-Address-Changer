import subprocess
import logging
import socket
import ipaddress
import os
import platform

logging.basicConfig(filename='ip_changer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_current_ip():
    try:
        ##Create a socket object to get local machine's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  ##Connect to Google's DNS server
        current_ip = s.getsockname()[0]  ##Get local IP address
        s.close()
        return current_ip
    except Exception as e:
        logging.error(f"Error in determining the current IP address: {e}")
        return None

def generate_new_ip(current_ip, start_ip, end_ip):
    try:
        ##Convert current IP address to an IPv4Address object
        current_ip_address = ipaddress.IPv4Address(current_ip)
        start_ip_address = ipaddress.IPv4Address(start_ip)
        end_ip_address = ipaddress.IPv4Address(end_ip)

        ##Check if the current IP address is within specified range
        if start_ip_address <= current_ip_address <= end_ip_address:
            ##Generate a new IP address by incrementing the current IP address
            new_ip_address = current_ip_address + 1
            ##Ensure the new IP address is within specified range
            if new_ip_address <= end_ip_address:
                return str(new_ip_address)
            else:
                logging.error("No available IP addresses within the specified range.")
                return None
        else:
            logging.error("Current IP address is not within the specified range.")
            return None
    except Exception as e:
        logging.error(f"Error in generating new IP address: {e}")
        return None

def change_ip_address(interface, new_ip):
    try:
        if platform.system() == 'Windows':
            ##Change IP address using netsh (Windows)
            subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'address', f'name="{interface}"', 'static', new_ip, '255.255.255.0'], check=True)
        elif platform.system() in ['Linux', 'Darwin']:
            ##Change IP address using ifconfig (Linux/mac)
            subprocess.run(['sudo', 'ifconfig', interface, new_ip, 'netmask', '255.255.255.0', 'up'], check=True)
        else:
            logging.error("Unsupported operating system.")
            print("Unsupported operating system.")
            return

        logging.info(f"IP address changed successfully to {new_ip}")
        print(f"IP address changed successfully to {new_ip}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")

def validate_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def get_ip_range():
    start_ip = input("Enter the start IP address of the range: ")
    while not validate_ip(start_ip):
        start_ip = input("Invalid IP address. Please enter a valid start IP address: ")

    end_ip = input("Enter the end IP address of the range: ")
    while not validate_ip(end_ip):
        end_ip = input("Invalid IP address. Please enter a valid end IP address: ")

    return start_ip, end_ip

def set_dhcp(interface):
    try:
        if platform.system() == 'Windows':
            ##Set IP address to DHCP using netsh (Windows)
            subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'address', f'name="{interface}"', 'dhcp'], check=True)
        elif platform.system() in ['Linux', 'Darwin']:
            ##Set IP address to DHCP using dhclient (Linux/mac)
            subprocess.run(['sudo', 'dhclient', '-r', interface], check=True)
        else:
            logging.error("Unsupported operating system.")
            print("Unsupported operating system.")
            return

        logging.info(f"IP address set to DHCP for interface {interface}")
        print(f"IP address set to DHCP for interface {interface}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")

def is_admin():
    if platform.system() == 'Windows':
        try:
            ##Attempt to open a system-protected directory for writing
            with open(os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), 'temp.txt'), 'w') as temp_file:
                pass
            ##If successful, delete the temp file and return True
            os.remove(temp_file.name)
            return True
        except:
            return False
    elif platform.system() in ['Linux', 'Darwin']:
        return os.geteuid() == 0
    else:
        return False

if __name__ == "__main__":
    try:
        if not is_admin():
            print("Please run this script with administrative/root privileges.")
            exit()

        print("Welcome to the IP Address Changer")

        while True:
            print("\nMenu:")
            print("1. Change IP address")
            print("2. Set IP address to DHCP")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                interface = input("Enter the network interface (e.g., eth0, en0): ")

                current_ip = get_current_ip()
                if current_ip:
                    print(f"Current IP address: {current_ip}")

                    start_ip, end_ip = get_ip_range()

                    new_ip = generate_new_ip(current_ip, start_ip, end_ip)
                    if new_ip:
                        confirmation = input(f"Are you sure you want to change the IP address to {new_ip}? (yes/no): ")
                        if confirmation.lower() == 'yes':
                            change_ip_address(interface, new_ip)
                        else:
                            print("IP address change aborted.")
                else:
                    print("Failed to determine the current IP address.")

            elif choice == '2':
                interface = input("Enter the network interface (e.g., eth0, en0): ")
                set_dhcp(interface)

            elif choice == '3':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a valid option.")

    except Exception as ex:
        logging.exception(f"An error occurred: {ex}")
        print(f"An error occurred: {ex}")

