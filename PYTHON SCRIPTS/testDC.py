import ssl
import socket

def get_canonical_name(ip_address):
    """
    Attempts to return the most recognizable 'Common Name' for an IP address.
    Priority:
    1. SSL Certificate Common Name (CN) - best for recognizable domains (www.google.com)
    2. Reverse DNS Hostname - best for server names (server1.host.com)
    """
    
    # --- METHOD 1: Try to grab the SSL Certificate (Port 443) ---
    try:
        # Create a context that ignores hostname mismatch (since we are connecting via IP)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False 
        
        # We must set CERT_REQUIRED to force Python to parse the certificate fields.
        # Note: This requires the target to have a valid certificate trusted by your machine.
        ctx.verify_mode = ssl.CERT_REQUIRED
        
        # Connect with a short timeout
        with socket.create_connection((ip_address, 443), timeout=4) as sock:
            with ctx.wrap_socket(sock, server_hostname=ip_address) as ssock:
                cert = ssock.getpeercert()
                
                # Parse the 'subject' field to find 'commonName'
                # Structure is: ((('commonName', 'www.google.com'),), ...)
                subject_items = [item[0] for item in cert['subject']]
                subject_dict = dict(subject_items)
                
                common_name = subject_dict.get('commonName')
                if common_name:
                    return f"{common_name} (Source: SSL Cert)"
                    
    except Exception as e:
        # If SSL fails (port closed, invalid cert, timeout), we silently move to fallback
        pass

    # --- METHOD 2: Fallback to Standard Reverse DNS ---
    try:
        # This returns the infrastructure name (e.g., 1e100.net for Google)
        hostname = socket.gethostbyaddr(ip_address)[0]
        return f"{hostname} (Source: Reverse DNS)"
    except Exception:
        return "Name could not be resolved"

# --- EXAMPLES ---

# 1. Google IP
google_ip = "142.250.190.46"
print(f"IP: {google_ip} -> {get_canonical_name(google_ip)}")

# 2. Cloudflare/CDN IP (See warning below)
cloudflare_ip = "104.21.19.19" 
print(f"IP: {cloudflare_ip} -> {get_canonical_name(cloudflare_ip)}")

# 3. Local DNS (Google DNS)
dns_ip = "8.8.8.8"
print(f"IP: {dns_ip} -> {get_canonical_name(dns_ip)}")