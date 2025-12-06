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
        print("1. Find the iP Address")
        print("2. Traceroute")
        print("3. Domanin detail /DNS Lookup")
        print("4. Reverse DNS")
        print("5. MX Records")
        print("6. Quick Port Scan")
        print("7. HTTP Headers")
        print("8. pen t")
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