import subprocess
import platform
import socket
import ssl
import json
import urllib.request
import urllib.error
import time

# --- Helper Function ---
def get_clean_target(user_input):
    """
    Removes http://, https:// and paths.
    """
    clean = user_input.replace("http://", "").replace("https://", "")
    clean = clean.split("/")[0]
    return clean

# --- Original 10 Functions (Condensed for space) ---

def option_1_ping(target):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    subprocess.run(['ping', param, '4', target])

def option_2_traceroute(target):
    cmd = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
    try: subprocess.run([cmd, target])
    except: print("Command not found.")

def option_3_dns_lookup(target):
    try: print(f"IP: {socket.gethostbyname(target)}")
    except: print("Error resolving domain.")

def option_4_reverse_dns(target):
    try:
        ip = socket.gethostbyname(target)
        print(f"Hostname: {socket.gethostbyaddr(ip)[0]}")
    except: print("No reverse record.")

def option_5_mx_records(target):
    subprocess.run(['nslookup', '-type=mx', target])

def option_6_port_scan(target):
    ports = [21, 22, 53, 80, 443, 3306, 8080]
    ip = socket.gethostbyname(target)
    print(f"Scanning {target}...")
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            print(f" -> Port {port}: OPEN")
        s.close()

def option_7_http_headers(target):
    try:
        resp = urllib.request.urlopen(f"http://{target}", timeout=5)
        for k, v in resp.info().items(): print(f"{k}: {v}")
    except Exception as e: print(f"Error: {e}")

def option_8_robots_txt(target):
    try:
        resp = urllib.request.urlopen(f"http://{target}/robots.txt", timeout=5)
        print(resp.read().decode('utf-8')[:300])
    except: print("robots.txt not found.")

def option_9_geoip(target):
    try:
        ip = socket.gethostbyname(target)
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as url:
            data = json.loads(url.read().decode())
            print(f"Location: {data.get('city')}, {data.get('country')}")
    except: print("GeoIP failed.")

def option_10_ssl_info(target):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((target, 443)) as s:
            with ctx.wrap_socket(s, server_hostname=target) as ss:
                print(f"Issuer: {ss.getpeercert()['issuer'][1][0][1]}")
    except: print("SSL failed.")

# --- NEW FEATURES (11, 12, 13) ---

def option_11_google_dorks(target):
    print(f"\n--- Generating Google Dork Links for {target} ---")
    print("Click these links to find sensitive info in your browser:\n")
    
    dorks = [
        ("Public Files (PDF/XLS)", f"site:{target} filetype:pdf OR filetype:xls OR filetype:docx"),
        ("Directory Listing", f"site:{target} intitle:index.of"),
        ("Config Files", f"site:{target} ext:xml OR ext:conf OR ext:cnf OR ext:ini"),
        ("Login Pages", f"site:{target} inurl:login OR inurl:admin"),
        ("Pastebin Leaks", f"site:pastebin.com {target}")
    ]

    for name, query in dorks:
        # We replace spaces with + to make a valid URL
        safe_query = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={safe_query}"
        print(f"[*] {name}:")
        print(f"    {url}")
        print("-" * 20)

def option_12_admin_finder(target):
    print(f"\n--- Hunting for Admin Pages on {target} ---")
    print("Note: This might take a few seconds...")
    
    # Common admin paths
    admin_paths = [
        'admin', 'administrator', 'login', 'wp-admin', 'cpanel', 
        'dashboard', 'admin.php', 'user', 'controlpanel'
    ]
    
    found_any = False
    
    for path in admin_paths:
        url = f"http://{target}/{path}"
        try:
            # We assume http (port 80). If you want https, change the string above.
            req = urllib.request.Request(url, method='HEAD') # HEAD is faster than GET
            urllib.request.urlopen(req, timeout=1)
            print(f"[FOUND!] Possible Admin Page: {url}")
            found_any = True
        except urllib.error.HTTPError as e:
            # If code is 401 (Unauthorized) or 403 (Forbidden), it exists but is locked!
            if e.code in [401, 403]:
                print(f"[LOCKED] Page exists but is protected ({e.code}): {url}")
                found_any = True
            # We ignore 404 (Not Found)
        except Exception:
            pass # Ignore connection errors
            
    if not found_any:
        print("No common admin pages found in this short list.")

def option_13_shodan_search(target):
    print(f"\n--- Shodan Host Search for {target} ---")
    
    # 1. Get the IP
    try:
        ip = socket.gethostbyname(target)
        print(f"Target IP: {ip}")
    except:
        print("Could not resolve domain.")
        return

    # 2. Ask for API Key (Shodan requires one)
    print("To use Shodan, you need an API Key.")
    api_key = input("Please paste your Shodan API Key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("Skipping Shodan search (No API Key provided).")
        return

    # 3. Call Shodan API manually (without installing shodan library)
    api_url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            
            print(f"\n[+] Organization: {data.get('org', 'Unknown')}")
            print(f"[+] OS: {data.get('os', 'Unknown')}")
            print("[+] Open Ports found by Shodan:")
            for item in data.get('data', []):
                print(f"    - Port: {item.get('port')} ({item.get('transport')})")
                
    except urllib.error.HTTPError as e:
        print(f"\n[!] Shodan API Error: {e.code}")
        print("Verify your API Key or the target might not be indexed yet.")
    except Exception as e:
        print(f"Error: {e}")

# --- Main Menu ---

def main():
    print("Welcome to the Python Recon Tool v2.0")
    user_target = input("Enter Target Domain or IP: ")
    target = get_clean_target(user_target)
    
    if not target:
        print("Invalid Target.")
        return

    while True:
        print("\n" + "="*30)
        print(f"TARGET: {target}")
        print("="*30)
        print("1. Ping")
        print("2. Traceroute")
        print("3. DNS Lookup")
        print("4. Reverse DNS")
        print("5. MX Records")
        print("6. Quick Port Scan")
        print("7. HTTP Headers")
        print("8. Robots.txt")
        print("9. GeoIP Location")
        print("10. SSL Info")
        print("-" * 30)
        print("11. Google Dork Links (NEW)")
        print("12. Admin Page Finder (NEW)")
        print("13. Shodan Host Info (NEW)")
        print("-" * 30)
        print("0. Exit")
        
        choice = input("Select option: ")

        match choice:
            case "1": option_1_ping(target)
            case "2": option_2_traceroute(target)
            case "3": option_3_dns_lookup(target)
            case "4": option_4_reverse_dns(target)
            case "5": option_5_mx_records(target)
            case "6": option_6_port_scan(target)
            case "7": option_7_http_headers(target)
            case "8": option_8_robots_txt(target)
            case "9": option_9_geoip(target)
            case "10": option_10_ssl_info(target)
            # New Cases
            case "11": option_11_google_dorks(target)
            case "12": option_12_admin_finder(target)
            case "13": option_13_shodan_search(target)
            case "0": break
            case _: print("Invalid option.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()