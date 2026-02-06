import subprocess  # To run terminal commands
import platform    # To check if we are on Windows or Linux
import socket      # To look up IPs and Domains
import webbrowser  # To open Chrome/Firefox automatically
import re          # To check if target is an IP or Domain



# --- HELPER FUNCTIONS ---

def get_target():
    """Asks user for target and cleans it up."""
    print("\n" + "*" * 40)
    raw = input("Enter Target (Domain or IP): ").strip()
    # Remove http:// if the user typed it
    clean = raw.replace("http://", "").replace("https://", "").replace("'", "").split("/")[0]
    return clean

def is_ip_address(target):
    """Checks if the target looks like an IP address (e.g., 192.168.1.1)."""
    # Simple regex to check for IP pattern
    return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target) is not None

def open_browser(url):
    """Opens the default web browser safely."""
    print(f"[*] Opening browser for: {url}")
    webbrowser.open(url)

def get_os_ping_flag(flag_type):
    """Returns the correct flag for Windows vs Linux/Mac"""
    system_name = platform.system().lower()
    is_windows = system_name == "windows"
    
    if flag_type == "count":
        return "-n" if is_windows else "-c"
    
    # Windows uses -l for size, Linux uses -s
    if flag_type == "size":
        return "-l" if is_windows else "-s"
        
    return ""

# --- MAIN MENUS ---

def menu_ping(target):
    # Detect System Explicitly
    sys_name = platform.system()
    print(f"\n--- PING OPTIONS (System Detected: {sys_name}) ---")
    print("1. Standard Ping (4 packets)")
    print("2. Force IP Version (-4 / -6)")
    print("3. Custom Count")
    print("4. Custom Packet Size")
    
    choice = input("Select Ping Option: ")
    
    # Get the correct flag for the current system (e.g., -n for Windows, -c for Linux)
    param_count = get_os_ping_flag("count")
    
    try:
        if choice == "1":
            # Simple ping
            print(f"[*] Running: ping {param_count} 4 {target}")
            subprocess.run(["ping", param_count, "4", target])
            
        elif choice == "2":
            version = input("Type '4' for IPv4 or '6' for IPv6: ")
            if version == "6":
                print("[*] Trying IPv6 Ping...")
                # Note: Some older systems need 'ping6', modern ones use 'ping -6'
                subprocess.run(["ping", "-6", param_count, "4", target])
            else:
                print(f"[*] Running: ping -4 {param_count} 4 {target}")
                subprocess.run(["ping", "-4", param_count, "4", target])

        elif choice == "3":
            count = input("How many packets to send? (e.g., 10): ")
            if not count.isdigit():
                print("[!] Error: Please enter a number.")
                return
            subprocess.run(["ping", param_count, count, target])

        elif choice == "4":
            size = input("Enter packet size in bytes (e.g., 128): ")
            if not size.isdigit():
                print("[!] Error: Please enter a number.")
                return
            
            param_size = get_os_ping_flag("size")
            subprocess.run(["ping", param_size, size, param_count, "4", target])
            
        else:
            print("Invalid choice.")
            
    except Exception as e:
        print(f"[!] Error running ping: {e}")

def menu_google_dorking(target):
    print("\n--- GOOGLE DORKING (Web Search) ---")
    print("1. Find Admin/Login Pages")
    print("2. Find Directory Listings (Index of)")
    print("3. Find Public Files (PDF/DOCX)")
    print("4. Find Specific Text in Site")
    
    choice = input("Select Dork Option: ")
    
    base_url = "https://www.google.com/search?q="
    
    if choice == "1":
        query = f"site:{target} (inurl:admin OR inurl:login OR inurl:panel)"
        open_browser(base_url + query)
        
    elif choice == "2":
        query = f"site:{target} intitle:index.of"
        open_browser(base_url + query)
        
    elif choice == "3":
        query = f"site:{target} (filetype:pdf OR filetype:xls OR filetype:docx)"
        open_browser(base_url + query)
        
    elif choice == "4":
        text = input("Enter text to search for: ")
        query = f"site:{target} intext:\"{text}\""
        open_browser(base_url + query)



def menu_dns_lookup(target):
    print("\n--- DNS LOOKUP (Address Book) ---")
    print("1. Forward Lookup (Domain -> IP)")
    print("2. Reverse Lookup (IP -> Domain)")
    print("3. Get MX Records (Mail Servers)")
    
    choice = input("Select DNS Option: ")
    
    if choice == "1":
        try:
            ip = socket.gethostbyname(target)
            print(f"[*] IP Address: {ip}")
        except:
            print("[!] Could not resolve domain.")
            
    elif choice == "2":
        try:
            # First ensure we have an IP
            ip = socket.gethostbyname(target) 
            print(f"[*] Resolving IP: {ip}")
            host = socket.gethostbyaddr(ip)
            print(f"[*] Hostname: {host[0]}")
            
            """NameDomain = socket.gethostbyname_ex(target)
            print(f"[*] Domain: {NameDomain[0]}")"""

        except:
            print("[!] Could not perform reverse lookup.")
            
    elif choice == "3":
        # FIX: Check if user is trying to get MX records for an IP address
        
        if is_ip_address(target):
            
            print("\n[!] Warning: You cannot check MX Records for an IP Address.")
            """print("    Please change target to a Domain Name (e.g., google.com)")"""
            print("\n   Correcting to Host Name...")
            value = socket.gethostbyaddr(target)
            # return 

            print(f"[*] Fetching Mail Servers for {value[0]}...")
            try:
                subprocess.run(["nslookup", "-type=mx",  value[0]])
            except Exception as e:
                print(f"[!] Error running nslookup: {e}")
        else:
            print(f"[*] Fetching Mail Servers for {target}...")
            try:
                subprocess.run(["nslookup", "-type=mx", target])
            except Exception as e:
                print(f"[!] Error running nslookup: {e}") 




def menu_email_hunter(target):
    print("\n--- EMAIL & USER HUNTING (Browser) ---")
    print("1. Search Emails for Domain (Hunter.io)")
    print("2. Search Username across Social Media")
    
    choice = input("Select Hunter Option: ")
    
    if choice == "1":
        if is_ip_address(target):
            print("[!] Hunter.io requires a Domain Name, not an IP.")
            return
        url = f"https://hunter.io/search/{target}"
        open_browser(url)
        
    elif choice == "2":
        username = input("Enter the Username to track: ")
        query = f"inurl:{username} OR intext:{username}"
        url = f"https://www.google.com/search?q={query}"
        open_browser(url)

# --- MAIN PROGRAM LOOP ---

def main():
    print("Welcome to our Information Gathering Toolkit!")
    
    # Step 1: Get Target
    current_target = get_target()
    
    while True:
        print("\n" + "="*40)
        print(f"CURRENT TARGET: {current_target}")
        print("="*40)
        print("1. Network Ping Tools (Connectivity)")
        print("2. Google Dorking (Web Search)")
        print("3. DNS Lookup (IP & Mail Records)")
        print("4. Email & Username Finding")
        print("5. Change Target")
        print("0. Exit Program")
        print("="*40)
        
        main_choice = input("Choose an Option: ")
        
        # Simple Switch Case Structure
        match main_choice:
            case "1":
                menu_ping(current_target)
            case "2":
                menu_google_dorking(current_target)
            case "3":
                menu_dns_lookup(current_target)
            case "4":
                menu_email_hunter(current_target)
            case "5":
                current_target = get_target()
            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid option, try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()