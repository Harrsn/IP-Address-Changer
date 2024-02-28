# IP Address Changer

This program allows you to change the IP address of your network interface easily.

## Usage:

1. Ensure that you run the program with administrative/root privileges, depending on your operating system.

2. Follow the on-screen prompts to perform the desired action:
   - To change the IP address, select option 1 from the menu and provide the required inputs (network interface, IP address range).
   - To set the IP address to DHCP, select option 2 from the menu and provide the network interface.

3. Follow the confirmation prompts to confirm your actions.

## Supported Platforms:

- Windows
- Linux
- macOS

## Dependencies:

- Python 3.x
- `IPaddress` module (standard library)
- `subprocess` module (standard library)
- `socket` module (standard library)
- `platform` module (standard library)

## Input Validation:

- The program validates user input for IP addresses to ensure they are in the correct format.

## Error Handling:

- The program handles errors gracefully and provides informative error messages in case of failures.

## Logging:

- All program activities are logged to a file named 'ip_changer.log' for troubleshooting purposes.
