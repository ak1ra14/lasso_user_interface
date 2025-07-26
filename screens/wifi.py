import sys
import subprocess

def get_available_wifi():
    wifi_list = []
    if sys.platform == 'darwin':  # Mac
        try:
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                universal_newlines=True
            )
            lines = result.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    ssid = line.split()[0]
                    wifi_list.append(ssid)
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    elif sys.platform.startswith('linux'):
        try:
            result = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], universal_newlines=True)
            wifi_list = [line for line in result.split('\n') if line]
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    elif sys.platform.startswith('win'):
        try:
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], universal_newlines=True)
            for line in result.split('\n'):
                if "SSID" in line:
                    ssid = line.split(":", 1)[1].strip()
                    if ssid:
                        wifi_list.append(ssid)
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    return wifi_list

# Example usage:
if __name__ == "__main__":
    print(get_available_wifi())