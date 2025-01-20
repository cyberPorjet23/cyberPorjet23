                             wifipentest

**wifipentest** is a powerful Python-based tool designed for Wi-Fi network penetration testing. It provides an easy-to-use interface for security professionals and enthusiasts to test the security of Wi-Fi networks. The tool is equipped with various features that allow you to perform network discovery, attack simulations, and vulnerability analysis.

                             Features

- **Network Discovery**: Detect available Wi-Fi networks in the vicinity.
- **WPA/WPA2 Cracking**: Utilize dictionary and brute-force attacks to crack Wi-Fi passwords.
- **Deauthentication Attack**: Perform deauthentication attacks to disconnect clients from a network.
- **Handshake Capture**: Capture WPA handshakes for offline cracking.
                             MORE............
                            
                             Requirements

- Python 3 
- A compatible wireless network adapter (supporting monitor mode and packet injection)

                             Installation

1. Clone the repository:

   git clone https://github.com/cyberPorjet23/wifipentest.git
          
                             ENTER cmd
   cd wifipentest

   sudo apt-get install aircrack-ng
    
   sudo apt-get install hashcat

   sudo apt install hcxtools

   python3 wifi exploit.py


                              Usage exp
  
                        Capture Handshake:

   python wifipentest.py capture-handshake --iface wlan0mon --ap-mac AA:BB:CC:DD:EE:FF --target-mac 11:22:33:44:55:66 --channel 6
   
                        Capture PMKID:


   python wifipentest.py capture-pmkid --iface wlan0mon

                       Crack Handshake:

   python wifipentest.py crack-handshake --handshake capture.cap --wordlist rockyou.txt

                         Crack PMKID
                         
   python wifipentest.py crack-pmkid --pmkid pmkid.pcapng --wordlist rockyou.txt

            
            I love YOU BORTHERS ❤️❤️❤️❤️
