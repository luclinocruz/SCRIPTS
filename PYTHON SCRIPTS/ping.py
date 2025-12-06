import subprocess # to call for my comand ping
import platform  # To distinguish which platform I am using

def execute_ping(target):
    """
    Function that identifies the operating system before executing the appropriate ping.
    """
    # 1. Identify the Operating System (Windows or Linux/macOS)
    current_os = platform.system().lower()
    
    # 2. Define the packet count parameter
    # Windows uses '-n', Linux/Mac uses '-c'
    parameter = '-n' if current_os == 'windows' else '-c'
    
    # limiting it to 4 pings so the program doesn't run forever
    command = ['ping', parameter, '4', target]

    print(f"\n--- Starting Ping for: {target} on system {current_os} ---")
    
    try:
        # 3. Execute the command on the system
        # subprocess.run waits for the command to finish to continue the script
        subprocess.run(command, check=True)
        print("\n--- Ping completed successfully ---")
        
    except subprocess.CalledProcessError:
        print(f"\n[Error] Could not contact the target: {target}")
    except Exception as e:
        print(f"\n[Unexpected Error] {e}")

# --- Main Program ---
if __name__ == "__main__":
    # Asks the user for the IP or Domain
    target_ip = input("Enter the target IP or domain (e.g., google.com or 192.168.1.1): ")
    
    if target_ip.strip(): # Checks if it is not empty
        execute_ping(target_ip)
    else:
        print("Please enter a valid address.")